from enum import Enum

class TokenType(Enum):
  Root = 0
  Int = 1
  Float = 2
  Plus = 3
  Minus = 4
  Star = 5
  Slash = 6
  LeftBracket = 7
  RightBracket = 8

class Token:
  def __init__(self, tokenType: TokenType, value=None):
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
      i = i + 1
    elif s[i] in '-':
      res.append(Token(TokenType.Minus))
      i = i + 1
    elif s[i] in '*':
      res.append(Token(TokenType.Star))
      i = i + 1
    elif s[i] in '/':
      res.append(Token(TokenType.Slash))
      i = i + 1
    elif s[i] in '(':
      res.append(Token(TokenType.LeftBracket))
      i = i + 1
    elif s[i] in ')':
      res.append(Token(TokenType.RightBracket))
      i = i + 1
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
print(tokenize('123 - 2 3.14'))

class Node:
  def __init__(self, tokenType: TokenType, priority: int):
    self.type = tokenType
    self.priority = priority
    self.parent = None
    self.right = None
    self.left = None
    self.value = None

  def set_left(self, node):
    node.parent = self
    self.left = node
    return node

  def set_right(self, node):
    node.parent = self
    self.right = node
    return node

  def drop_left(self, node):
    self.parent.set_right(node)
    node.set_left(self)
    return node

  def repr(self, depth=0):
    newline = "\n"
    value = " "+repr(self.value) if TokenType.Int.value <= self.type.value <= TokenType.Float.value else ""
    left = self.left.repr(depth + 1) if self.left != None else f'\n{(depth+1)*"  "}None'
    right = self.right.repr(depth + 1) if self.right != None else f'\n{(depth+1)*"  "}None'
    return f'{newline if depth > 0 else ""}{depth*"  "}{self.type}<{self.priority}>{value}{left}{right}'

  def __repr__(self):
    return self.repr()

TOKEN_PRIORITY = {
  TokenType.Root.value: 0,
  TokenType.LeftBracket.value: 0,
  TokenType.RightBracket.value: 1,
  TokenType.Plus.value: 2,
  TokenType.Minus.value: 2,
  TokenType.Star.value: 3,
  TokenType.Slash.value: 3,
  TokenType.Int.value: 4,
  TokenType.Float.value: 4,
}
LOWEST_PRIORITY = 0
RIGHT_BRACKET_PRIORITY = 1
ADDITION_PRIORITY = 2
MULTIPLICATION_PRIORITY = 3
BLANK_MULTIPLICATION_PRIORITY = 4
HIGHEST_PRIORITY = 5

def parse(l: list, start=0):
  # return root of AST
  root = Node(TokenType.Root, 0)
  previous = root
  while True:
    # parse Literal | UnaryOp
    while True:
      if TokenType.Int.value <= l[start].type.value <= TokenType.Float.value:
        node = Node(l[start].type, HIGHEST_PRIORITY)
        node.value = l[start].value
        previous = previous.set_right(node)
        start += 1
        if start >= len(l):
          return root
        break
      elif TokenType.Plus.value <= l[start].type.value <= TokenType.Minus.value or l[start].type.value == TokenType.LeftBracket.value:
        # reject invalid UnaryOps?
        previous = previous.set_right(Node(l[start].type, TOKEN_PRIORITY[l[start].type.value]))
        start += 1
        if start >= len(l):
          return root
      else:
        raise Exception(f'invalid unary operator TokenType.{l[start].type.name}')

    # parse BinaryOp
    while True:
      while previous.parent.priority >= TOKEN_PRIORITY[l[start].type.value]: # '>=' is left-associative; '>' would be right-associative
        previous = previous.parent
      if TokenType.Int.value <= l[start].type.value <= TokenType.Float.value:
        previous = previous.drop_left(Node(TokenType.Star, BLANK_MULTIPLICATION_PRIORITY))
        node = Node(l[start].type, HIGHEST_PRIORITY)
        node.value = l[start].value
        previous = previous.set_right(node)
        start += 1
        if start >= len(l):
          return root
      elif l[start].type.value == TokenType.LeftBracket.value:
        previous = previous.drop_left(Node(TokenType.Star))
        node = Node(l[start].type, LOWEST_PRIORITY)
        node.value = l[start].value
        previous = previous.set_right(node)
        start += 1
        if start >= len(l):
          return root
        break
      elif l[start].type.value == TokenType.RightBracket.value:
        previous = previous.parent
        if previous.type.value == TokenType.Root.value:
          node = Node(TokenType.LeftBracket, LOWEST_PRIORITY)
          node.set_right(previous.right)
          previous = previous.set_right(node)
        start += 1
        if start >= len(l):
          return root
      elif TokenType.Plus.value <= l[start].type.value <= TokenType.Minus.value:
        previous = previous.drop_left(Node(l[start].type, ADDITION_PRIORITY))
        start += 1
        if start >= len(l):
          return root
        break
      elif TokenType.Star.value <= l[start].type.value <= TokenType.Slash.value:
        previous = previous.drop_left(Node(l[start].type, MULTIPLICATION_PRIORITY))
        start += 1
        if start >= len(l):
          return root
        break

#print(parse(tokenize('1+1*2')))
#print(parse(tokenize('1*1+2')))
#print(parse(tokenize('(1+1)*2')))
#print(parse(tokenize('1-2+3-4+5')))
print(parse(tokenize('1*(2+3) / 4*(5+6)')))