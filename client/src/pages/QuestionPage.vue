<script lang="ts">
import * as constants from '@/constants';
import axios, { AxiosError } from 'axios';
axios.defaults.baseURL = constants.apiRoot;
axios.defaults.withCredentials = true;
axios.defaults.xsrfHeaderName = constants.csrfHeaderName;
axios.defaults.xsrfCookieName = constants.csrfCookieName;

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

type Submission = {
  pk: number;
  user_answer: string;
  gpt_mark: number;
  gpt_comments: string;
  date: string;
};

export default {
  data() {
    return {
      userAnswer: '',
      modalIsActive: false,
      loading: true,
      waiting: false,
      question: null as Question | null,
      submissions: new Array<Submission>(),
      topics: new Array<Topic>(),
    };
  },
  methods: {
    async reload(pk: number) {
      // React to route changes...
      this.userAnswer = '';
      this.modalIsActive = false;
      this.loading = true;
      this.waiting = false;
      this.question = null;
      this.submissions = [];
      this.topics = [];
      try {
        this.question = (await axios.get(`/main/question/${pk}/`)).data as Question;
        this.submissions = (await axios.get(`/main/question/${pk}/submissions/`)).data as Submission[];
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
      if (this.question === null) return;
      this.waiting = true;
      const submission = (
        await axios.post(`/main/question/${this.question.pk}/submissions/`, {
          user_answer: this.userAnswer,
        })
      ).data as Submission;
      this.submissions.unshift(submission);
      // this.$refs.submissions.focus();
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
  <sui-container text style="padding: 1em 0" v-if="question">
    <sui-tab>
      <sui-tab-panel header="Question">
        <div class="markdown" ref="question">
          {{ question.statement }}
        </div>
        <sui-divider />
        <form class="ui form">
          <div class="field">
            <label>Answer:</label>
            <textarea
              style="resize: vertical"
              v-model="userAnswer"
              placeholder="Type your answer here..."
              rows="15"
            ></textarea>
          </div>
          <input class="ui button primary" type="submit" value="Check" @click="submit" />
        </form>
      </sui-tab-panel>
      <sui-tab-panel header="Submissions">
        <sui-list selection verticalAlign="middle">
          <sui-list-item active v-for="submission in submissions" :key="submission.pk">
            <sui-item-content>
              <sui-item-header>
                {{ submission.gpt_mark / question.mark_denominator }} /
                {{ question.mark_maximum / question.mark_denominator }}
              </sui-item-header>
              <!--
                  <sui-item-meta>
                    <span>{{ submission.date }}</span>
                  </sui-item-meta>
                  -->
              <sui-item-description>
                {{ submission.user_answer }}
              </sui-item-description>
            </sui-item-content>
          </sui-list-item>
        </sui-list>
      </sui-tab-panel>
    </sui-tab>
  </sui-container>
</template>

<style scoped></style>
