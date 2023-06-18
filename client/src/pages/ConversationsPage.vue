<script lang="ts">
import { api, type User } from '@/api';
import { messageErrors, user } from '@/state';
import defaultAvatar from '@/assets/default-avatar.png';

export default {
  setup() {
    return { user };
  },
  computed: {
    avatar(): string {
      return user.value?.avatar ?? defaultAvatar;
    },
  },
};
</script>

<template>
  <div class="ui container" style="padding: 2em">
    <div v-if="user" class="ui stackable grid">
      <div class="five wide column">
        <div class="ui action input" style="width: 100%">
          <input type="number" placeholder="User ID" />
          <button class="ui primary button"><i class="plus icon" />New</button>
        </div>

        <div class="ui medium divided selection list">
          <router-link to="/" class="item">
            <i class="file alternate icon" />
            <div class="content">
              <div class="header">Name</div>
              <div class="description">Last message</div>
            </div>
          </router-link>
          <router-link to="/" class="item">
            <i class="file alternate icon" />
            <div class="content">
              <div class="header">Name</div>
              <div class="description">Last message</div>
            </div>
          </router-link>
        </div>
      </div>

      <div class="eleven wide column">
        <div class="window">
          <div class="ui segment">
            <div class="ui grid">
              <div class="left floated fourteen wide column">
                <div class="received message">
                  <img class="ui avatar image" :src="avatar" :alt="`${user.username}'s avatar`" />
                  <div class="content">
                    <!--
                  <div class="ui left sub header">
                    Froggie&nbsp;&nbsp;
                    <span class="timestamp">12:47:00</span>
                  </div>
                  -->
                    <div class="ui left pointing label">Hello World!</div>
                  </div>
                </div>
              </div>
              <div class="right floated fourteen wide column">
                <div class="sent message">
                  <div class="content">
                    <!--
                  <div class="ui sub header">
                    Queenie&nbsp;&nbsp;
                    <span class="timestamp">12:47:00</span>
                  </div>
                  -->
                    <div class="ui primary right pointing label">Hello World!</div>
                  </div>
                  <img class="ui avatar image" :src="avatar" :alt="`${user.username}'s avatar`" />
                </div>
              </div>
            </div>
          </div>

          <div class="ui action input">
            <input type="text" placeholder="Write your message..." class="msgbox" />
            <button class="ui primary button">Send</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.message {
  padding: 1em;
  display: flex;
}

.content {
  text-align: left;
  padding-left: 5px;
  padding-right: 5px;
}

.left .header {
  padding-left: 10px !important;
  text-align: left;
  justify-content: left;
}

.right .header {
  padding-right: 10px !important;
  text-align: right;
  justify-content: right;
}

.label {
  font-size: 1em !important;
  font-weight: 400 !important;
}

/*
.left .label {
  float: left;
}

.right .label {
  float: right;
}

.timestamp {
  font-style: italic;
  color: orange;
}
*/

.received {
  justify-content: left;
}

.sent {
  justify-content: right;
}

.window {
  height: 100%;
  min-height: 80vh;
  display: flex;
  flex-direction: column;
}

.window > .segment {
  flex-grow: 1;
  padding: 1em;
  overflow: hidden scroll;
}

.window > .input {
  flex-grow: 0;
}
</style>
