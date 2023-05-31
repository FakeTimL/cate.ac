from django.utils import timezone
import datetime
from ..models import QuestionSchedule

# According to:
# https://www.notion.so/Queue-and-Mastery-Points-08f8bd1bace54ba287f78513b7c1e890

def update_question_schedule(qs, is_correct):
  ''' Update & save / delete QuestionSchedule `qs` in-place (create new QuestionSchedules if needed), given whether the user
  has got correct on this question recently.
  '''
  
  if qs.stage == '': # Empty for "just learned"
    if is_correct:
      qs.stage = 'scheduled_review_correct'
      qs.time = timezone.now() + datetime.timedelta(days=7) # A week later
    else:
      qs.stage = 'scheduled_review_incorrect'
      qs.time = timezone.now() + datetime.timedelta(days=7)
    qs.save() # Update in database
    
  elif qs.stage == 'scheduled_review_incorrect': # Scheduled for review, previously got incorrect
    if is_correct:
      qs.stage = 'scheduled_review_correct'
      qs.time = timezone.now() + datetime.timedelta(days=1) # A day later
    else:
      qs.stage = 'scheduled_review_incorrect'
      qs.time = timezone.now() + datetime.timedelta(hours=4) # Four hours later
    qs.save()
    
  elif qs.stage == 'scheduled_review_correct': # Scheduled for review, previously got correct
    if is_correct:
      qs.delete() # Discard (delete from database)
    else:
      qs.stage = 'scheduled_review_incorrect'
      qs.time = timezone.now() + datetime.timedelta(days=1) # A day later
      qs.save()
    