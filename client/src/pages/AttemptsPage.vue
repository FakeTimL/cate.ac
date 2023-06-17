<script lang="ts">
import { api, type Attempt, type Sheet } from '@/api';
import LoadingText from './components/LoadingText.vue';
import { messageError } from '@/messages';
import { friendlyDate } from '@/dates';

export default {
  components: { LoadingText },
  setup() {
    return { friendlyDate };
  },
  data() {
    return {
      loading: true,
      attempts: new Array<[Attempt, Sheet | null]>(),
    };
  },
  async created() {
    try {
      const attempts = (await api.get('main/my_attempts/')).data as Attempt[];
      for (const attempt of attempts) {
        let sheet: Sheet | null = null;
        if (attempt.sheet !== null) {
          sheet = (await api.get(`main/sheet/${attempt.sheet}/`)).data as Sheet;
        }
        this.attempts.push([attempt, sheet]);
      }
      this.loading = false;
    } catch (e) {
      messageError(e);
    }
  },
};
</script>

<template>
  <div class="ui text container" style="padding: 1em 0; min-height: 80vh">
    <loading-text fill-height :loading="loading">
      <h1 class="ui header">My Recent Mock Exams</h1>
      <div class="ui medium divided selection list">
        <router-link
          v-for="[attempt, sheet] in attempts"
          :key="attempt.pk"
          :to="`/attempt/${attempt.pk}/`"
          class="item"
        >
          <i class="pencil alternate icon" />
          <div class="content">
            <div class="header">{{ sheet !== null ? sheet.name : '(Custom practice)' }}</div>
            <div class="description">Started {{ friendlyDate(new Date(attempt.begin_time)) }}</div>
          </div>
        </router-link>
      </div>
    </loading-text>
  </div>
</template>

<style scoped></style>
