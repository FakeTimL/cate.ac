<script lang="ts">
import { api } from '@/api';

export default {
  data() {
    return {
      text: '',
      email: '',
      waiting: false,
      errors: [] as string[],
      success: false,
    };
  },
  methods: {
    async submit(e: Event) {
      e.preventDefault();
      this.errors = [];
      this.waiting = true;
      try {
        await api.post('main/feedbacks/', {
          text: this.text,
          email: this.email,
        });
        this.waiting = false;
        this.success = true;
      } catch (error) {
        this.waiting = false;
        this.errors.push('Unknown error: ' + error);
      }
    },
  },
};
</script>

<template>
  <sui-container text style="padding: 1em 0; min-height: 80vh">
    <sui-header as="h1">Send anonymous feedback</sui-header>

    <sui-form>
      <sui-form-field>
        <label>Describe any problem or your ideas for improvement:</label>
        <textarea v-model="text" placeholder="Any idea is appreciated..." rows="20" style="resize: vertical"></textarea>
      </sui-form-field>
      <sui-form-field>
        <label>Email (optional)</label>
        <input type="text" v-model="email" placeholder="If you want follow-up discussions..." />
      </sui-form-field>
      <sui-button primary @click="submit">Send</sui-button>
    </sui-form>

    <sui-message icon positive v-if="success">
      <p>Your feedback has been sent. Thank you so much!</p>
    </sui-message>

    <sui-message icon error v-if="errors.length">
      <sui-message-content>
        <sui-list bulleted>
          <sui-list-item v-for="error in errors" :key="error">{{ error }}</sui-list-item>
        </sui-list>
      </sui-message-content>
    </sui-message>

    <sui-dimmer :active="waiting">
      <sui-loader />
    </sui-dimmer>
  </sui-container>
</template>
