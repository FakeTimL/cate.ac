<script lang="ts">
export default {};
</script>

<template>
  <div class="background">
    <div class="ui text container" style="padding: 1em 0; min-height: 80vh">
      <h1 class="ui header">About Us</h1>
      <div class="ui message">
        <p><strong>Q: What does the name "CATE" mean?</strong></p>
        <p>A: "Computer-Assisted Test Evaluator..."</p>
      </div>
      <h2 class="ui header">Our Mission</h2>
      <p>TODO</p>
      <h2 class="ui header">Our Team</h2>
      <p>TODO</p>
    </div>
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
