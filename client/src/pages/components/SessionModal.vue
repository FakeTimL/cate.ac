<script lang="ts">
import { api } from '@/api';
import { FormErrors } from '@/forms';
import axios from 'axios';

class FormFields {}

export default {
  // See: https://vuejs.org/guide/components/v-model.html
  props: ['modelValue', 'username'],
  emits: ['update:modelValue'],
  data() {
    return {
      waiting: false,
      fields: new FormFields(),
      errors: new FormErrors<FormFields>({}),
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
      this.errors.clear();
      this.waiting = true;
      try {
        await api.delete('accounts/session/');
        window.location.reload(); // Page refresh is required for new CSRF token.
        return;
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
  <sui-modal size="tiny" v-model="modalActive">
    <sui-modal-header>User {{ username }}</sui-modal-header>
    <sui-modal-content scrolling>
      <sui-form></sui-form>
    </sui-modal-content>
    <sui-modal-actions>
      <sui-message v-if="errors.all.length > 0" icon error>
        <sui-icon name="info" />
        <sui-message-content>
          <sui-list bulleted>
            <sui-list-item v-for="error of errors.all" :key="error">{{ error }}</sui-list-item>
          </sui-list>
        </sui-message-content>
      </sui-message>
      <sui-button primary @click="modalActive = false">OK</sui-button>
      <sui-button @click="submit">Log out</sui-button>
    </sui-modal-actions>
    <sui-dimmer :active="waiting">
      <sui-loader />
    </sui-dimmer>
  </sui-modal>
</template>

<style scoped></style>
