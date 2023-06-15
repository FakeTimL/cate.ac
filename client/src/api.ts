import axios from 'axios';

export const api = axios.create({
  baseURL: '/api/',
  withCredentials: true,
  xsrfHeaderName: 'X-CSRFTOKEN',
  xsrfCookieName: 'csrftoken',
  timeout: 1000,
});

// API schemas.

export interface Topic {
  pk: number;
  name: string;
  parent: number | null;
  children: number[];
  questions: number[];
  resources: string;
}

export interface Question {
  pk: number;
  statement: string;
  mark_denominator: number;
  mark_minimum: number;
  mark_maximum: number;
  mark_scheme: string;
  gpt_prompt: string;
  topics: number[];
}

export interface Submission {
  pk: number;
  user_answer: string;
  gpt_mark: number;
  gpt_comments: string;
  date: string;
}

export async function markdownHtml(markdown: string): Promise<string> {
  return (await api.post('main/markdown_html/', { markdown: markdown })).data.html;
}
