import threading
import logging
import os
import json
from time import sleep
from django.db.models.signals import post_save
from django.dispatch import receiver
import openai
import openai.error
from .models import *

logger = logging.getLogger(__name__)


# Temporary solution using threads.
# See: https://stackoverflow.com/a/11904222
# See: https://stackoverflow.com/a/11903904
class SubmissionThread(threading.Thread):
  def __init__(self, submission: Submission, **kwargs):
    self.submission = submission
    super(SubmissionThread, self).__init__(**kwargs)

  def run(self) -> bool:
    # Sending request to ChatGPT.
    max_attempts = 3
    while max_attempts > 0:
      max_attempts -= 1
      try:
        (self.submission.gpt_mark, self.submission.gpt_comments) = gpt_invoke(
          self.submission.question, self.submission.user_answer)
        self.submission.save()
        logger.info(self.submission)
        return True
      except json.JSONDecodeError as error:  # ChatGPT did not respond in valid JSON format.
        logger.warning(error)
        sleep(10)
      except ValueError as error:  # ChatGPT did not respond with a valid mark.
        logger.warning(error)
        sleep(10)
      except openai.error.RateLimitError as error:  # ChatGPT is too busy, please try again later...
        logger.warning(error)
        sleep(60)
      except openai.error.OpenAIError as error:  # Unexpected ChatGPT error: ' + str(error)
        logger.warning(error)
        sleep(60)
    return False


def gpt_invoke(question: Question, response: str) -> tuple[int, str]:
  openai.api_key = os.environ['DRP49_OPENAI_API_KEY']

  system = \
      'You are an IB examiner. You should mark the student response carefully according to the question and ' + \
      'marking criteria, and comment on how they may otherwise achieve full marks. Give your mark and comment ' + \
      'in the following JSON format: {"mark":0,"comment":""}. Make sure to respond in JSON only.\n' + \
      'Exam question:\n' + question.statement + '\n' + \
      'Marking criteria:\n' + question.gpt_prompt + '\n'
  user = 'The student\'s response:\n' + response + '\n'

  completion = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
      {'role': 'system', 'content': system},
      {'role': 'user', 'content': user},
    ]
  )
  content = completion.choices[0].message.content  # type: ignore
  feedback = json.loads(content)

  return int(float(feedback['mark']) * question.mark_denominator + 0.5), feedback['comment']
