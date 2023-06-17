<script lang="ts">
import { api } from '@/api';
import { FormErrors } from '@/errors';
import { messageErrors } from '@/messages';
import axios from 'axios';

import MarkdownContent from './components/MarkdownContent.vue';

class FormFields {
  text: string = '';
  email: string = '';
}

export default {
  components: {
    MarkdownContent,
  },
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
      try {
        e.preventDefault();
        this.success = false;
        this.errors.clear();
        if (this.fields.text == '') this.errors.fields.text.push('Please write something...');
        if (this.errors.all.length > 0) return;
        this.waiting = true;
        await api.post('main/feedbacks/', this.fields);
        this.success = true;
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
  <div class="ui text container" style="padding: 1em 0; min-height: 80vh">
    <h1 class="ui header">Send Anonymous Feedback</h1>
    <form class="ui form">
      <div class="field" :class="{ error: errors.fields.text.length > 0 }">
        <label>Describe any problem or your ideas for improvement:</label>
        <textarea
          placeholder="Any idea is appreciated..."
          rows="20"
          style="resize: vertical"
          v-model="fields.text"
          @input="errors.fields.text.length = 0"
        ></textarea>
      </div>

      <div class="field" :class="{ error: errors.fields.email.length > 0 }">
        <label>Email (optional)</label>
        <input
          placeholder="If you want follow-up discussions..."
          v-model="fields.email"
          @input="errors.fields.email.length = 0"
        />
      </div>
      <button class="ui primary button" :class="{ disabled: waiting, loading: waiting }" @click="submit">Send</button>
    </form>

    <div v-if="success" class="ui success icon message">
      <p>Your feedback has been sent. Thank you so much!</p>
    </div>

    <div v-if="errors.all.length > 0" class="ui error icon message">
      <i class="info icon" />
      <div class="content">
        <ul class="ui bulleted list">
          <li v-for="error of errors.all" :key="error" class="item">
            <markdown-content :markdown="error" />
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
