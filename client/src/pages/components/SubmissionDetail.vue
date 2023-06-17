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
      required: false,
    },
    submission: {
      type: Object, // Submission
      required: false,
    },
  },
};
</script>

<template>
  <div v-if="submission !== undefined">
    <h2>
      Your marks:
      {{ submission.gpt_mark === null ? '-' : (submission.gpt_mark / question.mark_denominator).toString() }}
      / {{ (question.mark_maximum / question.mark_denominator).toString() }}
    </h2>

    <h4>Your answer:</h4>
    <p>{{ submission.user_answer }}</p>

    <loading-text :length="1" :loading="submission.gpt_marking" text="ChatGPT is grading...">
      <div v-if="submission.gpt_mark !== null" class="ui info message">
        <h4>Comments:</h4>
        <p>{{ submission.gpt_comments }}</p>
        <details>
          <summary>Mark scheme:</summary>
          <blockquote>
            <markdown-content display :markdown="question.mark_scheme" />
          </blockquote>
        </details>
      </div>

      <p v-if="topics !== undefined">
        <span>Topics:</span>
        <router-link v-for="topic in topics" :key="topic.pk" :to="`/topic/${topic.pk}/`" class="ui label">
          {{ topic.name }}
        </router-link>
      </p>
    </loading-text>
  </div>

  <div v-else>
    <h2>Your marks: 0 / {{ (question.mark_maximum / question.mark_denominator).toString() }}</h2>
    <h4>You did not attempt this question.</h4>
  </div>
</template>

<style scoped></style>
