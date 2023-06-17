/** Global messages. */

import { AxiosError } from 'axios';
import { reactive } from 'vue';

/** See: https://stackoverflow.com/a/58962072 */
function containsKey<T extends object>(obj: T, key: PropertyKey): key is keyof T {
  return key in obj;
}

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
export const messages = reactive(new Array<Message>());

/** A convenient wrapper function for popping error messages. */
export function messageError(e: unknown) {
  if (e instanceof AxiosError) {
    if (e.response !== undefined) {
      const data = e.response.data;
      if (data instanceof Object) {
        let known = false;
        const keys = ['detail'];
        for (const key of keys)
          if (containsKey(data, key)) {
            messages.push(new Message('error', String(data[key])));
            known = true;
          }
        if (!known) {
          messages.push(
            new Message('error', `Unexpected server response "${String(data)}" (status code ${e.response.status})`),
          );
        }
      } else {
        messages.push(
          new Message('error', `Unexpected server response "${String(data)}" (status code ${e.response.status})`),
        );
      }
    } else {
      messages.push(new Message('error', `Unexpected error "${e.message}"`));
    }
  }
}
