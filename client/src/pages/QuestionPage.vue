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
      question: null as Question | null,
      topics: new Array<Topic>(),
    };
  },
  methods: {
    async reload(pk: number) {
      // React to route changes...
      this.modalIsActive = false;
      this.loading = true;
      this.question = null;
      this.topics = [];
      try {
        this.question = (await axios.get(`/main/question/${pk}/`)).data as Question;
        for (const topic_pk of this.question.topics) {
          this.topics.push((await axios.get(`/main/topic/${topic_pk}/`)).data as Topic);
        }
        this.loading = false;
      } catch (error) {
        // TODO
        this.loading = false;
      }
    },
    async submit(e: Event) {
      e.preventDefault();
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

    <p></p>
    <div class="markdown">{{ question?.statement }}</div>
    <p></p>
    <div class="ui divider"></div>

    <form class="ui form">
      <div class="field">
        <label>Answer:</label>
        <textarea
          style="resize: vertical"
          name="user_answer"
          placeholder="Type your answer here..."
          rows="15"
        ></textarea>
      </div>
      <input class="ui button primary" type="submit" value="Check" @click="submit" />
    </form>
  </sui-container>
</template>

<style scoped></style>
