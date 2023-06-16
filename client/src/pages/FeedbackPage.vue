<script lang="ts">
import { api } from '@/api';
import { FormErrors } from '@/forms';
import axios from 'axios';

class FormFields {
  text: string = '';
  email: string = '';
}

export default {
  data() {
    return {
      success: false,
      waiting: false,
      fields: new FormFields(),
      errors: new FormErrors<FormFields>({
        text: [],
        email: [],
      }),
    };
  },
  methods: {
    async submit(e: Event) {
      e.preventDefault();
      this.success = false;
      this.errors.clear();
      if (this.fields.text == '') this.errors.fields.text.push('Please write something...');
      if (this.errors.all.length > 0) return;
      this.waiting = true;
      try {
        await api.post('main/feedbacks/', this.fields);
        this.success = true;
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
    <sui-header as="h1">Send Anonymous Feedback</sui-header>
    <sui-form>
      <sui-form-field :error="errors.fields.text.length > 0">
        <label>Describe any problem or your ideas for improvement:</label>
        <textarea
          placeholder="Any idea is appreciated..."
          rows="20"
          style="resize: vertical"
          v-model="fields.text"
          @input="errors.fields.text.length = 0"
        ></textarea>
      </sui-form-field>

      <sui-form-field :error="errors.fields.email.length > 0">
        <label>Email (optional)</label>
        <input
          placeholder="If you want follow-up discussions..."
          v-model="fields.email"
          @input="errors.fields.email.length = 0"
        />
      </sui-form-field>
      <sui-button primary @click="submit">Send</sui-button>
    </sui-form>

    <sui-message v-if="success" icon positive>
      <p>Your feedback has been sent. Thank you so much!</p>
    </sui-message>

    <sui-message v-if="errors.all.length > 0" icon error>
      <sui-icon name="info" />
      <sui-message-content>
        <sui-list bulleted>
          <sui-list-item v-for="error of errors.all" :key="error">{{ error }}</sui-list-item>
        </sui-list>
      </sui-message-content>
    </sui-message>

    <sui-dimmer :active="waiting">
      <sui-loader />
    </sui-dimmer>
  </sui-container>
</template>
