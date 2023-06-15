<script lang="ts">
import { api } from '@/api';
import { AxiosError } from 'axios';

export default {
  // See: https://vuejs.org/guide/components/v-model.html
  props: ['modelValue'],
  emits: ['update:modelValue'],
  data() {
    return {
      username: '',
      username_error: false,
      password: '',
      password_error: false,
      waiting: false,
      errors: [] as string[],
    };
  },
  methods: {
    async submit() {
      this.errors = [];
      if (this.username == '') {
        this.username_error = true;
        this.errors.push('Please enter username.');
      }
      if (this.password == '') {
        this.password_error = true;
        this.errors.push('Please enter password.');
      }
      if (this.errors.length != 0) {
        return;
      }
      this.waiting = true;
      try {
        const response = await api.post('accounts/session/', {
          username: this.username,
          password: this.password,
        });
        this.waiting = false;
        if (response.data['username']) {
          window.location.reload(); // Page refresh is required for new CSRF token.
          return;
        } else {
          this.errors.push('Incorrect username or password.');
          return;
        }
      } catch (error) {
        this.waiting = false;
        let known = false;
        if (error instanceof AxiosError && error.response !== undefined) {
          const data = error.response.data;
          if (data['username'] instanceof Array) {
            this.username_error = known = true;
            this.errors = this.errors.concat(data['username']);
          }
          if (data['password'] instanceof Array) {
            this.password_error = known = true;
            this.errors = this.errors.concat(data['password']);
          }
        }
        if (!known) {
          this.errors.push('Unknown error: ' + error);
        }
      }
    },
  },
  computed: {
    isActive: {
      get(): boolean {
        return this.modelValue;
      },
      set(value: boolean) {
        this.$emit('update:modelValue', value);
      },
    },
  },
};
</script>

<template>
  <sui-modal size="tiny" v-model="isActive">
    <sui-modal-header>Log in</sui-modal-header>
    <sui-modal-content scrolling>
      <sui-form>
        <sui-form-field :error="username_error">
          <label>Username</label>
          <input placeholder="Username" v-model="username" @click="username_error = false" />
        </sui-form-field>
        <sui-form-field :error="password_error">
          <label>Password</label>
          <input placeholder="Password" type="password" v-model="password" @click="password_error = false" />
        </sui-form-field>
      </sui-form>
    </sui-modal-content>
    <sui-modal-actions>
      <sui-message icon error v-if="errors.length">
        <sui-icon name="info" />
        <sui-message-content>
          <sui-list bulleted>
            <sui-list-item v-for="error in errors" :key="error">{{ error }}</sui-list-item>
          </sui-list>
        </sui-message-content>
      </sui-message>
      <sui-button primary @click="submit">Log in</sui-button>
      <sui-button @click="isActive = false">Cancel</sui-button>
    </sui-modal-actions>
    <sui-dimmer :active="waiting">
      <sui-loader />
    </sui-dimmer>
  </sui-modal>
</template>

<style scoped></style>
