import lexer

import sly
class Parser(sly.Parser):
  # Get the token list from the lexer (required)
  tokens = lexer.LexerHelper.tokens

  # Grammar rules and actions
  @_('ID "=" ID')
  def expr(self, p):
    return (p.ID0, p.ID1)


if __name__ == '__main__':
  lexer = lexer.LexerHelper()
  parser = Parser()
  text = 'aaa = bbb'
  result = parser.parse(lexer.tokenize(text))
  print(result)
