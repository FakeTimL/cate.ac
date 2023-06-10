<script lang="ts">
export default {};
</script>

<template>
  <div class="background">
    <sui-container text style="padding: 1em 0; min-height: 100vh">
      <sui-header as="h1">About us</sui-header>
      <sui-message>
        <p><strong>Q: What does the name "CATE" mean?</strong></p>
        <p>A: ...</p>
      </sui-message>
      <sui-header as="h2">Our Mission</sui-header>
      <p>TODO</p>
      <sui-header as="h2">Our Team</sui-header>
      <p>TODO</p>
    </sui-container>
  </div>
</template>

<style scoped>
.background {
  width: 100%;
  background-image: url(@/assets/about-background-left.svg), url(@/assets/about-background-right.svg);
  background-size: 1420px, 1420px;
  background-repeat: no-repeat, no-repeat;
  background-position: left bottom, right bottom;
}
</style>
