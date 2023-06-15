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
      email: '',
      email_error: false,
      password: '',
      password_error: false,
      password_repeat: '',
      password_repeat_error: false,
      agree: false,
      agree_error: false,
      waiting: false,
      errors: [] as string[],
    };
  },
  methods: {
    async submit() {
      this.errors = [];
      if (this.username == '') {
        this.username_error = true;
        this.errors.push('Username must not be empty.');
      }
      if (this.password == '') {
        this.password_error = true;
        this.errors.push('Password must not be empty.');
      }
      if (this.password != this.password_repeat) {
        this.password_repeat_error = true;
        this.errors.push('Two passwords are different.');
      }
      if (!this.agree) {
        this.agree_error = true;
        this.errors.push('Please indicate that you agree to the Terms of Use and Privacy Policy by checking the box.');
      }
      if (this.errors.length != 0) {
        return;
      }
      this.waiting = true;
      try {
        await api.post('accounts/users/', {
          username: this.username,
          password: this.password,
          email: this.email,
        });
        await api.post('accounts/session/', {
          username: this.username,
          password: this.password,
        });
        this.waiting = false;
        window.location.reload(); // Page refresh is required for new CSRF token.
        return;
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
          if (data['email'] instanceof Array) {
            this.email_error = known = true;
            this.errors = this.errors.concat(data['email']);
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
    <sui-modal-header>Sign up</sui-modal-header>
    <sui-modal-content scrolling>
      <sui-form>
        <sui-form-field :error="username_error">
          <label>Username</label>
          <input placeholder="Username" v-model="username" @click="username_error = false" />
        </sui-form-field>
        <sui-form-field :error="email_error">
          <label>Email (optional)</label>
          <input placeholder="Email (optional)" v-model="email" @click="email_error = false" />
        </sui-form-field>
        <sui-form-field :error="password_error">
          <label>Password</label>
          <input placeholder="Password" type="password" v-model="password" @click="password_error = false" />
        </sui-form-field>
        <sui-form-field :error="password_repeat_error">
          <label>Repeat password</label>
          <input
            placeholder="Repeat password"
            type="password"
            v-model="password_repeat"
            @click="password_repeat_error = false"
          />
        </sui-form-field>
        <sui-form-field :error="agree_error">
          <sui-checkbox
            label="I agree to the Terms of Use and Privacy Policy"
            v-model="agree"
            @click="agree_error = false"
          />
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
      <sui-button primary @click="submit">Sign up</sui-button>
      <sui-button @click="isActive = false">Cancel</sui-button>
    </sui-modal-actions>
    <sui-dimmer :active="waiting">
      <sui-loader />
    </sui-dimmer>
  </sui-modal>
</template>

<style scoped></style>
