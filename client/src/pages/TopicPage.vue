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
  <div class="ui text container" style="padding: 1em 0; min-height: 80vh">
    <loading-text fill-height :loading="loading">
      <div v-if="topic">
        <h1 class="ui header">{{ topic.name }}</h1>
        <div class="ui medium divided selection list">
          <div class="item" @click="modalIsActive = true">
            <i class="info circle icon" />
            <div class="content">
              <div class="header">What is this topic about?</div>
            </div>
          </div>
          <router-link v-for="question in questions" :key="question.pk" :to="`/question/${question.pk}/`" class="item">
            <i class="question circle outline icon" />
            <div class="content">
              <div class="header">{{ question.statement.substring(0, 50) }}...</div>
            </div>
          </router-link>
        </div>
      </div>
    </loading-text>
  </div>
  <sui-modal v-if="topic" size="small" v-model="modalIsActive">
    <div class="header">What this topic is about?</div>
    <div class="content scrolling">
      <markdown-content :html="topic.resources" />
    </div>
  </sui-modal>
</template>

<style scoped></style>
