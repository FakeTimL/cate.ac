# Convert Anfa question batch file into Python object

import sys, json

# When saving file with text mode, always use '\n' as line ending (on all platforms).
# Python will automatically convert line endings according to the host platform.
# https://stackoverflow.com/questions/3257869/difference-between-binary-and-text-i-o-in-python-on-windows


'''
***: new question delimiter & statement begin
---: choices begin (args: num_choices - correct_choices)
  *: correct
  -: incorrect
----: explanation begin
-----: knowledge unit list begin
  [ ]: delimiter
'''


minuses2name = { 0: 'statement', 3: 'choices', 4: 'explanation', 5: 'knowledge_units' }


def count_leading_minuses(s): # Count leading minuses
  n = 0
  for c in s:
    if c != '-':
      break
    n += 1
  return n


def read_choices(lines, begin, end): # Lines [begin, end)
  #choices = { 'correct': {}, 'incorrect': {} }
  choices = []
  p = -1
  for q in range(begin, end + 1):
    s = lines[q]
    if len(s) > 0 and (s[0] == '*' or s[0] == '-') or q == end: # New choice block [p, q)
      if p != -1:
        s = str('\n').join(lines[p:q])
        assert(s[0] == '*' or s[0] == '-')
        is_correct = (s[0] == '*')
        s = s[1:] # Remove leading '*' or '-'
        ind = s.find('::')
        '''
        if ind != -1: # Has explanation
          text, explanation = s[:ind].strip(), s[ind+2:].strip()
          choices['correct'].append({ 'text': text, 'explanation': explanation })
        else:
          text = s.strip()
          choices['incorrect'].append({ 'text': text })
        '''
        if ind != -1: # Has explanation
          text, explanation = s[:ind].strip(), s[ind+2:].strip()
          choices.append({ 'text': text, 'is_correct': is_correct, 'explanation': explanation })
        else:
          text = s.strip()
          choices.append({ 'text': text, 'is_correct': is_correct })
      p = q
  return choices


def read_question(lines, begin, end): # Lines [begin, end)
  question = {}
  p = begin - 1
  question['type'] = 'qa'
  
  for q in range(begin, end + 1):
    if count_leading_minuses(lines[q]) >= 3 or q == end: # New block [p, q)
      m = count_leading_minuses(lines[p])
      
      if m == 3: # Choices: list containing {'text', 'is_correct', 'explanation'}
        v = read_choices(lines, p + 1, q)
        # Get number of choices and correct choices
        l = [int(x.strip()) for x in lines[p].split('-') if x.strip().isdigit()]
        assert len(l) == 2
        question['type'], question['num_choices'], question['num_correct_choices'] = 'choice', l[0], l[1]
      
      elif m == 5: # Knowledge units: list
        v = str(' ').join(lines[p+1:q]).split(' ') # Split into space-separated items
        v = [x.strip() for x in v if x.strip() != ''] # Exclude empty items
      
      else: # Statement or explanation: string
        v = str('\n').join(lines[p+1:q]).strip() # Concatenate lines
        if v.find('[[') != -1:
          question['type'] = 'fill'
      
      question[minuses2name[m]] = v
      p = q
  
  return question


def anfa_convert_lines(lines):
  n = len(lines)
  result = []
  
  # Strip comments and invisible characters at the end of the lines
  for i in range(n):
    s = lines[i]
    #if s.find('//') >= 0:
    #  s = s[:s.find('//')]
    #if s.find('#') >= 0:
    #  s = s[:s.find('#')]
    lines[i] = s.rstrip('\r\n')

  
  # Parse
  lines.append('***') # Sentinel
  try:
    p, q = lines.index('***'), 0
    while True:
      q = lines.index('***', p + 1)
      result.append(read_question(lines, p + 1, q))
      p = q
  except ValueError: # No more '***' in `lines`
    pass
  
  return result


def anfa_convert(s):
  return anfa_convert_lines(s.split('\n'))


if __name__ == '__main__':
  if len(sys.argv) > 1:
    filename = sys.argv[1]
  else:
    print('Usage: python3 anfaconv.py [filename]')
    print('Note: file encoding must be UTF-8')
    exit()
  
  lines = []
  with open(filename, 'r', encoding='utf-8') as f:
    while True:
      s = f.readline()
      if s == '':
        break
      lines.append(s)
  
  result = anfa_convert_lines(lines)
  
  with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False)
