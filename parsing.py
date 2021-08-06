from enum import Enum

class TokenType(Enum):
  Int = 0
  Float = 1
  Plus = 2
  Minus = 3
  Star = 4
  Slash = 5
  LeftBracket = 6
  RightBracket = 7

class Token:
  def __init__(self, tokenType: TokenType, value = None):
    self.type = tokenType
    self.value = value
  def __repr__(self):
    return repr(self.value) if self.value != None else f'TokenType.{self.type.name}'

def tokenize(s: str) -> list:
  res = []
  i = 0
  while i < len(s):
    if '0' <= s[i] <= '9':
      end, tokenType = tokenizeNumber(s, i)
      subs = s[i:end]
      res.append(Token(tokenType, int(subs) if tokenType == TokenType.Int else float(subs)))
      i = end
    elif s[i] in '+':
      res.append(Token(TokenType.Plus))
      i = i+1
    elif s[i] in '-':
      res.append(Token(TokenType.Minus))
      i = i+1
    elif s[i] in '*':
      res.append(Token(TokenType.Star))
      i = i+1
    elif s[i] in '/':
      res.append(Token(TokenType.Slash))
      i = i+1
    elif s[i] in '(':
      res.append(Token(TokenType.LeftBracket))
      i = i+1
    elif s[i] in ')':
      res.append(Token(TokenType.RightBracket))
      i = i+1
    elif s[i] == ' ':
      i += 1
      continue
    else:
      raise Exception(s[i:])
  return res

def tokenizeNumber(s: str, start: int) -> int:
  i = start
  while '0' <= s[i] <= '9':
    i += 1
    if i >= len(s): return i, TokenType.Int
  if s[i] != '.':
    return i, TokenType.Int
  i += 1
  if i >= len(s): return i, TokenType.Float
  while '0' <= s[i] <= '9':
    i += 1
    if i >= len(s): return i, TokenType.Float
  return i, TokenType.Float

print(tokenize('123'))
print(tokenize('123.'))
print(tokenize('123.0'))
print(tokenize('123+3.14'))
print(tokenize('123 + 3.14'))
print(tokenize('123 + 3.14 * -2'))

class UnaryOp:
  def __init__(self, tokenType: TokenType):
    self.type = tokenType
    self.right = None

class BinaryOp:
  def __init__(self, tokenType: TokenType):
    self.type = tokenType
    self.left = None
    self.right = None

def parse(l: list, start = 0):
  previous = None
  priority = 0
  while:
    if previous == None:
      if TokenType.Int <= l[start].type <= TokenType.Float:
        previous = l[start]
        start += 1
      elif TokenType.Plus <= l[start].type <= TokenType.Minus:
        previous = UnaryOp(l[start].type)
    else:
      pass
