<script lang="ts">
import { glossary } from '@/glossary';
import MarkdownContent from './MarkdownContent.vue';

export default {
  components: { MarkdownContent },
  props: {
    markdown: { type: String, required: true },
    disabled: { type: Boolean, default: false },
  },
  data() {
    return { statement: '' };
  },
  created() {
    this.statement = this.markdown;
    if (this.disabled) return;

    const placeholder = () => Math.random().toString(36).substring(2, 15);
    const craft = (key: string, value: string) => `<i data-tooltip="${value}" data-position="bottom center">${key}</i>`;
    const placeholders: Record<string, string> = {};

    for (const [key, value] of Object.entries(glossary)) {
      const search = new RegExp(`\\b${key}\\b`, 'i');
      const match = search.exec(this.statement);
      if (match) {
        const placeholderKey = placeholder();
        placeholders[placeholderKey] = craft(match[0], value);
        this.statement = this.statement.replace(search, placeholderKey);
      }
    }
    for (const [key, value] of Object.entries(placeholders)) {
      this.statement = this.statement.replace(key, value);
    }
    console.log(this.statement);
  },
};
</script>

<template>
  <markdown-content display unsafe :markdown="statement" />
</template>
