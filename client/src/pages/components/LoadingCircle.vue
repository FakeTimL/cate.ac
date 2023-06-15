<script lang="ts">
export default {
  props: {
    loading: {
      type: Boolean,
      required: true,
    },
    fillHeight: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<template>
  <div class="stack-container">
    <transition name="fade">
      <div v-if="loading" key="loading" class="child" :style="{ height: fillHeight ? '80vh' : undefined }">
        <div class="ui active loader" />
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
  position: relative;
  height: max-content;
  width: 100%;
  display: grid;
}

.stack-container > .child {
  position: relative;
  grid-column: 1 / -1;
  grid-row: 1;
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
