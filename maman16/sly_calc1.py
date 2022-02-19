# calclex.py

from sly import Lexer,  Parser

class CalcLexer(Lexer):
  # Set of token names.   This is always required
  tokens = { A, B, C,SEP}

  # String containing ignored characters between tokens
  ignore = ' \t'

  A  = r'a'
  B    = r'b'
  C   = r'c'
  SEP   = r';'

if __name__ == '__main__1':
  data = 'x = 3 + 42 * (s - t)'
  lexer = CalcLexer()
  for tok in lexer.tokenize(data):
    print('type=%r, value=%r' % (tok.type, tok.value))



class CalcParser(Parser):
  # Get the token list from the lexer (required)
  tokens = CalcLexer.tokens

  # Grammar rules and actions
  @_('stmts')
  def prog(self, p):
    print("stmts->p")
    return p.stmts

  @_('stmt SEP stmts')
  def stmts(self, p):
    print("stmt ;->stmt")
    return [p.stmt] +p.stmts

  @_('')
  def stmts(self, p):
    print(' "" ->stmts')
    return []

  @_('A')
  def stmt(self, p):
    print("A-> stmts")
    return 'a'

  @_('B')
  def stmt(self, p):
    print("A-> stmts")
    return 'b'

  @_('C')
  def stmt(self, p):
    print("C-> stmts")
    return 'c'

  def error(self, tok):
    print(f"error: {tok}")
    # Read ahead looking for a terminating ";"
    while True:
      tok = next(self.tokens, None)           # Get the next token
      if not tok or tok.type == 'SEP':
        break
      self.errok()

    # Return SEMI to the parser as the next lookahead token
    return tok
if __name__ == '__main__':
  lexer = CalcLexer()
  parser = CalcParser()
  result = parser.parse(lexer.tokenize('a;b; c  c; c;c;'))
  print(result)


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