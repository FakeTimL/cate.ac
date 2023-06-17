<script lang="ts">
import { api } from '@/api';
import { FormErrors } from '@/errors';
import { messageErrors } from '@/messages';
import axios from 'axios';

import MarkdownContent from './MarkdownContent.vue';

class FormFields {
  username: string = '';
  password: string = '';
}

export default {
  components: { MarkdownContent },
  // See: https://vuejs.org/guide/components/v-model.html
  props: ['modelValue'],
  emits: ['update:modelValue'],
  data() {
    return {
      waiting: false,
      fields: new FormFields(),
      errors: new FormErrors<FormFields>({
        username: [],
        password: [],
      }),
    };
  },
  computed: {
    modalActive: {
      get(): boolean {
        return this.modelValue;
      },
      set(value: boolean) {
        this.$emit('update:modelValue', value);
      },
    },
  },
  methods: {
    async submit() {
      try {
        this.errors.clear();
        if (this.fields.username == '') this.errors.fields.username.push('Please enter username.');
        if (this.fields.password == '') this.errors.fields.password.push('Please enter password.');
        if (this.errors.all.length > 0) return;
        this.waiting = true;
        await api.post('accounts/session/', this.fields);
        window.location.reload(); // Page refresh is required for new CSRF token.
        return;
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
  <sui-modal size="tiny" v-model="modalActive">
    <sui-modal-header>Log in</sui-modal-header>

    <sui-modal-content scrolling>
      <sui-form>
        <sui-form-field :error="errors.fields.username.length > 0">
          <label>Username</label>
          <input placeholder="Username" v-model="fields.username" @input="errors.fields.username.length = 0" />
        </sui-form-field>
        <sui-form-field :error="errors.fields.password.length > 0">
          <label>Password</label>
          <input
            placeholder="Password"
            type="password"
            v-model="fields.password"
            @input="errors.fields.password.length = 0"
          />
        </sui-form-field>
      </sui-form>
    </sui-modal-content>

    <sui-modal-actions>
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
      <sui-button primary :disabled="waiting" :loading="waiting" @click="submit">Log in</sui-button>
      <sui-button @click="modalActive = false">Cancel</sui-button>
    </sui-modal-actions>
  </sui-modal>
</template>

<style scoped></style>
