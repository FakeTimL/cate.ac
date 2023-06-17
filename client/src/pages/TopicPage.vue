<script lang="ts">
import { api, markdownHtml, type Topic, type Question } from '@/api';
import LoadingText from './components/LoadingText.vue';
import MarkdownContent from './components/MarkdownContent.vue';
import { messageError } from '@/messages';

export default {
  components: {
    LoadingText,
    MarkdownContent,
  },
  props: {
    pk: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      modalIsActive: false,
      loading: true,
      topic: null as Topic | null,
      questions: new Array<Question>(),
    };
  },
  async created() {
    try {
      this.topic = (await api.get(`main/topic/${this.pk}/`)).data as Topic;
      for (const questions_pk of this.topic.questions) {
        this.questions.push((await api.get(`main/question/${questions_pk}/`)).data as Question);
      }
      this.topic.resources = await markdownHtml(this.topic.resources);
      this.loading = false;
    } catch (e) {
      messageError(e);
    }
  },
};
</script>

<template>
  <sui-container text style="padding: 1em 0; min-height: 80vh">
    <loading-text fill-height :loading="loading">
      <div v-if="topic">
        <sui-header as="h1">{{ topic.name }}</sui-header>
        <sui-list divided selection size="medium">
          <sui-list-item @click="modalIsActive = true">
            <sui-icon name="info circle" />
            <sui-list-content>
              <sui-list-header>What is this topic about?</sui-list-header>
            </sui-list-content>
          </sui-list-item>
          <router-link
            class="ui item"
            v-for="question in questions"
            :key="question.pk"
            :to="`/question/${question.pk}/`"
          >
            <sui-icon name="question circle outline" />
            <sui-list-content>
              <sui-list-header> {{ question.statement.substring(0, 50) }}... </sui-list-header>
            </sui-list-content>
          </router-link>
        </sui-list>
      </div>
    </loading-text>
  </sui-container>
  <sui-modal v-if="topic" size="small" v-model="modalIsActive">
    <sui-header>What this topic is about?</sui-header>
    <sui-modal-content scrolling>
      <markdown-content :html="topic.resources" />
    </sui-modal-content>
  </sui-modal>
</template>

<style scoped></style>
