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
      const data = (await api.get('accounts/session/')).data;
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
      <router-link to="/">
        <sui-menu-item header>CATE</sui-menu-item>
      </router-link>
      <router-link to="/topics/">
        <sui-menu-item :active="currentPathIs('/topics/')">Topics</sui-menu-item>
      </router-link>
      <router-link to="/submissions/" v-if="user">
        <sui-menu-item :active="currentPathIs('/submissions/')">Answers</sui-menu-item>
      </router-link>
      <router-link to="/attempts/" v-if="user">
        <sui-menu-item :active="currentPathIs('/attempts/')">Mock Exams</sui-menu-item>
      </router-link>
      <router-link to="/feedback/">
        <sui-menu-item :active="currentPathIs('/feedback/')">Feedback</sui-menu-item>
      </router-link>
      <router-link to="/about/">
        <sui-menu-item :active="currentPathIs('/about/')">About</sui-menu-item>
      </router-link>
      <sui-menu-item position="right" v-if="!user" @click="logInModalIsActive = true">
        <span>Log in</span>
      </sui-menu-item>
      <sui-menu-item v-if="!user" @click="signUpModalIsActive = true">
        <sui-icon name="user circle" />
        <span>Sign up</span>
      </sui-menu-item>
      <sui-menu-item position="right" v-if="user" @click="sessionModalIsActive = true">
        <sui-image avatar :src="avatar" :alt="`${user.username}'s avatar`" />
        <span>{{ user.username }}</span>
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
      <session-modal v-model="sessionModalIsActive" />
    </template>
  </base-layout>
  <popup-messages />
</template>

<style scoped></style>
