<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue';
import TheWelcome from './components/TheWelcome.vue';
</script>

<script lang="ts">
export default {
  data() {
    return {
      selected: [],
      count: 0,
    }
  },
  methods: {
    basicTrigger() {
      this.count++;
    }
  },
  mounted() {
  }
}
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <hello-world msg="You did it!" />
    </div>
  </header>

  <main>
    <the-welcome />
    {{ count }}
  </main>

  <sui-checkbox label="Apple" value="Apple" v-model="selected" />
  <sui-checkbox label="Banana" value="Banana" v-model="selected" />
  <sui-checkbox label="Chocolate" value="Chocolate" v-model="selected" />

  <sui-button animated>
    <sui-button-content visible>Next</sui-button-content>
    <sui-button-content hidden>
      <sui-icon name="arrow right" />
    </sui-button-content>
  </sui-button>
  <sui-button icon ref="basicTrigger">
    <sui-icon name="add" />
  </sui-button>
  <!-- sui-popup :trigger="basicTrigger" basic content="The default theme's basic popup removes the pointing arrow." /> -->
</template>

<!--
<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
-->
