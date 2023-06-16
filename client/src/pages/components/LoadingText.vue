<script lang="ts">
export default {
  props: {
    loading: {
      type: Boolean,
      required: true,
    },
    length: {
      type: Number,
      default: 5,
    },
    fillHeight: {
      type: Boolean,
      default: false,
    },
    text: {
      type: String,
      required: false,
    },
  },
};
</script>

<template>
  <div class="stack-container">
    <transition name="fade" mode="default">
      <div v-if="loading" key="loading" class="child" :style="{ minHeight: fillHeight ? '80vh' : undefined }">
        <div v-if="text" class="ui active indeterminate text loader">{{ text }}</div>
        <div v-for="index in length" :key="index" class="ui placeholder">
          <div class="header">
            <div class="line"></div>
            <div class="line"></div>
          </div>
          <div class="paragraph">
            <div class="line"></div>
            <div class="line"></div>
            <div class="line"></div>
            <div class="line"></div>
            <div class="line"></div>
          </div>
        </div>
      </div>
      <div v-else key="loaded" class="child">
        <slot />
      </div>
    </transition>
  </div>
</template>

<style scoped>
/* See: https://stackoverflow.com/questions/59053601/adapt-parent-to-maximum-size-of-its-children-in-css */
.stack-container {
  display: grid;
  grid-template-rows: max-content;
  grid-template-columns: minmax(0, 1fr);
}

.stack-container > .child {
  grid-column: 1 / -1;
  grid-row: 1;
  position: relative;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
