<script lang="ts">
import { api, type Topic } from '@/api';
import LoadingText from './components/LoadingText.vue';

export default {
  components: { LoadingText },
  data() {
    return {
      loading: true,
      chapters: new Array<Topic>(),
      topics: new Map<number, Topic[]>(),
    };
  },
  async created() {
    try {
      for (let topic of (await api.get('main/topics/')).data as Topic[]) {
        if (topic.parent === null) {
          this.chapters.push(topic);
        } else {
          let list = this.topics.get(topic.parent);
          if (list === undefined) {
            list = [];
            this.topics.set(topic.parent, list);
          }
          list.push(topic);
        }
      }
      this.loading = false;
    } catch (error) {
      // TODO
      this.loading = false;
    }
  },
};
</script>

<template>
  <sui-container text style="padding: 1em 0; min-height: 80vh">
    <loading-text fill-height :loading="loading">
      <sui-header as="h1">Browse Questions by Topic</sui-header>
      <sui-list divided selection size="medium">
        <sui-list-item v-for="chapter in chapters" :key="chapter.pk">
          <sui-icon name="folder open outline" />
          <sui-list-content>
            <sui-list-header>{{ chapter.name }}</sui-list-header>
            <sui-list-list>
              <router-link
                class="ui item"
                v-for="topic in topics.get(chapter.pk)"
                :key="topic.pk"
                :to="`/topic/${topic.pk}/`"
              >
                <sui-icon name="book" />
                <sui-list-content>
                  <sui-list-header>{{ topic.name }}</sui-list-header>
                </sui-list-content>
              </router-link>
            </sui-list-list>
          </sui-list-content>
        </sui-list-item>
      </sui-list>
    </loading-text>
  </sui-container>
</template>

<style scoped></style>
