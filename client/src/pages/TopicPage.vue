<script lang="ts">
import * as constants from '@/constants';
import axios, { AxiosError } from 'axios';
axios.defaults.baseURL = constants.apiRoot;

type Topic = {
  pk: number;
  name: string;
  parent: number | null;
  children: number[];
  questions: number[];
  resources: string;
};

type Question = {
  pk: number;
  statement: string;
  mark_denominator: number;
  mark_minimum: number;
  mark_maximum: number;
  mark_scheme: string;
  gpt_prompt: string;
  topics: number[];
};

export default {
  data() {
    return {
      modalIsActive: false,
      loading: true,
      topic: null as Topic | null,
      questions: new Array<Question>(),
    };
  },
  methods: {
    async reload(pk: number) {
      // React to route changes...
      this.modalIsActive = false;
      this.loading = true;
      this.topic = null;
      this.questions = [];
      try {
        this.topic = (await axios.get(`/main/topic/${pk}/`)).data as Topic;
        for (const questions_pk of this.topic.questions) {
          this.questions.push((await axios.get(`/main/question/${questions_pk}/`)).data as Question);
        }
        this.loading = false;
      } catch (error) {
        // TODO
        this.loading = false;
      }
    },
  },
  created() {
    // See: https://router.vuejs.org/guide/essentials/dynamic-matching.html
    this.reload(parseInt(this.$route.params.pk as string));
    this.$watch(
      () => this.$route.params,
      async (newParams, oldParams) => this.reload(parseInt(newParams.pk as string)),
    );
  },
};
</script>

<template>
  <sui-container text style="padding: 1em 0">
    <sui-header as="h1">{{ topic?.name }}</sui-header>
    <div class="ui placeholder" v-if="loading">
      <div class="image header">
        <div class="line"></div>
        <div class="line"></div>
      </div>
      <div class="paragraph">
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
      </div>
      <div class="image header">
        <div class="line"></div>
        <div class="line"></div>
      </div>
      <div class="paragraph">
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
      </div>
      <div class="image header">
        <div class="line"></div>
        <div class="line"></div>
      </div>
      <div class="paragraph">
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
      </div>
    </div>
    <sui-list divided selection size="medium" v-if="!loading">
      <sui-list-item @click="modalIsActive = true">
        <sui-icon name="info circle" />
        <sui-list-content>
          <sui-list-header>What is this topic about?</sui-list-header>
        </sui-list-content>
      </sui-list-item>
      <router-link class="ui item" v-for="question in questions" :key="question.pk" :to="`/question/${question.pk}/`">
        <sui-icon name="question circle outline" />
        <sui-list-content>
          <sui-list-header>{{ question.statement.substring(0, 50) }}...</sui-list-header>
        </sui-list-content>
      </router-link>
    </sui-list>
  </sui-container>
  <sui-modal v-model="modalIsActive">
    <sui-header as="h1">What is this topic about?</sui-header>
    <sui-modal-content><div v-html="topic?.resources"></div></sui-modal-content>
  </sui-modal>
</template>

<style scoped></style>
