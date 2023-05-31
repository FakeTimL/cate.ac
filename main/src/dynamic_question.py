import json, time, random
from markdown2 import markdown


# Java-style method override validator
# https://stackoverflow.com/questions/1167617/in-python-how-do-i-indicate-im-overriding-a-method
# TODO: add this into shared library

def overrides(interface_class):
  def overrider(method):
    assert(method.__name__ in dir(interface_class))
    return method
  return overrider


# Initializing commands
# https://www.notion.so/Question-input-shortcuts-f06666a6cfc1425c9dc6cdec0f742327

init_commands = ''' # Line 1
from sympy import *
from math import gcd
import random

def in_set(*args):
  return sympify(random.choice(args))

def in_range(l, r, prec=0):
  mul = 10**prec
  return sympify(random.randrange(l * mul, r * mul)) / mul

def real_frac_in_range(l, r):
  assert(l + 1 < r)
  a, b = 0, 0
  while a == b:
    a, b = in_range(l, r), in_range(l, r)
  if a > b:
    a, b = b, a
  g = gcd(a, b)
  return (a / g, b / g)

'''


# We need this because the random seeds are stored as integers in the database
# https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.IntegerField
INTEGER_FIELD_MAX = 2147483647


class DynamicQuestion:
  ''' Dynamic question evaluator, base class
  '''
  
  initialized = False
  global_dict, local_dict = dict(), dict()
  
  @classmethod
  def init_environment(cls):
    if not DynamicQuestion.initialized:
      print("Initializing environment for dynamic question evaluator...")
      DynamicQuestion.initialized = True
      # https://stackoverflow.com/questions/12505047/why-doesnt-an-import-in-an-exec-in-a-function-work
      exec(init_commands, DynamicQuestion.global_dict, DynamicQuestion.global_dict)
  
  def __init__(self, data):
    self.data = data
    DynamicQuestion.init_environment()
    self.global_dict, self.local_dict = DynamicQuestion.global_dict, DynamicQuestion.local_dict
  
  def init_random_with_seed(self):
    ''' Ensure that self.data['seed'] is present (or generate one based on the current system time) and use this to initialize package `random`
    '''
    if 'seed' in self.data:
      assert(type(self.data['seed']) == int)
      seed = self.data['seed']
    else:
      seed = int(time.time() * 1000) % INTEGER_FIELD_MAX
      self.data['seed'] = seed
    # Setting seed is sufficient to make subsequent randomization repeatable
    # https://stackoverflow.com/questions/30745014/python-random-use-both-state-and-seed
    random.seed(seed)
  
  def eval_part(self, s):
    ''' Evaluate commands within one `<<>>` block and return evaluation result
    '''
    assert(s != '')
    if s[0] == '@': # Latex formula
      result = eval('latex(' + s[1:].strip() + ')', self.global_dict, self.local_dict)
    elif s[0] == '#': # Numerically evaluated result
      prec = 2 # Default precision
      ind = s.find(' ')
      if s[1:ind].isdigit():
        prec = int(s[1:ind])
      else:
        ind = 1
      result_float = eval('(' + s[ind:].strip() + ').evalf()', self.global_dict, self.local_dict)
      # At most `prec` digits after decimal point
      # https://stackoverflow.com/questions/14997799/most-pythonic-way-to-print-at-most-some-number-of-decimal-places
      result = (format(result_float, '.' + str(prec) + 'f').rstrip('0').rstrip('.'))
    else: # Simplified (symbolically evaluated) latex
      result = eval('latex(simplify(' + s.strip() + '))', self.global_dict, self.local_dict)
    return str(result)
  
  def execute_code(self, s):
    ''' Evaluate commands in all "<<>>" blocks in string `s` and return the replaced string.
    '''
    
    p, q = s.find('<<'), 0
    
    while p != -1:
      q = s.find('>>', p + 2)
      assert(q != -1)
      command = s[p + 2 : q]
      
      ind = command.find('|')
      if ind == -1:
        result = self.eval_part(command)
      else:
        exec(command[ind + 1 :].strip(), self.global_dict, self.local_dict)
        eval_command = command[: ind]
        if eval_command.strip() == '': # No eval command
          result = ''
          #if s[p - 1] == '\n' and s[q + 2] == '\n': # Command occupies the whole line
          #  q += 1 # Also remove the EOL character
        else:
          result = self.eval_part(eval_command)
      
      s = s[:p] + result + s[q + 2 :] # Replace command with result
      q = p + len(result) # String grew / shrank after replacement, so we need to recalculate q
      
      p = s.find('<<', q)
    
    return s
    
  def separate_blanks(self, s):
    ''' Separate contents in all "[[]]" blocks in string `s` and return the replaced string along with an array.
    '''
    
    contents = []
    index = 0
    p, q = s.find('[['), 0
    
    while p != -1:
      q = s.find(']]', p + 2)
      assert(q != -1)
      content = s[p + 2 : q].strip()
      
      num_underscores = 8
      if content != '': # #####
        num_underscores = len(content) * 2 + 8
        num_underscores = min(num_underscores, 15)
      contents.append(content)
      result = ('<a href="#blank_%d"><u>' % index) + ('(%d)' % (index + 1)).center(num_underscores, ' ').replace(' ', '&ensp;') + '</u></a>'
      index += 1
      
      s = s[:p] + result + s[q + 2 :] # Replace command with result
      q = p + len(result) # String grew / shrank after replacement, so we need to recalculate q
      
      p = s.find('[[', q)
    
    return s, contents
  
  def execute(self, s):
    ''' Evaluate commands in all "<<>>" blocks in string `s`, separates "[[]]" blocks, 
    converts markdown to HTML and return replaced string.
    '''
    return markdown(self.execute_code(s))
    
  # The following variables & methods should be considered to be implemented in subclasses
  
  #type = ''
  
  def prepare(self):
    ''' Prepare the dynamic (random) parts of the question, optionally according to a given random seed.
    
    If self.data['seed'] is present, then the random generation procedure will use its value as seed; otherwise, the random seed
    will be the current system time (in milliseconds) and will be stored in self.data['seed'].
    '''
    
    self.init_random_with_seed()
    
    # Execute commands in all text fields
    self.data['statement'] = self.execute(self.data['statement'])
    if 'explanation' in self.data:
      self.data['explanation'] = self.execute(self.data['explanation'])
  
  '''
  def get_data(self):
    return self.data
  
  def get_json_data(self):
    return json.dumps(self.data)
  '''
  
  def get_user_answers(self, request_data):
    ''' Takes a QueryDict `request_data` (GET or POST data from question forms) as input, and returns a dict of fields & values
    relevant to the user's answer to this question (e.g. { 'choices': [1, 2, 3] } for multiple choice questions).
    '''
    raise NotImplementedError('This method must be implemented in subclasses')
    return {}
  
  def validate_user_answers(self, answers):
    ''' Takes a dict (see above) of the user's answers as input, and returns whether the user's answers are correct. Additional
    information for front-end rendering (e.g. per-choice correctness if the question is a multiple choice) may be stored in
    self.data[]. The question is uniquely defined by using self.data['seed'] as the seed for the random generation procedure.
    '''
    raise NotImplementedError('This method must be implemented in subclasses')
    return None


class DynamicQuestionChoice(DynamicQuestion):
  ''' Multiple choice question, codename = 'choice'
  '''
  
  #type = 'choice'
  
  def select_choices(self):
    ''' Randomly select choices, optionally according to a given random seed. Stores results in self.data['choices_shown'].
    
    If self.data['seed'] is present, then the random generation procedure will use its value as seed; otherwise, the random seed
    will be the current system time (in milliseconds) and will be stored in self.data['seed'].
    '''
    
    assert('choices' in self.data and 'num_choices' in self.data and 'num_correct_choices' in self.data)
    self.init_random_with_seed()
    
    correct_choices, incorrect_choices = [], []
    for choice in self.data['choices']:
      if choice['is_correct']:
        correct_choices.append(choice)
      else:
        incorrect_choices.append(choice)
    
    correct_choices_shown = random.sample(correct_choices, self.data['num_correct_choices'])
    incorrect_choices_shown = random.sample(incorrect_choices, self.data['num_choices'] - self.data['num_correct_choices'])
    self.data['choices_shown'] = correct_choices_shown + incorrect_choices_shown
    random.shuffle(self.data['choices_shown'])
  
  @overrides(DynamicQuestion)
  def prepare(self):
    # TODO: AVOID COLLISION (SIMILAR VALUES) OF INCORRECT CHOICES WITH CORRECT ONES
    
    assert('choices' in self.data)
    self.init_random_with_seed()
    
    # Execute commands in all text fields
    self.data['statement'] = self.execute(self.data['statement'])
    self.data['statement'] = self.data['statement'].replace('[[]]', '________') # #####
    
    for i in range(len(self.data['choices'])):
      choice = self.data['choices'][i]
      choice['text'] = self.execute(choice['text'])
      if 'explanation' in choice:
        choice['explanation'] = self.execute(choice['explanation'])
    
    if 'explanation' in self.data:
      self.data['explanation'] = self.execute(self.data['explanation'])
    
    # Randomly select choices
    self.select_choices()
  
  @overrides(DynamicQuestion)
  def get_user_answers(self, request_data):
    return { 'choices': request_data.getlist('choices', []) }
  
  @overrides(DynamicQuestion)
  def validate_user_answers(self, answers):
    assert('choices' in self.data and 'seed' in self.data)
    assert('choices_shown' in self.data)
    
    n = self.data['num_choices']
    for i in range(n):
      self.data['choices_shown'][i]['user_chosen'] = False
    
    for x in answers.get('choices', []):
      i = int(x) - 1
      if i >= 0 and i < n:
        self.data['choices_shown'][i]['user_chosen'] = True
    
    is_correct = True
    for i in range(n):
      # 'is_correct': naming clash...
      correct_answer = True if self.data['choices_shown'][i]['is_correct'] else False
      if self.data['choices_shown'][i]['user_chosen'] != correct_answer:
        is_correct = False
    
    return is_correct


class DynamicQuestionQA(DynamicQuestion):
  ''' Q&A question, codename = 'qa'
  '''
  
  #type = 'qa'
  
  @overrides(DynamicQuestion)
  def prepare(self):
    self.init_random_with_seed()
    
    # Execute commands in all text fields
    self.data['statement'] = self.execute(self.data['statement'])
    if 'explanation' in self.data:
      self.data['explanation'] = self.execute(self.data['explanation'])
  
  @overrides(DynamicQuestion)
  def get_user_answers(self, request_data):
    return { 'answer_text': request_data['answer_text'] }
  
  @overrides(DynamicQuestion)
  def validate_user_answers(self, answers):
    self.data['user_answer'] = answers['answer_text']
    return True


class DynamicQuestionFill(DynamicQuestion):
  ''' Fill-in-the-blanks question, codename = 'fill'
  '''
  
  #type = 'fill'
  
  @overrides(DynamicQuestion)
  def prepare(self):
    self.init_random_with_seed()
    
    # Execute commands in all text fields
    s, contents = self.separate_blanks(self.execute_code(self.data['statement']))
    self.data['statement'] = markdown(s)
    if 'explanation' in self.data:
      self.data['explanation'] = self.execute(self.data['explanation'])
    
    # Store answers
    self.data['blanks'] = []
    for answer in contents:
      self.data['blanks'].append({ 'correct_answer': answer })
  
  @overrides(DynamicQuestion)
  def get_user_answers(self, request_data):
    assert('blanks' in self.data)
    n = len(self.data['blanks'])
    
    result = []
    for i in range(n):
      result.append(request_data.get('blank_' + str(i)))
    return { 'blanks': result }
  
  @overrides(DynamicQuestion)
  def validate_user_answers(self, user_answers):
    assert('blanks' in self.data)
    
    n = len(self.data['blanks'])
    
    is_correct = True
    for i in range(n):
      user_answer = '' if i >= len(user_answers['blanks']) else user_answers['blanks'][i]
      correct_answer = self.data['blanks'][i]['correct_answer']
      
      blank_is_correct = (user_answer == correct_answer) # True or false
      if user_answer == '' or correct_answer == '': # None if user did not give an answer / we do not have an answer
        blank_is_correct = None
      
      self.data['blanks'][i]['user_answer'] = user_answer
      self.data['blanks'][i]['user_is_correct'] = blank_is_correct
      
      if blank_is_correct == None:
        is_correct = None
      if blank_is_correct == False and is_correct != None:
        is_correct = False
    
    return None #is_correct # #####


def init_dynamic_question(data):
  ''' Returns an instance of an appropriate subclass of DynamicQuestion from given `data`. Uses the 'type' attribute in
  `data` to determine which subclass will be returned.
  
  Value of 'type' - subclass:
    'choice' - DynamicQuestionChoice (multiple choice)
    'qa' - DynamicQuestionQA (Q & A)
    'fill' - DynamicQuestionFill (fill-in-the-blanks)
  '''
  
  if data['type'] == 'choice':
    return DynamicQuestionChoice(data)
  elif data['type'] == 'qa':
    return DynamicQuestionQA(data)
  elif data['type'] == 'fill':
    return DynamicQuestionFill(data)
  else:
    assert False, 'Question type not supported: \'' + data['type'] + '\''


def init_dynamic_question_from_json(jsondata):
  return init_dynamic_question(json.loads(jsondata))
