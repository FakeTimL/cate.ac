<script lang="ts">
import { api, type Topic, type Question, type Submission } from '@/api';
import { FormErrors } from '@/errors';
import { friendlyDate } from '@/dates';
import axios from 'axios';

import LoadingCircle from './components/LoadingCircle.vue';
import MarkdownContent from './components/MarkdownContent.vue';
import SubmissionDetail from './components/SubmissionDetail.vue';
import { messageErrors } from '@/messages';

class FormFields {
  question: number | null = null;
  user_answer: string = '';
  gpt_marking: boolean = true;
}

export default {
  components: { LoadingCircle, MarkdownContent, SubmissionDetail },
  setup() {
    return { friendlyDate };
  },
  props: {
    pk: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      loading: true,
      reloadTimeout: null as number | null,
      question: null as Question | null,
      topics: new Array<Topic>(),
      submissions: new Array<Submission>(),

      tabIndex: 0,
      submissionIndex: null as number | null,

      waiting: false,
      fields: new FormFields(),
      errors: new FormErrors<FormFields>({ question: [], user_answer: [], gpt_marking: [] }),
    };
  },

  async created() {
    try {
      this.question = (await api.get(`main/question/${this.pk}/`)).data as Question;
      this.fields.question = this.question.pk;
      for (const topic_pk of this.question.topics) {
        this.topics.push((await api.get(`main/topic/${topic_pk}/`)).data as Topic);
      }
      await this.reload();
    } catch (e) {
      messageErrors(e);
    }
  },

  unmounted() {
    if (this.reloadTimeout !== null) clearTimeout(this.reloadTimeout);
  },

  methods: {
    // Refresh submissions.
    async reload() {
      try {
        this.submissions = (await api.get(`main/question/${this.pk}/my_submissions/`)).data as Submission[];
        if (this.submissions.reduce((acc, submission) => acc || submission.gpt_marking, false))
          this.reloadTimeout = setTimeout(this.reload, 1000);
        this.loading = false;
      } catch (e) {
        messageErrors(e);
      }
    },

    async submit() {
      if (this.question === null) return;
      try {
        this.errors.clear();
        this.waiting = true;
        await api.post(`main/my_submissions/`, this.fields);
        await this.reload();
        this.tabIndex = 1;
        this.submissionIndex = 0;
      } catch (e) {
        if (axios.isAxiosError(e)) this.errors.decode(e);
        else messageErrors(e);
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
            <markdown-content display :markdown="question.statement" />
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
              <sui-button primary :disabled="waiting" :loading="waiting" @click.prevent="submit">Check</sui-button>
            </sui-form>

            <sui-message v-if="errors.all.length > 0" icon error>
              <sui-icon name="info" />
              <sui-message-content>
                <sui-list bulleted>
                  <sui-list-item v-for="error of errors.all" :key="error">
                    <markdown-content :markdown="error" />
                  </sui-list-item>
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
                  Your marks:
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
  </sui-container>
</template>

<style scoped></style>
