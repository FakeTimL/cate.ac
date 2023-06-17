<script lang="ts">
import type { Sheet, Attempt, Question, User, Submission } from '@/api';
import { api } from '@/api';
import { messageErrors } from '@/messages';
import { friendlyDuration } from '@/dates';

import LoadingText from './components/LoadingText.vue';
import MarkdownContent from './components/MarkdownContent.vue';

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
      questions: new Array<Question>(),
      submissions: new Map<number, Submission>(),

      currentTime: 0,
      currentTimeTimeout: null as number | null,
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
      const sheet_questions = new Array<[number, Question]>();
      for (const { question: pk, index } of this.sheet.sheet_questions) {
        const question = (await api.get(`main/question/${pk}/`)).data as Question;
        sheet_questions.push([index, question]);
      }
      for (const pk of this.attempt.submissions) {
        const submission = (await api.get(`main/my_submission/${pk}/`)).data as Submission;
        this.submissions.set(submission.question, submission);
      }
      sheet_questions.sort(([i, _], [j, __]) => i - j);
      for (const [_, question] of sheet_questions) this.questions.push(question);
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
          <li v-for="question in questions" :key="question.pk" class="item" style="margin: 1em 0">
            <p>
              <markdown-content display :markdown="question.statement" />
            </p>
            <sui-form>
              <sui-form-field>
                <textarea placeholder="Type your answer here..." rows="15" style="resize: vertical"></textarea>
              </sui-form-field>
            </sui-form>
          </li>
        </ol>
      </div>
    </loading-text>
  </div>
</template>

<style scoped></style>
