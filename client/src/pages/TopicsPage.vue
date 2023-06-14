<script lang="ts">
import * as constants from '@/constants';
import axios, { AxiosError } from 'axios';
axios.defaults.baseURL = constants.apiRoot;

type Topic = {
  pk: number;
  name: string;
  parent: number | null;
  children: number[];
  questions: number[];
  resources: string;
};

export default {
  data() {
    return {
      loading: true,
      chapters: new Array<Topic>(),
      topics: new Map<number, Topic[]>(),
    };
  },
  async mounted() {
    try {
      for (let topic of (await axios.get('/main/topics/')).data as Topic[]) {
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
  <sui-container text style="padding: 1em 0">
    <sui-header as="h1">Browse questions by topic</sui-header>
    <div class="ui placeholder" v-if="loading">
      <div class="image header">
        <div class="line"></div>
        <div class="line"></div>
      </div>
      <div class="paragraph">
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
      </div>
      <div class="image header">
        <div class="line"></div>
        <div class="line"></div>
      </div>
      <div class="paragraph">
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
      </div>
      <div class="image header">
        <div class="line"></div>
        <div class="line"></div>
      </div>
      <div class="paragraph">
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
        <div class="line"></div>
      </div>
    </div>
    <sui-list divided selection size="medium" v-if="!loading">
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
  </sui-container>
</template>

<style scoped></style>
