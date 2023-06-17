import { AxiosError } from 'axios';

/** See: https://stackoverflow.com/a/58962072 */
function containsKey<T extends object>(obj: T, key: PropertyKey): key is keyof T {
  return key in obj;
}

/** Pretty-print general errors. */
export function printErrors(e: unknown): string[] {
  const res = new Array<string>();
  if (e instanceof AxiosError) {
    if (e.response !== undefined) {
      const data = e.response.data;
      if (data instanceof Object) {
        let known = false;
        const keys = ['detail', 'non_field_errors'];
        for (const key of keys)
          if (containsKey(data, key)) {
            res.push(String(data[key]));
            known = true;
          }
        if (!known) {
          res.push(
            [
              'Unexpected server response (status code ' + e.response.status.toString() + '):',
              '```json',
              JSON.stringify(data),
              '```',
            ].join('\n'),
          );
        }
      } else {
        res.push(
          [
            'Unexpected server response (status code ' + e.response.status.toString() + '):',
            '```json',
            JSON.stringify(data),
            '```',
          ].join('\n'),
        );
      }
    } else {
      res.push(['Unexpected error:', '```', e.message, '```'].join('\n'));
    }
  } else {
    res.push(['Unexpected error:', '```json', JSON.stringify(e), '```'].join('\n'));
  }
  return res;
}

/** Wraps common methods for handling form errors. */
export class FormErrors<T> {
  constructor(public fields: Record<keyof T, string[]>, public others: string[] = []) {}

  /** Clears all errors. */
  clear() {
    for (const values of Object.values<string[]>(this.fields)) values.length = 0;
    this.others = [];
  }

  /** Returns all errors as a list. */
  get all(): string[] {
    let res: string[] = [];
    for (const values of Object.values<string[]>(this.fields)) res = res.concat(values);
    res = res.concat(this.others);
    return res;
  }

  /** Decodes and records an error response from server. */
  decode(e: AxiosError) {
    let known = false;
    if (e.response !== undefined) {
      const data = e.response.data;
      if (data instanceof Object)
        for (const [key, list] of Object.entries<string[]>(this.fields))
          if (containsKey(data, key)) {
            const arr = data[key];
            if (arr instanceof Array)
              for (const elem of arr) {
                list.push(String(elem));
                known = true;
              }
          }
    }
    if (!known) this.others.push(...printErrors(e));
  }
}
