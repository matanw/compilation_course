# calclex.py

from sly import Lexer,  Parser

class CalcLexer(Lexer):
  # Set of token names.   This is always required
  tokens = { ID, NUMBER, PLUS, MINUS, TIMES,
             DIVIDE, ASSIGN, LPAREN, RPAREN }

  # String containing ignored characters between tokens
  ignore = ' \t'

  # Regular expression rules for tokens
  ID      = r'[a-zA-Z_][a-zA-Z0-9_]*'
  NUMBER  = r'\d+'
  PLUS    = r'\+'
  MINUS   = r'-'
  TIMES   = r'\*'
  DIVIDE  = r'/'
  ASSIGN  = r'='
  LPAREN  = r'\('
  RPAREN  = r'\)'

if __name__ == '__main__1':
  data = 'x = 3 + 42 * (s - t)'
  lexer = CalcLexer()
  for tok in lexer.tokenize(data):
    print('type=%r, value=%r' % (tok.type, tok.value))



class CalcParser(Parser):
  # Get the token list from the lexer (required)
  tokens = CalcLexer.tokens

  # Grammar rules and actions
  @_('expr PLUS term')
  def expr(self, p):
    print("et->e", p.expr,'+',p.term)
    return p.expr + p.term

  @_('expr MINUS term')
  def expr(self, p):
    print("et-> e", p.expr,'-',p.term)
    return p.expr - p.term

  @_('term')
  def expr(self, p):
    print('t-> e',p.term)
    return p.term

  @_('term TIMES factor')
  def term(self, p):
    print("tf->t",p.term,'*',p.factor)
    return p.term * p.factor


  @_('term DIVIDE factor')
  def term(self, p):
    print("tf->t",p.term,'/',p.factor)
    return p.term / p.factor

  @_('factor')
  def term(self, p):
    print("f->t", p.factor)
    return p.factor

  @_('NUMBER')
  def factor(self, p):
    print("numm->f", p.NUMBER)
    return int(p.NUMBER)

  @_('LPAREN expr RPAREN')
  def factor(self, p):
    print("(e)->f", p.expr)
    return p.expr

  def error(self, p):

    print("Whoa. You are seriously hosed.", p)
    next(self.tokens)
    self.errok()
    if not p:

      print("End of File!")
      return

if __name__ == '__main__':
  lexer = CalcLexer()
  parser = CalcParser()

  while True:
    try:
      text = input('calc > ')
      result = parser.parse(lexer.tokenize(text))
      print(result)
    except EOFError:
      break

if False:

  @_('term TIMES error')
  def term(self, p):
    print("tr->t")
    return 50