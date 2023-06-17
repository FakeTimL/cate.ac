<script lang="ts">
import type { Sheet, Attempt, Question, User, Submission } from '@/api';
import axios from 'axios';
import { api } from '@/api';
import { messageErrors } from '@/messages';
import { friendlyDuration } from '@/dates';
import { FormErrors } from '@/errors';

import LoadingText from './components/LoadingText.vue';
import MarkdownContent from './components/MarkdownContent.vue';

class FormFields {
  question: number | null = null;
  user_answer: string = '';
  gpt_marking: boolean = false;
}

class QuestionItem {
  question: Question;
  submission = null as Submission | null;

  modified = false;
  waiting = false;
  fields = new FormFields();
  errors = new FormErrors<FormFields>({
    question: [],
    user_answer: [],
    gpt_marking: [],
  });

  constructor(question: Question, submission: Submission | null) {
    this.question = question;
    this.submission = submission;
    this.fields.question = question.pk;
    this.fields.user_answer = submission?.user_answer ?? '';
  }
}

export default {
  components: { LoadingText, MarkdownContent },
  setup() {
    return { friendlyDuration };
  },

  props: {
    pk: { type: String, required: true },
  },

  data() {
    return {
      loading: true,
      attempt: null as Attempt | null,
      sheet: null as Sheet | null,
      author: null as User | null,
      items: new Array<QuestionItem>(),

      currentTime: 0,
      currentTimeTimeout: null as number | null,

      waiting: false,
    };
  },

  computed: {
    completed(): boolean {
      return this.attempt?.end_time !== null;
    },
    secondsElapsed(): number {
      if (this.attempt === null) return 0;
      return this.currentTime - new Date(this.attempt.begin_time).getTime() / 1000;
    },
    progressLabel(): string {
      if (this.sheet === null) return '';
      return (
        (this.sheet.time_limit >= this.secondsElapsed ? 'Time remaining: ' : 'Time past deadline: ') +
        friendlyDuration(Math.abs(this.sheet.time_limit - this.secondsElapsed))
      );
    },
    progressPercent(): number {
      if (this.sheet === null) return 0;
      return this.sheet.time_limit >= this.secondsElapsed ? this.secondsElapsed / this.sheet.time_limit : 1.0;
    },
  },

  async created() {
    try {
      this.attempt = (await api.get(`main/my_attempt/${this.pk}/`)).data as Attempt;
      this.sheet = (await api.get(`main/sheet/${this.attempt.sheet}/`)).data as Sheet;
      this.author = (await api.get(`accounts/user/${this.sheet.user}/`)).data as User;

      // Retrieve and sort all questions on sheet.
      const sheet_questions = new Array<[number, Question]>();
      for (const { question: pk, index } of this.sheet.sheet_questions) {
        const question = (await api.get(`main/question/${pk}/`)).data as Question;
        sheet_questions.push([index, question]);
      }
      sheet_questions.sort(([i, _], [j, __]) => i - j);

      // Retrieve all submissions made in this attempt.
      const submissions = new Map<number, Submission>();
      for (const { submission: pk } of this.attempt.attempt_submissions) {
        const submission = (await api.get(`main/my_submission/${pk}/`)).data as Submission;
        submissions.set(submission.question, submission);
      }

      // Create QuestionItems.
      for (const [_, question] of sheet_questions) {
        const submission = submissions.get(question.pk) ?? null;
        this.items.push(new QuestionItem(question, submission));
      }

      // Start countdown timer.
      this.currentTime = new Date().getTime() / 1000;
      this.currentTimeTimeout = window.setInterval(() => (this.currentTime = new Date().getTime() / 1000), 1000);
      this.loading = false;
    } catch (e) {
      messageErrors(e);
    }
  },

  unmounted() {
    if (this.currentTimeTimeout !== null) clearTimeout(this.currentTimeTimeout);
  },

  methods: {
    async submit(final: boolean) {
      if (this.attempt === null) return;
      try {
        if (final) this.attempt.end_time = new Date().toISOString();
        this.attempt.attempt_submissions.length = 0;
        for (const item of this.items)
          if (item.submission !== null) {
            this.attempt.attempt_submissions.push({ submission: item.submission.pk });
          }
        this.attempt = (await api.patch(`/main/my_attempt/${this.attempt.pk}/`, this.attempt)).data as Attempt;
      } catch (e) {
        messageErrors(e);
      }
      this.waiting = false;
    },

    async save(item: QuestionItem) {
      try {
        item.errors.clear();
        item.waiting = true;
        item.submission = (await api.post(`main/my_submissions/`, item.fields)).data as Submission;
        await this.submit(false);
        item.modified = false;
      } catch (e) {
        if (axios.isAxiosError(e)) item.errors.decode(e);
        else messageErrors(e);
      }
      item.waiting = false;
    },
  },
};
</script>

<template>
  <div class="ui text container" style="padding: 1em 0">
    <loading-text fill-height :loading="loading">
      <div v-if="sheet">
        <h1 class="ui header">{{ sheet.name }}</h1>
        <div v-if="!completed" style="padding: 1px">
          <sui-progress :label="progressLabel" :percent="progressPercent * 100" active color="primary" />
        </div>
        <div class="ui list">
          <div class="item">
            <i class="hourglass icon" />
            <div class="content">Time limit: {{ friendlyDuration(sheet.time_limit) }}</div>
          </div>
          <div v-if="author !== null" class="item">
            <i class="user icon" />
            <div class="content">Author: {{ author.username }}</div>
          </div>
          <div v-if="sheet.description.length > 0" class="item">
            <i class="book icon" />
            <div class="content">Description: <markdown-content :markdown="sheet.description" /></div>
          </div>
        </div>
        <ol class="ui list">
          <li v-for="item in items" :key="item.question.pk" class="item" style="margin: 1em 0">
            <p>
              <markdown-content display :markdown="item.question.statement" />
            </p>
            <div class="ui form">
              <div class="field" :class="{ error: item.errors.fields.user_answer.length > 0 }">
                <textarea
                  placeholder="Type your answer here..."
                  rows="15"
                  style="resize: vertical"
                  v-model="item.fields.user_answer"
                  @input="
                    item.errors.fields.user_answer.length = 0;
                    item.modified = true;
                  "
                ></textarea>
              </div>
              <button
                class="ui button"
                :class="{ disabled: item.waiting || !item.modified, loading: item.waiting }"
                @click.prevent="save(item)"
              >
                <i v-if="!item.modified" class="check icon" />
                {{ item.modified ? 'Save' : 'Saved' }}
              </button>
            </div>
          </li>
        </ol>
      </div>
    </loading-text>
  </div>
</template>

<style scoped></style>
