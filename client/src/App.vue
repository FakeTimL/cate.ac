<script lang="ts">
import { api } from '@/api';
import { useRouter } from 'vue-router';
import { messageError } from './messages';
import PopupMessages from './pages/components/PopupMessages.vue';
import BaseLayout from './pages/components/BaseLayout.vue';
import SignUpModal from './pages/components/SignUpModal.vue';
import LogInModal from './pages/components/LogInModal.vue';
import SessionModal from './pages/components/SessionModal.vue';
import defaultAvatar from '@/assets/default-avatar.png';

// See: https://stackoverflow.com/a/66258242
export default {
  data() {
    return {
      loading: true,
      username: '', // TODO: make user class
      avatar: '',
      signUpModalIsActive: false,
      logInModalIsActive: false,
      sessionModalIsActive: false,
    };
  },
  components: { PopupMessages, BaseLayout, SignUpModal, LogInModal, SessionModal },
  methods: {
    currentPathIs(s: string): boolean {
      return useRouter().currentRoute.value.path === s;
    },
  },
  computed: {
    landingPage(): boolean {
      return this.currentPathIs('/');
    },
  },
  async created() {
    try {
      const data = (await api.get('accounts/session/', {})).data;
      if (data['username']) {
        this.username = data['username'];
        this.avatar = data['avatar'] ?? defaultAvatar;
      }
    } catch (e) {
      messageError(e);
    }
  },
};
</script>

<template>
  <base-layout :landingPage="currentPathIs('/')">
    <template #navigation>
      <router-link to="/">
        <sui-menu-item header>CATE</sui-menu-item>
      </router-link>
      <router-link to="/topics/">
        <sui-menu-item :active="currentPathIs('/topics')">Topics</sui-menu-item>
      </router-link>
      <router-link to="/submissions/" v-if="username">
        <sui-menu-item :active="currentPathIs('/submissions')">Answers</sui-menu-item>
      </router-link>
      <router-link to="/feedback/">
        <sui-menu-item :active="currentPathIs('/feedback')">Feedback</sui-menu-item>
      </router-link>
      <router-link to="/about/">
        <sui-menu-item :active="currentPathIs('/about')">About</sui-menu-item>
      </router-link>
      <sui-menu-item position="right" v-if="!username" @click="logInModalIsActive = true">
        <span>Log in</span>
      </sui-menu-item>
      <sui-menu-item v-if="!username" @click="signUpModalIsActive = true">
        <sui-icon name="user circle" />
        <span>Sign up</span>
      </sui-menu-item>
      <sui-menu-item position="right" v-if="username" @click="sessionModalIsActive = true">
        <sui-image avatar :src="avatar" :alt="`${username}'s avatar`" />
        <span>{{ username }}</span>
      </sui-menu-item>
    </template>
    <template #footer>
      <sui-list link inverted size="small">
        <sui-list-item as="a" href="https://doc.ic.uk.cate.ac/">doc.ic.uk.cate.ac</sui-list-item>
        <sui-list-item as="a" href="https://cate.doc.ic.ac.uk/">cate.doc.ic.ac.uk</sui-list-item>
      </sui-list>
    </template>
    <template #modals>
      <sign-up-modal v-model="signUpModalIsActive" />
      <log-in-modal v-model="logInModalIsActive" />
      <session-modal v-model="sessionModalIsActive" :username="username" />
    </template>
  </base-layout>
  <popup-messages />
</template>

<style scoped></style>
