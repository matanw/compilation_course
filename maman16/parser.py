import lexer, errror_logger

import sly
class Parser(sly.Parser):
  tokens = lexer.get_token_set()

  @_('declarations stmt_block')
  def program(self, p):
    return []

  @_('declarations declaration')
  def declarations(self, p):
    return []

  @_('')
  def declarations(self, p):
    return []

  @_('idlist ":" type ";"')
  def declaration(self, p):
    return []

  @_('INT')
  def type(self, p):
    return []

  @_('FLOAT')
  def type(self, p):
    return []

  @_('idlist "," ID')
  def idlist(self, p):
    return []

  @_('ID')
  def idlist(self, p):
    return []

  @_('assignment_stmt')
  def stmt(self, p):
    return []

  @_('input_stmt')
  def stmt(self, p):
    return []

  @_('output_stmt')
  def stmt(self, p):
    return []

  @_('if_stmt')
  def stmt(self, p):
    return []

  @_('while_stmt')
  def stmt(self, p):
    return []

  @_('switch_stmt')
  def stmt(self, p):
    return []

  @_('break_stmt')
  def stmt(self, p):
    return []

  @_('stmt_block')
  def stmt(self, p):
    return []

  @_('ID "=" expression ";"')
  def assignment_stmt(self, p):
    return []

  @_('INPUT "(" ID ")" ";"')
  def input_stmt(self, p):
    return []

  @_('OUTPUT "(" expression ")" ";"')
  def output_stmt(self, p):
    return []

  @_('IF ")" boolexpr "(" stmt ELSE stmt')
  def if_stmt(self, p):
    return []

  @_('WHILE ")" boolexpr "(" stmt')
  def while_stmt(self, p):
    return []

  @_('SWITCH "(" expression ")" "{" caselist DEFAULT ":" stmtlist "}"')
  def switch_stmt(self, p):
    return []

  @_('caselist CASE NUM ":" stmtlist')
  def caselist(self, p):
    return []

  @_('')
  def caselist(self, p):
    return []

  @_('BREAK ";"')
  def break_stmt(self, p):
    return []

  @_('"{" stmtlist "}"')
  def stmt_block(self, p):
    return []

  @_('stmtlist stmt')
  def stmtlist(self, p):
    return []

  @_('')
  def stmtlist(self, p):
    return []

  @_('boolexpr OR boolterm')
  def boolexpr(self, p):
    return []

  @_('boolterm')
  def boolexpr(self, p):
    return []

  @_('boolterm AND boolfactor')
  def boolterm(self, p):
    return []

  @_('boolfactor')
  def boolterm(self, p):
    return []

  @_('NOT "(" boolexpr ")"')
  def boolfactor(self, p):
    return []

  @_('expression RELOP expression')
  def boolfactor(self, p):
    return []

  @_('expression ADDOP term')
  def expression(self, p):
    return []

  @_('term')
  def expression(self, p):
    return []

  @_('term MULOP factor')
  def term(self, p):
    return []

  @_('factor')
  def term(self, p):
    return []

  @_('"(" expression ")"')
  def factor(self, p):
    return []

  @_('CAST "(" expression ")"')
  def factor(self, p):
    return []

  @_('ID')
  def factor(self, p):
    return []

  @_('NUM')
  def factor(self, p):
    return []


if __name__ == '__main__':

  text = '{break;}'
  parser = Parser()
  result = parser.parse(lexer.get_filtered_tokrens(text, error_logger=errror_logger.ErrorLogger()))
  print(result)


