<script lang="ts">
import { api } from '@/api';
import { AxiosError } from 'axios';

function is<T>(value: T): T {
  return value;
}

type FormData = {
  username: string;
  password: string;
  email: string;
  passwordRepeat: string;
  agree: boolean;
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
        email: '',
        passwordRepeat: '',
        agree: false,
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
      if (this.fields.username == '') (this.fieldErrors.username ??= []).push('Username must not be empty.');
      if (this.fields.password == '') (this.fieldErrors.password ??= []).push('Password must not be empty.');
      if (this.fields.password != this.fields.passwordRepeat)
        (this.fieldErrors.passwordRepeat ??= []).push('Two passwords are different.');
      if (!this.fields.agree)
        (this.fieldErrors.agree ??= []).push(
          'Please indicate that you agree to the Terms of Use and Privacy Policy by checking the box.',
        );
      if (this.errorList.length) return;
      this.waiting = true;
      try {
        await api.post('accounts/users/', this.fields);
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
    <sui-modal-header>Sign up</sui-modal-header>
    <sui-modal-content scrolling>
      <sui-form>
        <sui-form-field :error="Boolean(fieldErrors.username)">
          <label>Username</label>
          <input placeholder="Username" v-model="fields.username" @input="delete fieldErrors.username" />
        </sui-form-field>
        <sui-form-field :error="Boolean(fieldErrors.email)">
          <label>Email (optional)</label>
          <input placeholder="Email (optional)" v-model="fields.email" @input="delete fieldErrors.email" />
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
        <sui-form-field :error="Boolean(fieldErrors.passwordRepeat)">
          <label>Repeat password</label>
          <input
            placeholder="Repeat password"
            type="password"
            v-model="fields.passwordRepeat"
            @input="delete fieldErrors.passwordRepeat"
          />
        </sui-form-field>
        <sui-form-field :error="Boolean(fieldErrors.agree)">
          <sui-checkbox
            label="I agree to the Terms of Use and Privacy Policy"
            v-model="fields.agree"
            @change="delete fieldErrors.agree"
          />
        </sui-form-field>
      </sui-form>
    </sui-modal-content>
    <sui-modal-actions>
      <sui-message icon error v-if="errorList.length">
        <sui-icon name="info" />
        <sui-message-content>
          <sui-list bulleted>
            <sui-list-item v-for="error of errorList" :key="error">{{ error }}</sui-list-item>
          </sui-list>
        </sui-message-content>
      </sui-message>
      <sui-button primary @click="submit">Sign up</sui-button>
      <sui-button @click="modalActive = false">Cancel</sui-button>
    </sui-modal-actions>
    <sui-dimmer :active="waiting">
      <sui-loader />
    </sui-dimmer>
  </sui-modal>
</template>

<style scoped></style>
