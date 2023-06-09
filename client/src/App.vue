<script lang="ts">
import ClickCounter from './components/ClickCounter.vue';
import MultiChoice from './components/MultiChoice.vue';

export default {
  components: {
    ClickCounter,
    MultiChoice,
  },
};
</script>

<template>
  <div class="box">
    <click-counter />
    <multi-choice />
  </div>
</template>

<style scoped>
.box {
  max-width: 300px;
  margin: 1em auto;
}
</style>
