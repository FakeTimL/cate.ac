<script lang="ts">
import { api, markdownHtml, type Topic, type Question, type Submission } from '@/api';
import { friendlyDate } from '@/dates';
import LoadingCircle from './components/LoadingCircle.vue';
import MarkdownContent from './components/MarkdownContent.vue';

export default {
  components: {
    LoadingCircle,
    MarkdownContent,
  },
  setup() {
    return { friendlyDate };
  },
  props: {
    pk: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      tabIndex: 0,
      submissionIndex: null as number | null,
      userAnswer: '',
      modalIsActive: false,
      loading: true,
      waiting: false,
      question: null as Question | null,
      submissions: new Array<Submission>(),
      topics: new Array<Topic>(),
    };
  },
  async created() {
    try {
      this.question = (await api.get(`main/question/${this.pk}/`)).data as Question;
      this.submissions = (await api.get(`main/question/${this.pk}/my_submissions/`)).data as Submission[];
      for (const topic_pk of this.question.topics) {
        this.topics.push((await api.get(`main/topic/${topic_pk}/`)).data as Topic);
      }
      this.question.statement = await markdownHtml(this.question.statement);
      this.question.mark_scheme = await markdownHtml(this.question.mark_scheme);
      this.loading = false;
    } catch (error) {
      // TODO
      this.loading = false;
    }
  },
  methods: {
    async submit(e: Event) {
      e.preventDefault();
      if (this.question === null) return;
      this.waiting = true;
      const submission = (
        await api.post(`main/question/${this.question.pk}/my_submissions/`, {
          user_answer: this.userAnswer,
        })
      ).data as Submission;
      this.submissions.unshift(submission);
      this.tabIndex = 1;
      this.submissionIndex = 0;
    },
  },
};
</script>

<template>
  <sui-container text style="padding: 1em 0; min-height: 80vh">
    <loading-circle fill-height :loading="loading">
      <div v-if="question">
        <sui-tab v-model:activeIndex="tabIndex">
          <sui-tab-panel header="Question">
            <markdown-content :html="question.statement" />
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
          <sui-tab-panel header="My submissions">
            <sui-list selection>
              <sui-list-item
                v-for="(submission, index) in submissions"
                :key="submission.pk"
                :active="index === submissionIndex"
                @click="submissionIndex = index"
              >
                <sui-list-header>
                  Score:
                  {{ submission.gpt_mark / question.mark_denominator }} /
                  {{ question.mark_maximum / question.mark_denominator }}
                </sui-list-header>
                <span>Answered {{ friendlyDate(new Date(submission.date)) }}</span>
              </sui-list-item>
            </sui-list>
            <div v-if="submissionIndex !== null && submissions[submissionIndex]">
              <sui-divider />
              <h2>
                Score:
                {{ submissions[submissionIndex].gpt_mark / question.mark_denominator }} /
                {{ question.mark_maximum / question.mark_denominator }}
              </h2>
              <h4>Your answer:</h4>
              <p>{{ submissions[submissionIndex].user_answer }}</p>
              <div class="ui info message">
                <h4>Comments:</h4>
                <p>{{ submissions[submissionIndex].gpt_comments }}</p>
                <details>
                  <summary>Mark scheme:</summary>
                  <blockquote>
                    <markdown-content :html="question.mark_scheme" />
                  </blockquote>
                </details>
              </div>
              <p>
                <span>Topics:</span>
                <router-link v-for="topic in topics" :key="topic.pk" :to="`/topic/${topic.pk}/`" class="ui label">
                  {{ topic.name }}
                </router-link>
              </p>
            </div>
          </sui-tab-panel>
        </sui-tab>
      </div>
    </loading-circle>
  </sui-container>
</template>

<style scoped></style>
