<script lang="ts">
import { api } from '@/api';
import { AxiosError } from 'axios';

function is<T>(value: T): T {
  return value;
}

type FormData = {
  username: string;
  password: string;
};

type FormError = Partial<Record<keyof FormData, string[]>>;

export default {
  // See: https://vuejs.org/guide/components/v-model.html
  props: ['modelValue'],
  emits: ['update:modelValue'],
  data() {
    return {
      waiting: false,
      fields: {
        username: '',
        password: '',
      },
      fieldErrors: is<FormError>({}),
      otherErrors: is<string[]>([]),
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
    errorList(): string[] {
      return Object.entries(this.fieldErrors)
        .reduce((acc, x) => acc.concat(x[1]), is<string[]>([]))
        .concat(this.otherErrors);
    },
  },
  methods: {
    async submit() {
      this.fieldErrors = {};
      this.otherErrors = [];
      if (this.fields.username == '') (this.fieldErrors.username ??= []).push('Please enter username.');
      if (this.fields.password == '') (this.fieldErrors.password ??= []).push('Please enter password.');
      if (this.errorList.length) return;
      this.waiting = true;
      try {
        await api.post('accounts/session/', this.fields);
        window.location.reload(); // Page refresh is required for new CSRF token.
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
  <sui-modal size="tiny" v-model="modalActive">
    <sui-modal-header>Log in</sui-modal-header>
    <sui-modal-content scrolling>
      <sui-form>
        <sui-form-field :error="Boolean(fieldErrors.username)">
          <label>Username</label>
          <input placeholder="Username" v-model="fields.username" @input="delete fieldErrors.username" />
        </sui-form-field>
        <sui-form-field :error="Boolean(fieldErrors.password)">
          <label>Password</label>
          <input
            placeholder="Password"
            type="password"
            v-model="fields.password"
            @input="delete fieldErrors.password"
          />
        </sui-form-field>
      </sui-form>
    </sui-modal-content>
    <sui-modal-actions>
      <sui-message v-if="errorList.length" icon error>
        <sui-icon name="info" />
        <sui-message-content>
          <sui-list bulleted>
            <sui-list-item v-for="error of errorList" :key="error">{{ error }}</sui-list-item>
          </sui-list>
        </sui-message-content>
      </sui-message>
      <sui-button primary @click="submit">Log in</sui-button>
      <sui-button @click="modalActive = false">Cancel</sui-button>
    </sui-modal-actions>
    <sui-dimmer :active="waiting">
      <sui-loader />
    </sui-dimmer>
  </sui-modal>
</template>

<style scoped></style>
