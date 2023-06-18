<script lang="ts">
import type { Sheet, Attempt, Question, User, Submission, Topic } from '@/api';
import axios from 'axios';
import { api } from '@/api';
import { messageErrors } from '@/state';
import { friendlyDuration } from '@/dates';
import { FormErrors } from '@/errors';

import LoadingText from './components/LoadingText.vue';
import MarkdownContent from './components/MarkdownContent.vue';
import SubmissionDetail from './components/SubmissionDetail.vue';

class FormFields {
  question: number | null = null;
  user_answer: string = '';
  gpt_marking: boolean = false;
}

class QuestionItem {
  question: Question;
  topics: Topic[];
  submission = null as Submission | null;

  modified = false;
  waiting = false;
  fields = new FormFields();
  errors = new FormErrors<FormFields>({ question: [], user_answer: [], gpt_marking: [] });

  constructor(question: Question, topics: Topic[], submission: Submission | null) {
    this.question = question;
    this.topics = topics;
    this.submission = submission;
    this.fields.question = question.pk;
    this.fields.user_answer = submission?.user_answer ?? '';
  }
}

export default {
  components: { LoadingText, MarkdownContent, SubmissionDetail },
  setup() {
    return { friendlyDuration };
  },

  props: {
    pk: { type: String, required: true },
  },

  data() {
    return {
      loading: true,
      reloadTimeout: null as number | null,
      attempt: null as Attempt | null,
      sheet: null as Sheet | null,
      author: null as User | null,
      items: null as QuestionItem[] | null,

      currentTime: 0,
      currentTimeInterval: null as number | null,

      waiting: false,

      total: 0,
      marked: 0,
      totalMarks: 0,
      userMarksLow: 0,
      userMarksHigh: 0,
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

    markingCompleted(): boolean {
      return this.marked == this.total;
    },

    markingLabel(): string {
      return this.total == this.marked
        ? 'Grading finished!'
        : `${this.marked.toString()} / ${this.total.toString()} questions graded...`;
    },

    markingPercent(): number {
      return this.marked / this.total;
    },

    markingRange(): string {
      return this.total == this.marked
        ? this.userMarksHigh.toString()
        : `(${this.userMarksLow.toString()} ~ ${this.userMarksHigh.toString()})`;
    },
  },

  async created() {
    try {
      this.attempt = (await api.get(`main/me/attempt/${this.pk}/`)).data as Attempt;
      this.sheet = (await api.get(`main/sheet/${this.attempt.sheet}/`)).data as Sheet;
      this.author = (await api.get(`accounts/user/${this.sheet.user}/`)).data as User;

      // Retrieve and sort all questions on sheet.
      const sheet_questions = new Array<[number, Question]>();
      for (const { question: pk, index } of this.sheet.sheet_questions) {
        sheet_questions.push([index, (await api.get(`main/question/${pk}/`)).data as Question]);
      }
      sheet_questions.sort(([i, _], [j, __]) => i - j);

      // Retrieve all submissions made in this attempt.
      const submissions = new Map<number, Submission>();
      for (const { submission: pk } of this.attempt.attempt_submissions) {
        const submission = (await api.get(`main/me/submission/${pk}/`)).data as Submission;
        submissions.set(submission.question, submission);
      }

      // Retrieve all topics and create QuestionItems.
      this.items = [];
      for (const [_, question] of sheet_questions) {
        const submission = submissions.get(question.pk) ?? null;
        const topics = new Array<Topic>();
        for (const pk of question.topics) {
          topics.push((await api.get(`main/topic/${pk}/`)).data as Topic);
        }
        this.items.push(new QuestionItem(question, topics, submission));
      }

      // Start countdown timer.
      this.currentTime = new Date().getTime() / 1000;
      this.currentTimeInterval = window.setInterval(() => (this.currentTime = new Date().getTime() / 1000), 1000);

      await this.reload();
    } catch (e) {
      messageErrors(e);
    }
  },

  unmounted() {
    if (this.reloadTimeout !== null) clearTimeout(this.reloadTimeout);
    if (this.currentTimeInterval !== null) clearInterval(this.currentTimeInterval);
  },

  methods: {
    // Refresh submissions.
    async reload() {
      if (this.items === null) return;
      try {
        for (const item of this.items)
          if (item.submission !== null) {
            item.submission = (await api.get(`main/me/submission/${item.submission.pk}/`)).data as Submission;
          }

        // Calculate total marks.
        if (this.completed) {
          this.total = 0;
          this.marked = 0;
          this.totalMarks = 0;
          this.userMarksLow = 0;
          this.userMarksHigh = 0;

          for (const item of this.items) {
            this.total++;
            this.totalMarks += item.question.mark_maximum / item.question.mark_denominator;

            if (item.submission === null) {
              this.marked++;
            } else if (item.submission.gpt_mark !== null) {
              this.marked++;
              this.userMarksLow += item.submission.gpt_mark / item.question.mark_denominator;
              this.userMarksHigh += item.submission.gpt_mark / item.question.mark_denominator;
            } else {
              this.userMarksHigh += item.question.mark_maximum / item.question.mark_denominator;
            }
          }

          // Check if grading is in progress.
          if (this.items.reduce((acc, item) => acc || (item.submission?.gpt_marking ?? false), false))
            this.reloadTimeout = setTimeout(this.reload, 1000);
        }

        this.loading = false;
      } catch (e) {
        messageErrors(e);
      }
    },

    async saveAttempt(final: boolean) {
      if (this.attempt === null || this.items === null) return;
      try {
        if (final) this.attempt.end_time = new Date().toISOString();
        this.attempt.attempt_submissions.length = 0;
        for (const item of this.items)
          if (item.submission !== null) {
            this.attempt.attempt_submissions.push({ submission: item.submission.pk });
          }
        this.attempt = (await api.patch(`main/me/attempt/${this.attempt.pk}/`, this.attempt)).data as Attempt;
      } catch (e) {
        messageErrors(e);
      }
    },

    async saveItem(item: QuestionItem) {
      try {
        item.errors.clear();
        item.waiting = true;
        if (item.submission !== null) {
          item.submission = (await api.patch(`main/me/submission/${item.submission.pk}/`, item.fields))
            .data as Submission;
        } else {
          item.submission = (await api.post(`main/me/submissions/`, item.fields)).data as Submission;
          await this.saveAttempt(false);
        }
        item.modified = false;
      } catch (e) {
        if (axios.isAxiosError(e)) item.errors.decode(e);
        else messageErrors(e);
      }
      item.waiting = false;
    },

    async submit() {
      if (this.items === null) return;
      try {
        this.waiting = true;
        for (const item of this.items) await this.saveItem(item);
        await this.saveAttempt(true);
        await this.reload();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } catch (e) {
        messageErrors(e);
      }
      this.waiting = false;
    },
  },
};
</script>

<template>
  <div class="ui text container" style="padding: 1em 0">
    <loading-text fill-height :loading="loading">
      <div v-if="attempt !== null && sheet !== null && author !== null && items !== null">
        <h1 class="ui header">{{ sheet.name }}</h1>

        <div v-if="!completed" style="padding: 1px">
          <sui-progress :label="progressLabel" :percent="progressPercent * 100" active color="primary" />
        </div>

        <div v-if="completed" style="padding: 1px">
          <sui-progress :label="markingLabel" :percent="markingPercent * 100" :active="!markingCompleted" indicating />
        </div>
        <div v-if="completed" class="ui raised piled segment" style="margin: 1em; text-align: center">
          <h1 class="ui header" style="transition: opacity 0.5s" :style="{ opacity: markingPercent }">
            Total marks: {{ markingRange }} / {{ totalMarks }}
          </h1>
          <!-- Please keep it rounded up. -->
          <div class="ui yellow star huge disabled rating">
            <i
              v-for="n in 5"
              :key="n"
              class="star icon"
              :class="{ active: n <= Math.ceil((userMarksLow / totalMarks) * 5) }"
            />
          </div>
        </div>

        <div class="ui list">
          <div class="item">
            <i class="hourglass icon" />
            <div class="content">Time limit: {{ friendlyDuration(sheet.time_limit) }}</div>
          </div>
          <div class="item">
            <i class="user icon" />
            <div class="content">Author: {{ author.username }}</div>
          </div>
          <div v-if="sheet.description.length > 0" class="item">
            <i class="book icon" />
            <div class="content"><markdown-content :markdown="sheet.description" /></div>
          </div>
        </div>

        <div class="ui divider" />

        <ol class="ui list">
          <li v-for="item in items" :key="item.question.pk" class="item" style="margin: 1em 0">
            <markdown-content display :markdown="item.question.statement" />

            <div v-if="!completed" class="ui form" style="margin-top: 1em">
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
                @click.prevent="saveItem(item)"
              >
                <i v-if="!item.modified" class="check icon" />
                {{ item.modified ? 'Save' : 'Saved' }}
              </button>
            </div>

            <div v-else class="ui piled segment" style="margin: 1.5em 0">
              <submission-detail
                :question="item.question"
                :topics="item.topics ?? undefined"
                :submission="item.submission ?? undefined"
              />
            </div>

            <router-link v-if="completed" :to="`/conversation/${author.pk}/`" class="ui primary button">
              <i class="question icon" />
              Ask Question
            </router-link>
          </li>
        </ol>

        <button
          class="ui primary button"
          :class="{ disabled: waiting || completed, loading: waiting }"
          @click.prevent="submit"
        >
          <i v-if="completed" class="check icon" />
          {{ completed ? 'Answers Confirmed & Submitted' : 'Confirm Answers & Submit' }}
        </button>
      </div>
    </loading-text>
  </div>
</template>

<style scoped></style>
