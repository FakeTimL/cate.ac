<script lang="ts">
import { api, type Submission } from '@/api';
import LoadingText from './components/LoadingText.vue';

export default {
  components: { LoadingText },
  data() {
    return {
      loading: true,
      submissions: new Array<Submission>(),
    };
  },
  async created() {
    try {
      this.submissions = (await api.get('main/my_submissions/')).data as Submission[];
      this.loading = false;
    } catch (error) {
      // TODO
      this.loading = false;
    }
  },
};
</script>

<template>
  <sui-container text style="padding: 1em 0; min-height: 80vh">
    <loading-text fill-height :loading="loading">
      <sui-header as="h1">My past answers</sui-header>
      <sui-list divided selection size="medium">
        <router-link
          class="ui item"
          v-for="submission in submissions"
          :key="submission.pk"
          :to="`/question/${submission.question}/`"
        >
          <sui-icon name="comments outline" />
          <sui-list-content>
            {{ submission.user_answer }}
          </sui-list-content>
        </router-link>
      </sui-list>
    </loading-text>
  </sui-container>
</template>

<style scoped></style>
