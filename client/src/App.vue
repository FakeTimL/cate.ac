<script lang="ts">
import { useRouter } from 'vue-router';
import SignUpModal from './pages/components/SignUpModal.vue';
import LogInModal from './pages/components/LogInModal.vue';

// See: https://stackoverflow.com/a/66258242
export default {
  data() {
    return {
      signUpModalIsActive: false,
      logInModalIsActive: false,
    };
  },
  components: { SignUpModal, LogInModal },
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
};
</script>

<template>
  <div class="outer-container">
    <sui-menu borderless :inverted="landingPage" :color="landingPage ? 'blue' : ''" class="navigation">
      <sui-container>
        <router-link to="/">
          <sui-menu-item header>CATE</sui-menu-item>
        </router-link>
        <router-link to="/topics">
          <sui-menu-item :active="currentPathIs('/topics')">Topics</sui-menu-item>
        </router-link>
        <router-link to="/feedback">
          <sui-menu-item :active="currentPathIs('/feedback')">Feedback</sui-menu-item>
        </router-link>
        <router-link to="/about">
          <sui-menu-item :active="currentPathIs('/about')">About</sui-menu-item>
        </router-link>
        <!--
        {% if user.is_authenticated %}
        <a class="item" href="{% url 'main:history' %}">Answers</a>
        {% endif %}
        -->
        <div class="right menu">
          <!--
          {% if user.is_authenticated %}
          <a class="login item" href="{% url 'accounts:index' %}">
            <img class="ui avatar image" src="{{ user.profile.get_avatar }}" alt="{{ user.get_username }}'s avatar" />
            <span>user.get_username</span>
          </a>
          -->
          <sui-menu-item class="login item" @click="logInModalIsActive = true">
            <span>Log in</span>
          </sui-menu-item>
          <sui-menu-item class="login item" @click="signUpModalIsActive = true">
            <sui-icon name="user circle" />
            <span>Sign up</span>
          </sui-menu-item>
        </div>
      </sui-container>
    </sui-menu>
    <div class="content">
      <router-view v-slot="{ Component, route }">
        <transition name="fade" mode="default">
          <div :key="route.fullPath">
            <component :is="Component"></component>
          </div>
        </transition>
      </router-view>
    </div>
    <sui-segment inverted vertical class="footer">
      <sui-container>
        <sui-list link inverted size="small">
          <sui-list-item as="a" href="https://doc.ic.uk.cate.ac/">doc.ic.uk.cate.ac</sui-list-item>
          <sui-list-item as="a" href="https://cate.doc.ic.ac.uk/">cate.doc.ic.ac.uk</sui-list-item>
        </sui-list>
      </sui-container>
    </sui-segment>
    <sign-up-modal v-model="signUpModalIsActive" />
    <log-in-modal v-model="logInModalIsActive" />
  </div>
</template>

<style scoped>
/* Outermost container */
.outer-container {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}

.navigation,
.content {
  flex-grow: 0;
}

.footer {
  flex-grow: 1;
  padding: 2em 0em;
}

/* Navigation bar */
.navigation {
  margin: 0;
  border-radius: 0;
  /* Tweak: hide top shadow */
  margin-top: -1px;
  /* Transition between landing page and other pages */
  transition: background-color 0.5s;
}

.navigation .item {
  padding-top: 1.4em;
  padding-bottom: 1.4em;
}

.navigation .item .avatar {
  margin-top: -1em;
  margin-bottom: -1em;
  /* Tweak: make it less crowded */
  margin-right: 0.4em;
}

.navigation .item .ui.tiny.image {
  height: 3em;
  width: auto;
  margin: -0.8em 0;
}

@media (max-width: 767.5px) {
  .navigation .login.item span {
    display: none;
  }
}

.fade-leave-active {
  position: absolute; /* Takes no space in document flow when leaving. */
  width: 100%;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
