<script lang="ts">
import { api, type User } from '@/api';
import { messageErrors, user } from '@/state';
import { useRouter } from 'vue-router';
import PopupMessages from './pages/components/PopupMessages.vue';
import BaseLayout from './pages/components/BaseLayout.vue';
import SignUpModal from './pages/components/SignUpModal.vue';
import LogInModal from './pages/components/LogInModal.vue';
import SessionModal from './pages/components/SessionModal.vue';
import defaultAvatar from '@/assets/default-avatar.png';

// See: https://stackoverflow.com/a/66258242
export default {
  components: { PopupMessages, BaseLayout, SignUpModal, LogInModal, SessionModal },
  setup() {
    return { user };
  },
  data() {
    return {
      loading: true,
      signUpModalIsActive: false,
      logInModalIsActive: false,
      sessionModalIsActive: false,
    };
  },
  methods: {
    currentPathIs(s: string): boolean {
      return useRouter().currentRoute.value.path === s;
    },
  },
  computed: {
    landingPage(): boolean {
      return this.currentPathIs('/');
    },
    avatar(): string {
      return user.value?.avatar ?? defaultAvatar;
    },
  },
  async created() {
    try {
      const data = (await api.get('accounts/me/')).data;
      if (data) user.value = data as User;
      // console.log(data);
    } catch (e) {
      messageErrors(e);
    }
  },
};
</script>

<template>
  <base-layout :landingPage="currentPathIs('/')">
    <template #navigation>
      <router-link to="/" class="header item">
        <span>CATE</span>
      </router-link>
      <router-link to="/topics/" class="item" :class="{ active: currentPathIs('/topics/') }">
        <i class="book icon" />
        <span>Topics</span>
      </router-link>
      <router-link v-if="user" to="/submissions/" class="item" :class="{ active: currentPathIs('/submissions/') }">
        <i class="edit icon" />
        <span>Answers</span>
      </router-link>
      <router-link v-if="user" to="/attempts/" class="item" :class="{ active: currentPathIs('/attempts/') }">
        <i class="file alternate icon" />
        <span>Exams</span>
      </router-link>
      <router-link to="/feedback/" class="item" :class="{ active: currentPathIs('/feedback/') }">
        <i class="comment icon" />
        <span>Feedback</span>
      </router-link>
      <!--
      <router-link to="/about/" class="item" :class="{ active: currentPathIs('/about/') }">
        <i class="info circle icon" />
        <span>About</span>
      </router-link>
      -->
      <a v-if="!user" @click="logInModalIsActive = true" class="right item">
        <span>Log in</span>
      </a>
      <a v-if="!user" @click="signUpModalIsActive = true" class="item">
        <i class="user circle icon" />
        <span>Sign up</span>
      </a>
      <router-link v-if="user" to="/conversations/" class="right item">
        <i class="envelope icon" />
        <span>Messages</span>
      </router-link>
      <a v-if="user" @click="sessionModalIsActive = true" class="item">
        <img class="ui avatar image" :src="avatar" :alt="`${user.username}'s avatar`" />
        <span>{{ user.username }}</span>
      </a>
    </template>
    <template #footer>
      <div class="ui small inverted link list">
        <a href="https://doc.ic.uk.cate.ac/" class="item">doc.ic.uk.cate.ac</a>
        <a href="https://cate.doc.ic.ac.uk/" class="item">cate.doc.ic.ac.uk</a>
      </div>
    </template>
    <template #modals>
      <sign-up-modal v-model="signUpModalIsActive" />
      <log-in-modal v-model="logInModalIsActive" />
      <session-modal v-model="sessionModalIsActive" />
    </template>
  </base-layout>
  <popup-messages />
</template>

<style scoped></style>
