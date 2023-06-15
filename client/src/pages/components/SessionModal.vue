<script lang="ts">
import { api } from '@/api';

export default {
  // See: https://vuejs.org/guide/components/v-model.html
  props: ['modelValue', 'username'],
  emits: ['update:modelValue'],
  data() {
    return {
      waiting: false,
      errors: [] as string[],
    };
  },
  methods: {
    async submit() {
      this.errors = [];
      this.waiting = true;
      try {
        await api.delete('accounts/session/', {});
        this.waiting = false;
        window.location.reload(); // Page refresh is required for new CSRF token.
      } catch (error) {
        this.waiting = false;
        window.location.reload(); // Page refresh is required for new CSRF token.
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
    <sui-modal-header>User {{ username }}</sui-modal-header>
    <sui-modal-content scrolling>
      <sui-form></sui-form>
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
      <sui-button primary @click="isActive = false">OK</sui-button>
      <sui-button @click="submit">Log out</sui-button>
    </sui-modal-actions>
    <sui-dimmer :active="waiting">
      <sui-loader />
    </sui-dimmer>
  </sui-modal>
</template>

<style scoped></style>
