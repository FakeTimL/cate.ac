<script lang="ts">
type Fruit = 'Apple' | 'Banana' | 'Chocolate';

const colors = {
  Apple: 'red',
  Banana: 'yellow',
  Chocolate: 'brown',
};

export default {
  data() {
    return {
      selected: [],
    };
  },
  methods: {
    fruitColor(key: Fruit): string {
      return colors[key];
    },
  },
};
</script>

<template>
  <p><sui-checkbox label="Apple" value="Apple" v-model="selected" /></p>
  <p><sui-checkbox label="Banana" value="Banana" v-model="selected" /></p>
  <p><sui-checkbox label="Chocolate" value="Chocolate" v-model="selected" /></p>
  <span>Selected: </span>
  <sui-label v-for="item in selected" :color="fruitColor(item)" :key="item">{{ item }}</sui-label>
</template>
