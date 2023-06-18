<script lang="ts">
import axios from 'axios';
import { api, type Message, type User } from '@/api';
import { messageErrors } from '@/state';
import { FormErrors } from '@/errors';

import LoadingCircle from './components/LoadingCircle.vue';
import MarkdownContent from './components/MarkdownContent.vue';
import defaultAvatar from '@/assets/default-avatar.png';

// Send a blank message as placeholder when starting a new conversation.
class FormFields {
  receiver: number | null = null;
  content = '';
}

class ConversationItem {
  subject: User;
  messages: Message[];

  waiting = false;
  content = '';

  constructor(subject: User, messages: Message[], prev: ConversationItem | null) {
    this.subject = subject;
    this.messages = messages;
    if (prev !== null) {
      this.waiting = prev.waiting;
      this.content = prev.content;
    }
  }
}

export default {
  components: { LoadingCircle, MarkdownContent },
  setup() {
    return { defaultAvatar };
  },

  props: {
    pk: { type: String, required: false }, // Subject primary key (TODO)
  },
  data() {
    return {
      loading: true,
      reloadTimeout: null as number | null,
      user: null as User | null,
      items: null as ConversationItem[] | null,
      itemIndex: null as number | null,

      waiting: false,
      fields: new FormFields(),
      errors: new FormErrors<FormFields>({ receiver: [], content: [] }),
    };
  },
  computed: {
    current(): ConversationItem | null {
      if (this.itemIndex === null || this.items === null) return null;
      return this.items[this.itemIndex] ?? null;
    },
  },

  async created() {
    await this.reload();
    this.loading = false;
    // Scroll to bottom of conversation.
    if (this.items !== null && this.items.length > 0) this.itemIndex = 0;
    this.$nextTick(() => {
      const elem = this.$refs.window as HTMLElement | undefined;
      elem?.scroll({ top: elem.scrollHeight, behavior: 'smooth' });
    });
  },

  unmounted() {
    if (this.reloadTimeout !== null) clearTimeout(this.reloadTimeout);
  },

  methods: {
    // Reload all messages.
    async reload() {
      try {
        // Retrieve current user and all messages.
        this.user = (await api.get('accounts/me/')).data as User;
        const messages = (await api.get(`accounts/me/messages/`)).data as Message[];

        // Make more recent conversations appear on top.
        messages.sort((x, y) => new Date(y.date).getTime() - new Date(x.date).getTime());

        // Classify messages according to related users.
        let map = new Map<number, Message[]>();
        for (const message of messages) {
          const subject = message.sender == this.user.pk ? message.receiver : message.sender;
          let list = map.get(subject);
          if (list === undefined) {
            list = [];
            map.set(subject, list);
          }
          list.push(message);
        }

        // Retrieve related users.
        const subjects = new Map<number, User>();
        for (const [pk, _] of map.entries()) {
          const subject = (await api.get(`accounts/user/${pk}/`)).data as User;
          subjects.set(subject.pk, subject);
        }

        // Update or create ConversationItems.
        const old = this.items;
        this.items = new Array<ConversationItem>();
        for (const [pk, messages] of map.entries()) {
          const subject = subjects.get(pk)!;
          const prevItem = old?.find((v) => v.subject.pk == subject.pk) ?? null;
          this.items.push(new ConversationItem(subject, messages.reverse(), prevItem));
        }

        this.reloadTimeout = setTimeout(this.reload, 5000);
      } catch (e) {
        messageErrors(e);
      }
    },

    async add() {
      try {
        this.errors.clear();
        this.waiting = true;
        const _message = (await api.post(`accounts/me/messages/`, this.fields)).data as Message;
        // Trigger immediate reload (TODO: avoid).
        if (this.reloadTimeout !== null) clearTimeout(this.reloadTimeout);
        await this.reload();
        this.waiting = false;
      } catch (e) {
        if (axios.isAxiosError(e)) {
          this.errors.decode(e);
          this.waiting = false;
        } else {
          messageErrors(e);
        }
      }
    },

    async send(item: ConversationItem | null) {
      if (this.items === null || item === null || !item.content) return;
      try {
        item.waiting = true;
        const message = (
          await api.post(`accounts/me/messages/`, {
            receiver: item.subject.pk,
            content: item.content,
          })
        ).data as Message;
        item.messages.push(message);
        item.content = '';
        item.waiting = false;
        // Move item to top of list.
        this.items.splice(this.items.indexOf(item), 1);
        this.items.unshift(item);
        this.itemIndex = 0;
        // Scroll to bottom of conversation.
        this.$nextTick(() => {
          const elem = this.$refs.window as HTMLElement | undefined;
          elem?.scroll({ top: elem.scrollHeight, behavior: 'smooth' });
        });
      } catch (e) {
        messageErrors(e);
      }
    },
  },
};
</script>

<template>
  <div class="ui container" style="padding: 1em 0">
    <loading-circle :loading="loading" fill-height>
      <div v-if="user" class="ui stackable grid">
        <div class="five wide column">
          <div class="ui action input" style="width: 100%" :class="{ error: errors.fields.receiver.length > 0 }">
            <input
              type="number"
              placeholder="User ID (numeric)"
              v-model="fields.receiver"
              @input="errors.fields.receiver.length = 0"
            />
            <button class="ui primary button" :class="{ disabled: waiting, loading: waiting }" @click="add">
              <i class="plus icon" />New
            </button>
          </div>

          <div v-if="errors.all.length > 0" class="ui icon error message">
            <i class="info icon" />
            <div class="content">
              <ul class="ui bulleted list">
                <li v-for="error of errors.all" :key="error" class="item">
                  <markdown-content :markdown="error" />
                </li>
              </ul>
            </div>
          </div>

          <div class="ui medium divided selection list">
            <div
              v-for="(item, index) in items"
              :key="item.subject.pk"
              class="item"
              :class="{ active: index == itemIndex }"
              @click="itemIndex = index"
            >
              <img
                class="ui avatar image"
                :src="item.subject.avatar ?? defaultAvatar"
                :alt="`${item.subject.username}'s avatar`"
              />
              <div class="content">
                <div class="header">{{ item.subject.username }}#{{ item.subject.pk }}</div>
                <div class="description">{{ item.messages[item.messages.length - 1].content.substring(0, 30) }}</div>
              </div>
            </div>
          </div>
        </div>

        <div class="eleven wide column" style="padding: 1em 0">
          <div v-if="current !== null" class="window">
            <div class="ui segment" ref="window">
              <div class="ui grid">
                <!-- Filter out placeholder messages. -->
                <div
                  v-for="message in current.messages.filter((v) => v.content)"
                  :key="message.pk"
                  :class="{ left: message.sender != user.pk, right: message.sender == user.pk }"
                  class="floated fourteen wide column"
                >
                  <div v-if="message.sender != user.pk" class="received message">
                    <img
                      class="ui avatar image"
                      :src="current.subject.avatar ?? defaultAvatar"
                      :alt="`${current.subject.username}'s avatar`"
                    />
                    <div class="content">
                      <div class="ui left pointing label">
                        <markdown-content :markdown="message.content" />
                      </div>
                    </div>
                  </div>
                  <div v-else class="sent message">
                    <div class="content">
                      <div class="ui blue right pointing label">
                        <markdown-content :markdown="message.content" />
                      </div>
                    </div>
                    <img
                      class="ui avatar image"
                      :src="user?.avatar ?? defaultAvatar"
                      :alt="`${user.username}'s avatar`"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div class="ui action input">
              <input
                type="text"
                placeholder="Write your message..."
                v-model="current.content"
                @keypress.enter="send(current)"
              />
              <button class="ui primary button" @click="send(current)">Send</button>
            </div>
          </div>

          <div v-else class="ui placeholder segment">
            <div class="ui icon header">
              <i class="user plus icon" />
              Select or add a user to start conversation
            </div>
          </div>
        </div>
      </div>
    </loading-circle>
  </div>
</template>

<style scoped>
.message {
  display: flex;
  align-items: center;
}

.message .label:deep(a) {
  color: inherit;
  text-decoration: underline;
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

.placeholder.segment {
  height: 80vh;
}

.window {
  height: 80vh;
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
