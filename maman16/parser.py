import lexer

import sly
class Parser(sly.Parser):
  # Get the token list from the lexer (required)
  tokens = lexer.LexerHelper.tokens

  # Grammar rules and actions
  @_('ID "=" ID')
  def expr(self, p):
    print(p.ID0)
    return (p.ID0, p.ID1)

if __name__ == '__main__':

  text = 'aaa = /****456****/ & bbb'
  lexer = lexer.Lexer(text, lexer.ErrorLogger())
  parser = Parser()
  result = parser.parse(lexer.get_generator())
  print(result)


