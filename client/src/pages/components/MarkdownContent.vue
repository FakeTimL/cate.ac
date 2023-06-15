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
  <div class="markdown" v-html="html"></div>
</template>

<style scoped></style>
