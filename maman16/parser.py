import lexer, errror_logger

import sly
class Parser(sly.Parser):
  # Get the token list from the lexer (required)
  tokens = lexer.Lexer.tokens
  @_('')
  def stmts(self, p):
    return []

  @_('stmts ";" expr')
  def stmts(self, p):
    return p.stmts + [p.expr]

  @_('ID "=" ID')
  def expr(self, p):
    return (p.ID0, p.ID1)

if __name__ == '__main__':

  text = ';aaa = ddd ; fff=5 ; fff=h '
  parser = Parser()
  result = parser.parse(lexer.get_filtered_tokrens(text, error_logger=errror_logger.ErrorLogger()))
  print(result)


