<script lang="ts">
export default {
  props: {
    landingPage: Boolean,
  },
  data() {
    return {
      large: false,
      sidebarActive: false,
      sidebarAnimating: false,
      timeout: null as number | null,
    };
  },
  methods: {
    toggle(value: boolean) {
      this.sidebarActive = value;
      this.sidebarAnimating = true;
      if (this.timeout !== null) clearTimeout(this.timeout);
      this.timeout = setTimeout(() => (this.sidebarAnimating = false), 500);
    },
    onResize() {
      this.large = window.innerWidth > 767.5;
    },
    onClickSidebar() {
      this.toggle(false);
    },
    onClickPusher(e: Event) {
      if (this.sidebarActive) e.stopPropagation();
      this.toggle(false);
    },
    onClickButton(e: Event) {
      e.stopPropagation();
      this.toggle(true);
    },
  },
  mounted() {
    window.addEventListener('resize', this.onResize);
    this.onResize();
  },
  unmounted() {
    window.removeEventListener('resize', this.onResize);
  },
};
</script>

<template>
  <div class="ui pushable">
    <div
      class="ui left push sidebar inverted vertical navigation menu"
      :class="{ visible: sidebarActive, animating: sidebarAnimating }"
      @click="onClickSidebar"
    >
      <slot name="navigation"></slot>
    </div>
    <div class="pusher" :class="{ dimmed: sidebarActive }" @click="onClickPusher">
      <div class="flex-container">
        <div class="ui borderless navigation menu" :class="{ inverted: landingPage, blue: landingPage }">
          <sui-container v-if="large">
            <slot name="navigation"></slot>
          </sui-container>
          <sui-menu-item v-if="!large" @click="onClickButton">
            <sui-icon name="bars" />
          </sui-menu-item>
          <router-link to="/" v-if="!large">
            <sui-menu-item header>CATE</sui-menu-item>
          </router-link>
        </div>
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
            <slot name="footer"></slot>
          </sui-container>
        </sui-segment>
        <slot name="modals"></slot>
      </div>
    </div>
  </div>
</template>

<style scoped>
.flex-container {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}

.ui.navigation.menu,
.content {
  flex-grow: 0;
}

.ui.inverted.footer.segment {
  flex-grow: 1;
  padding: 2em 0em;
}

/* Navigation bar */
.ui.navigation.menu:not(.sidebar) {
  margin: 0;
  border-radius: 0;
  /* Tweak: hide top shadow */
  /* margin-top: -1px; */
  /* Transition between landing page and other pages */
  transition: background-color 0.5s;
}

.ui.navigation.menu :deep(.item) {
  padding-top: 1.4em;
  padding-bottom: 1.4em;
}

.ui.navigation.menu :deep(.item .avatar) {
  margin-top: -1em;
  margin-bottom: -1em;
  /* Tweak: make it less crowded */
  margin-right: 0.4em;
}

.ui.navigation.menu :deep(.item .ui.tiny.image) {
  height: 3em;
  width: auto;
  margin: -0.8em 0;
}

@media (max-width: 767.5px) {
  .ui.navigation.menu :deep(.login.item span) {
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
