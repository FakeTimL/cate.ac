<script lang="ts">
import { messages } from '@/state';
import MarkdownContent from './MarkdownContent.vue';

export default {
  components: { MarkdownContent },
  setup() {
    return { messages };
  },
};
</script>

<template>
  <transition-group tag="div" name="list" class="fixed-container">
    <div v-for="message in messages.slice().reverse()" :key="message.key" class="child">
      <div class="ui floating message" :class="message.className" style="margin: 0 !important">
        <i class="close icon" @click="messages.splice(messages.indexOf(message), 1)"></i>
        <markdown-content :markdown="message.content" />
      </div>
    </div>
  </transition-group>
</template>

<style scoped>
.fixed-container {
  position: fixed;
  right: 0;
  bottom: 0;
  width: 30em;
  max-width: 100%;
}

.fixed-container > .child {
  padding-right: 1em;
  padding-bottom: 1em;
  width: 100%;
}

/* See: https://vuejs.org/guide/built-ins/transition-group.html#move-transitions */
.list-move,
.list-enter-active,
.list-leave-active {
  transition: all 0.5s cubic-bezier(0, 0.49, 0.24, 0.96);
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* Ensure leaving items are taken out of layout flow. */
.list-leave-active {
  position: absolute;
}
</style>
