<script lang="ts">
import { api } from '@/api';
import { AxiosError } from 'axios';

function is<T>(value: T): T {
  return value;
}

type FormData = {
  text: string;
  email: string;
};

type FormError = Partial<Record<keyof FormData, string[]>>;

export default {
  data() {
    return {
      success: false,
      waiting: false,
      fields: {
        text: '',
        email: '',
      },
      fieldErrors: is<FormError>({}),
      otherErrors: is<string[]>([]),
    };
  },
  computed: {
    errorList(): string[] {
      return Object.entries(this.fieldErrors)
        .reduce((acc, x) => acc.concat(x[1]), is<string[]>([]))
        .concat(this.otherErrors);
    },
  },
  methods: {
    async submit(e: Event) {
      e.preventDefault();
      this.success = false;
      this.fieldErrors = {};
      this.otherErrors = [];
      if (this.fields.text == '') (this.fieldErrors.text ??= []).push('Please write something...');
      if (this.errorList.length) return;
      this.waiting = true;
      try {
        await api.post('main/feedbacks/', this.fields);
        this.success = true;
      } catch (e) {
        if (e instanceof AxiosError) {
          if (e.response !== undefined) {
            this.fieldErrors = e.response.data;
            if (e.response.data['detail']) this.otherErrors.push(String(e.response.data['detail']));
            if (e.response.data['non_field_errors']) this.otherErrors.push(String(e.response.data['non_field_errors']));
          } else {
            this.otherErrors.push(e.message);
          }
        } else {
          throw e;
        }
      }
      this.waiting = false;
    },
  },
};
</script>

<template>
  <sui-container text style="padding: 1em 0; min-height: 80vh">
    <sui-header as="h1">Send Anonymous Feedback</sui-header>
    <sui-form>
      <sui-form-field :error="Boolean(fieldErrors.text)">
        <label>Describe any problem or your ideas for improvement:</label>
        <textarea
          placeholder="Any idea is appreciated..."
          rows="20"
          style="resize: vertical"
          v-model="fields.text"
          @input="delete fieldErrors.text"
        ></textarea>
      </sui-form-field>
      <sui-form-field :error="Boolean(fieldErrors.email)">
        <label>Email (optional)</label>
        <input
          placeholder="If you want follow-up discussions..."
          v-model="fields.email"
          @input="delete fieldErrors.email"
        />
      </sui-form-field>
      <sui-button primary @click="submit">Send</sui-button>
    </sui-form>
    <sui-message v-if="success" icon positive>
      <p>Your feedback has been sent. Thank you so much!</p>
    </sui-message>
    <sui-message v-if="errorList.length" icon error>
      <sui-icon name="info" />
      <sui-message-content>
        <sui-list bulleted>
          <sui-list-item v-for="error of errorList" :key="error">{{ error }}</sui-list-item>
        </sui-list>
      </sui-message-content>
    </sui-message>
    <sui-dimmer :active="waiting">
      <sui-loader />
    </sui-dimmer>
  </sui-container>
</template>
