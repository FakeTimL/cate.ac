<script lang="ts">
import { type Topic } from '@/api';
import LoadingText from './LoadingText.vue';
import MarkdownContent from './MarkdownContent.vue';

export default {
  components: {
    LoadingText,
    MarkdownContent,
  },
  props: {
    question: {
      type: Object, // Question
      required: true,
    },
    topics: {
      type: Array<Topic>,
      required: true,
    },
    submission: {
      type: Object, // Submission
      required: true,
    },
  },
};
</script>

<template>
  <h2>
    Score:
    {{ submission.gpt_mark === null ? '-' : (submission.gpt_mark / question.mark_denominator).toString() }}
    / {{ (question.mark_maximum / question.mark_denominator).toString() }}
  </h2>
  <h4>Your answer:</h4>
  <p>{{ submission.user_answer }}</p>
  <loading-text :length="1" :loading="submission.gpt_mark === null" text="ChatGPT is grading...">
    <div class="ui info message">
      <h4>Comments:</h4>
      <p>{{ submission.gpt_comments }}</p>
      <details>
        <summary>Mark scheme:</summary>
        <blockquote>
          <markdown-content display :markdown="question.mark_scheme" />
        </blockquote>
      </details>
    </div>
    <p>
      <span>Topics:</span>
      <router-link v-for="topic in topics" :key="topic.pk" :to="`/topic/${topic.pk}/`" class="ui label">
        {{ topic.name }}
      </router-link>
    </p>
  </loading-text>
</template>

<style scoped></style>
