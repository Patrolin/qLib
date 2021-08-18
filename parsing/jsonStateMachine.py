
# https://www.json.org/json-en.html
def parseElement(s: str, i: int):
  i = parseWhitespace(s, i)
  if i >= len(s): raise Exception()
  if s[i] == '{':
    r, i = z = parseObject(s, i)
  elif s[i] == '[':
    r, i = parseArray(s, i)
  elif s[i] == '"':
    r, i = parseString(s, i)
  elif s[i] in '0123456789':
    r, i = parseNumber(s, i)
  elif s[i] == 't':
    r, i = parseTrue(s, i)
  elif s[i] == 'f':
    r, i = parseFalse(s, i)
  elif s[i] == 'n':
    r, i = parseNull(s, i)
  else:
    raise Exception(repr(s[i:]))
  i = parseWhitespace(s, i)
  return r, i

def parseWhitespace(s: str, i: int):
  while i < len(s) and s[i] in ' \t\r\n':
    i += 1
  return i

def parseObject(s: str, i: int):
  i += 1
  if i >= len(s): raise Exception('unexpected EOF')
  r = dict()
  while True:
    i = parseWhitespace(s, i)
    if i >= len(s): raise Exception('unexpected EOF')
    if s[i] == '"':
      c, i = parseString(s, i)
      i = parseWhitespace(s, i)
      if i >= len(s): raise Exception('unexpected EOF')
      if s[i] == ':':
        i += 1
        e, i = parseElement(s, i)
        r[c] = e
      else: raise Exception(repr(s[:i+1]))
    elif s[i] == '}':
      return r, i
    else:
      raise Exception(repr(s[:i+1]))

def parseArray(s: str, i: int):
  i += 1
  if i >= len(s): raise Exception('unexpected EOF')
  r = []
  while True:
    c, i = parseElement(s, i)
    r.append(c)
    if i >= len(s): raise Exception('unexpected EOF')
    if s[i] == ',':
      i += 1
      if i >= len(s): raise Exception('unexpected EOF')
    elif s[i] == ']':
      i += 1
      return r, i
    else:
      raise Exception(repr(s[:i+1]))

def parseString(s: str, i: int):
  j = i
  while True:
    j += 1
    if j >= len(s): raise Exception('unexpected EOF')
    if s[j] == '"':
      return s[i+1:j], j+1
    # TODO: handle escape sequences

def parseNumber(s: str, i: int):
  j = i
  while '0' <= s[j] <= '9':
    j += 1
    if j >= len(s): return int(s[i:j]), j
  if s[j] != '.':
    return int(s[i:j]), j
  j += 1
  if j >= len(s): return float(s[i:j]), j
  while '0' <= s[j] <= '9':
    j += 1
    if j >= len(s): return float(s[i:j]), j
  return float(s[i:j]), j

def parseTrue(s: str, i: int):
  if s[i:i+4] == 'true': return True, i+4
  else: raise Exception(repr(s[:i+4]))

def parseFalse(s: str, i: int):
  if s[i:i+5] == 'false': return False, i+5
  else: raise Exception(repr(s[:i+5]))

def parseNull(s: str, i: int):
  if s[i:i+4] == 'null': return None, i+4
  else: raise Exception(repr(s[:i+4]))

print(parseElement(' { "foo": [ "hello world", 1, 3.14, false, false, null ] } ', 0))
