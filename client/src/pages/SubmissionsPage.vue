<script lang="ts">
import { api, type Question, type Submission } from '@/api';
import { messageErrors } from '@/state';
import LoadingText from './components/LoadingText.vue';

export default {
  components: { LoadingText },
  data() {
    return {
      loading: true,
      questions: new Map<number, Question>(),
      submissions: new Array<Submission>(),
    };
  },
  async created() {
    try {
      this.submissions = (await api.get('main/my_submissions/')).data as Submission[];
      for (let submission of this.submissions) {
        if (!this.questions.has(submission.question)) {
          this.questions.set(
            submission.question,
            (await api.get(`main/question/${submission.question}/`)).data as Question,
          );
        }
      }
      this.loading = false;
    } catch (e) {
      messageErrors(e);
    }
  },
};
</script>

<template>
  <sui-container text style="padding: 1em 0; min-height: 80vh">
    <loading-text fill-height :loading="loading">
      <sui-header as="h1">My Recent Answers</sui-header>
      <sui-list divided selection size="medium">
        <router-link
          class="ui item"
          v-for="submission in submissions"
          :key="submission.pk"
          :to="`/question/${submission.question}/`"
        >
          <sui-icon name="comments outline" />
          <sui-list-content>
            <sui-list-header>
              [{{ submission.gpt_mark }}/{{ questions.get(submission.question)?.mark_maximum }}]
              {{ submission.user_answer }}
            </sui-list-header>
          </sui-list-content>
        </router-link>
      </sui-list>
    </loading-text>
  </sui-container>
</template>

<style scoped></style>
