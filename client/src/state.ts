/** Global states. */

import type { User } from './api';
import { ref, reactive } from 'vue';
import { printErrors } from './errors';

export type Severity = 'success' | 'info' | 'warning' | 'error';

export class Message {
  constructor(public severity: Severity, public content: string, public key: symbol = Symbol()) {}

  get className(): Partial<Record<Severity, boolean>> {
    if (this.severity == 'success') return { success: true };
    else if (this.severity == 'info') return { info: true };
    else if (this.severity == 'warning') return { warning: true };
    else if (this.severity == 'error') return { error: true };
    else return {};
  }
}

/** Global shared state of messages. */
export const messages = reactive<Message[]>([]);

/** A convenient wrapper function for popping error messages. */
export function messageErrors(e: unknown) {
  const arr = printErrors(e);
  for (const elem of arr) messages.push(new Message('error', elem));
}

/** Global shared state of current user information. */
export const user = ref<User>();
