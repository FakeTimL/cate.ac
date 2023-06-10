<script lang="ts">
export default {
  // See: https://vuejs.org/guide/components/v-model.html
  props: ['modelValue'],
  emits: ['update:modelValue'],
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
    <sui-modal-content image>
      <sui-image wrapped size="medium" src="" />
      <sui-modal-description>
        <sui-header>Default Profile Image</sui-header>
        <p>We've found the following gravatar image associated with your e-mail address.</p>
        <p>Is it okay to use this photo?</p>
      </sui-modal-description>
    </sui-modal-content>
    <sui-modal-actions>
      <sui-button positive @click="isActive = false">OK</sui-button>
    </sui-modal-actions>
  </sui-modal>
</template>

<style scoped></style>
