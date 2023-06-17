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

export interface Message {
  pk: number;
  sender: number;
  receiver: number;
  content: string;
  date: string;
}

export interface Feedback {
  pk: number;
  text: string;
  email: string;
  date: string;
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

export interface Sheet {
  pk: number;
  user: number;
  sheet_questions: { question: number; index: number }[];
  time_limit: string;
  name: string;
  description: string;
}

export interface Submission {
  pk: number;
  user: number;
  question: number;
  user_answer: string;
  gpt_mark: number | null;
  gpt_comments: string;
  date: string;
}

export interface Attempt {
  pk: number;
  user: number;
  attempt_submissions: { submission: number; index: number }[];
  sheet: number | null;
  time_limit: string;
  begin_time: string;
  end_time: string | null;
}

// Common API calls.

export async function markdownHtml(markdown: string): Promise<string> {
  return (await api.post('main/markdown_html/', { markdown: markdown })).data.html;
}
