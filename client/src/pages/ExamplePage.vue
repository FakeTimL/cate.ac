<script lang="ts">
export default {
  data() {
    return {
      count: 0,
    };
  },
  computed: {
    // Had to make this a string, otherwise 0 will not display correctly
    counterText(): string {
      return this.count.toString();
    },
    popupText(): string {
      return 'Click to increment the counter. Next value: ' + (this.count + 1).toString();
    },
  },
  methods: {
    increment() {
      this.count++;
    },
    reset() {
      this.count = 0;
    },
  },
  mounted() {
    // I don't know why but without this line the popup will not show until button is clicked once
    this.$forceUpdate();
  },
};
</script>

<template>
  <div class="box">
    <p class="center">
      <sui-statistic label="Clicks" :value="counterText" />
    </p>
    <p class="center">
      <sui-button icon ref="popupTrigger" @click="increment()">
        <sui-icon name="add" />
      </sui-button>
      <sui-popup position="bottom center" :content="popupText" :trigger="$refs.popupTrigger" />
      <sui-button icon @click="reset()">
        <sui-icon name="undo" />
      </sui-button>
    </p>
  </div>
</template>

<style scoped>
.box {
  max-width: 300px;
  margin: 0 auto;
  padding: 1em 0;
}

.center {
  text-align: center;
}
</style>
