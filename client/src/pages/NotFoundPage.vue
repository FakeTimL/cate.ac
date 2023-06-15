<script lang="ts">
export default {};
</script>

<template>
  <sui-container class="outer-container">
    <sui-header icon as="h1">
      <sui-icon name="frown outline" />
      <sui-header-content>
        404 Not Found
        <sui-header-subheader>The requested URL does not exist...</sui-header-subheader>
      </sui-header-content>
    </sui-header>
  </sui-container>
</template>

<style scoped>
.outer-container {
  padding: 1em 0;
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
