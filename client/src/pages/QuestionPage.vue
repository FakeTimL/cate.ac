<script lang="ts">
import { api, markdownHtml, type Topic, type Question, type Submission } from '@/api';
import { FormErrors } from '@/forms';
import { friendlyDate } from '@/dates';
import axios from 'axios';

import LoadingCircle from './components/LoadingCircle.vue';
import MarkdownContent from './components/MarkdownContent.vue';
import SubmissionDetail from './components/SubmissionDetail.vue';

class FormFields {
  user_answer: string = '';
}

export default {
  components: {
    LoadingCircle,
    MarkdownContent,
    SubmissionDetail,
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
      loading: true,
      question: null as Question | null,
      topics: new Array<Topic>(),
      submissions: new Array<Submission>(),
      timeout: null as number | null,

      tabIndex: 0,
      submissionIndex: null as number | null,

      waiting: false,
      fields: new FormFields(),
      errors: new FormErrors<FormFields>({
        user_answer: [],
      }),
    };
  },
  async created() {
    try {
      this.question = (await api.get(`main/question/${this.pk}/`)).data as Question;
      this.question.statement = await markdownHtml(this.question.statement);
      this.question.mark_scheme = await markdownHtml(this.question.mark_scheme);
      for (const topic_pk of this.question.topics) {
        this.topics.push((await api.get(`main/topic/${topic_pk}/`)).data as Topic);
      }
    } catch (error) {
      // TODO
    }
    await this.refreshSubmissions();
    this.loading = false;
  },
  unmounted() {
    if (this.timeout !== null) {
      // Clear pending refresh tasks.
      clearTimeout(this.timeout);
    }
  },
  methods: {
    async refreshSubmissions() {
      try {
        this.submissions = (await api.get(`main/question/${this.pk}/my_submissions/`)).data as Submission[];
      } catch (error) {
        // TODO
      }
      let refreshRequired = false;
      for (const submission of this.submissions)
        if (submission.gpt_mark === null) {
          refreshRequired = true;
          break;
        }
      if (refreshRequired) {
        // Refresh after 5 seconds.
        this.timeout = setTimeout(this.refreshSubmissions, 5000);
      }
    },
    async submit(e: Event) {
      e.preventDefault();
      if (this.question === null) return;
      this.errors.clear();
      if (this.fields.user_answer == '') this.errors.fields.user_answer.push('Please write something...');
      if (this.errors.all.length > 0) return;
      this.waiting = true;
      try {
        const submission = (await api.post(`main/question/${this.question.pk}/my_submissions/`, this.fields))
          .data as Submission;
        this.submissions.unshift(submission);
        this.tabIndex = 1;
        this.submissionIndex = 0;
        // Refresh after 5 seconds.
        this.timeout = setTimeout(this.refreshSubmissions, 5000);
      } catch (e) {
        if (axios.isAxiosError(e)) this.errors.decode(e);
        else throw e;
      }
      this.waiting = false;
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

            <sui-form>
              <sui-form-field :error="errors.fields.user_answer.length > 0">
                <label>Answer:</label>
                <textarea
                  placeholder="Type your answer here..."
                  rows="15"
                  style="resize: vertical"
                  v-model="fields.user_answer"
                  @input="errors.fields.user_answer.length = 0"
                ></textarea>
              </sui-form-field>
              <sui-button primary @click="submit">Check</sui-button>
            </sui-form>

            <sui-message v-if="errors.all.length > 0" icon error>
              <sui-icon name="info" />
              <sui-message-content>
                <sui-list bulleted>
                  <sui-list-item v-for="error of errors.all" :key="error">{{ error }}</sui-list-item>
                </sui-list>
              </sui-message-content>
            </sui-message>
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
                  {{
                    submission.gpt_mark === null ? '-' : (submission.gpt_mark / question.mark_denominator).toString()
                  }}
                  / {{ (question.mark_maximum / question.mark_denominator).toString() }}
                </sui-list-header>
                <span>Answered {{ friendlyDate(new Date(submission.date)) }}</span>
              </sui-list-item>
            </sui-list>

            <div v-if="submissionIndex !== null && submissions[submissionIndex]">
              <sui-divider />
              <submission-detail :question="question" :topics="topics" :submission="submissions[submissionIndex]" />
            </div>
          </sui-tab-panel>
        </sui-tab>
      </div>
    </loading-circle>

    <sui-dimmer :active="waiting">
      <sui-loader />
    </sui-dimmer>
  </sui-container>
</template>

<style scoped></style>
