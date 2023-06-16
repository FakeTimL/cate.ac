<script lang="ts">
import { render } from '@/render';

export default {
  props: {
    html: {
      type: String,
      required: true,
    },
  },
  mounted() {
    render(this.$el);
  },
};
</script>

<template>
  <div v-html="html"></div>
</template>

<style scoped></style>
