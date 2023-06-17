<script lang="ts">
import { api, type Topic } from '@/api';
import LoadingText from './components/LoadingText.vue';
import { messageError } from '@/messages';

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
      for (const topic of (await api.get('main/topics/')).data as Topic[]) {
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
    } catch (e) {
      messageError(e);
    }
  },
};
</script>

<template>
  <div class="ui text container" style="padding: 1em 0; min-height: 80vh">
    <loading-text fill-height :loading="loading">
      <h1 class="ui header">Browse Questions by Topic</h1>
      <div class="ui medium divided selection list">
        <div v-for="chapter in chapters" :key="chapter.pk" class="item">
          <i class="folder open outline icon" />
          <div class="content">
            <div class="header">{{ chapter.name }}</div>
            <div class="list">
              <router-link
                v-for="topic in topics.get(chapter.pk)"
                :key="topic.pk"
                :to="`/topic/${topic.pk}/`"
                class="item"
              >
                <i class="book icon" />
                <div class="content">
                  <div class="header">{{ topic.name }}</div>
                </div>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </loading-text>
  </div>
</template>

<style scoped></style>
