<script lang="ts">
export default {};
</script>

<template>
  <sui-container text style="padding: 1em 0; min-height: 100vh">
    <sui-header as="h1">Send anonymous feedback</sui-header>
    <form class="ui form" action="{{ submit_url }}" method="{{ submit_method }}">
      {% if submit_method|lower == 'post' %}{% csrf_token %}{% endif %}
      <div class="field">
        <label>Describe any problem or your ideas for improvement:</label>
        <textarea name="content" placeholder="Any idea is appreciated..." rows="20" style="resize: vertical"></textarea>
      </div>
      <div class="field">
        <label>Email (optional)</label>
        <input type="text" name="email" placeholder="If you want follow-up discussions..." />
      </div>
      <input class="ui button primary" type="submit" value="Send" />
    </form>
  </sui-container>
</template>
