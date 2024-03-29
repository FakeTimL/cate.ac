<script lang="ts">
import axios from 'axios';
import { api, type Attempt, type Sheet } from '@/api';
import { messageErrors } from '@/state';
import { friendlyDate } from '@/dates';
import { FormErrors } from '@/errors';

import LoadingText from './components/LoadingText.vue';
import MarkdownContent from './components/MarkdownContent.vue';

class FormFields {
  sheet: number | null = null;
  attempt_submissions: { submission: number }[] = [];
}

export default {
  components: { LoadingText, MarkdownContent },
  setup() {
    return { friendlyDate };
  },
  data() {
    return {
      loading: true,
      attempts: new Array<[Attempt, Sheet]>(),

      waiting: false,
      fields: new FormFields(),
      errors: new FormErrors<FormFields>({ sheet: [], attempt_submissions: [] }),
    };
  },
  async created() {
    try {
      const attempts = (await api.get('main/me/attempts/')).data as Attempt[];
      for (const attempt of attempts) {
        const sheet = (await api.get(`main/sheet/${attempt.sheet}/`)).data as Sheet;
        this.attempts.push([attempt, sheet]);
      }
      this.loading = false;
    } catch (e) {
      messageErrors(e);
    }
  },
  methods: {
    async add() {
      try {
        this.errors.clear();
        this.waiting = true;
        const attempt = (await api.post(`main/me/attempts/`, this.fields)).data as Attempt;
        this.$router.push(`/attempt/${attempt.pk}/`);
      } catch (e) {
        if (axios.isAxiosError(e)) this.errors.decode(e);
        else messageErrors(e);
      }
      this.waiting = false;
    },
  },
};
</script>

<template>
  <div class="ui text container" style="padding: 1em 0; min-height: 80vh">
    <loading-text fill-height :loading="loading">
      <h1 class="ui header">My Mock Exams</h1>

      <div class="ui action input" :class="{ error: errors.fields.sheet.length > 0 }">
        <input
          type="number"
          placeholder="Paper number"
          v-model="fields.sheet"
          @input="errors.fields.sheet.length = 0"
        />
        <button class="ui primary button" :class="{ disabled: waiting, loading: waiting }" @click="add">
          <i class="plus icon" />New Attempt
        </button>
      </div>

      <div v-if="errors.all.length > 0" class="ui icon error message">
        <i class="info icon" />
        <div class="content">
          <ul class="ui bulleted list">
            <li v-for="error of errors.all" :key="error" class="item">
              <markdown-content :markdown="error" />
            </li>
          </ul>
        </div>
      </div>

      <div class="ui medium divided selection list">
        <router-link
          v-for="[attempt, sheet] in attempts"
          :key="attempt.pk"
          :to="`/attempt/${attempt.pk}/`"
          class="item"
        >
          <i class="file alternate icon" />
          <div class="content">
            <div class="header">{{ sheet.name }}</div>
            <div class="description">Started {{ friendlyDate(new Date(attempt.begin_time)) }}</div>
          </div>
        </router-link>
      </div>
    </loading-text>
  </div>
</template>

<style scoped></style>
