import axios from 'axios';

// API client configuration.

export const api = axios.create({
  baseURL: '/api/',
  withCredentials: true,
  xsrfHeaderName: 'X-CSRFTOKEN',
  xsrfCookieName: 'csrftoken',
  // timeout: 10000,
});

// API schemas.

export interface Credential {
  username: string;
  password: string;
}

export interface User {
  pk: number;
  username: string;
  password: string | null;
  email: string | null;
  avatar: string;
  first_name: string;
  last_name: string;
  bio: string;
  date_joined: string;
  last_login: string;
  admin: boolean | null;
}

export interface Feedback {
  pk: number;
  text: string;
  email: string;
  publish_date: string;
}

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
  user: number;
  question: number;
  user_answer: string;
  gpt_mark: number;
  gpt_comments: string;
  date: string;
}

// Common API calls.

export async function markdownHtml(markdown: string): Promise<string> {
  return (await api.post('main/markdown_html/', { markdown: markdown })).data.html;
}
