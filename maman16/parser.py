import lexer, program_errors,tree_nodes

import sly

class Parser(sly.Parser):
  tokens = lexer.get_token_set()

  def __init__(self, error_manager: program_errors.ErrorsManager, files_lines: int):
    super().__init__()
    self.error_manager = error_manager
    self.files_lines = files_lines

  @_('declarations stmt_block')
  def program(self, p):
    return tree_nodes.Program(declarations=p.declarations,stmts=p.stmt_block)

  @_('declarations declaration')
  def declarations(self, p):
    return p.declarations + [p.declaration]

  @_('')
  def declarations(self, p):
    return []

  @_('idlist ":" type ";"')
  def declaration(self, p):
    return tree_nodes.Declaration(ids=p.idlist,var_type=p.type, lineno=p.lineno)

  @_('INT')
  def type(self, p):
    return p.INT

  @_('FLOAT')
  def type(self, p):
    return p.FLOAT

  @_('idlist "," ID')
  def idlist(self, p):
    return p.idlist + [p.ID]

  @_('ID')
  def idlist(self, p):
    return [p.ID]

  @_('assignment_stmt')
  def stmt(self, p):
    return [p.assignment_stmt]

  @_('input_stmt')
  def stmt(self, p):
    return [p.input_stmt]

  @_('output_stmt')
  def stmt(self, p):
    return [p.output_stmt]

  @_('if_stmt')
  def stmt(self, p):
    return [p.if_stmt]

  @_('while_stmt')
  def stmt(self, p):
    return [p.while_stmt]

  @_('switch_stmt')
  def stmt(self, p):
    return [p.switch_stmt]

  @_('break_stmt')
  def stmt(self, p):
    return [p.break_stmt]

  @_('stmt_block')
  def stmt(self, p):
    return p.stmt_block

  @_('ID "=" expression ";"')
  def assignment_stmt(self, p):
    return tree_nodes.AssigmentStmt(var_name=p.ID, value=p.expression, lineno=p.lineno)

  @_('INPUT "(" ID ")" ";"')
  def input_stmt(self, p):
    return tree_nodes.InputStmt(var_name=p.ID, lineno=p.lineno)

  @_('OUTPUT "(" expression ")" ";"')
  def output_stmt(self, p):
    return tree_nodes.OutputStmt(value=p.expression)

  @_('IF "(" boolexpr ")" stmt ELSE stmt')
  def if_stmt(self, p):
    return tree_nodes.IfStmt(
        condition=p.boolexpr,
        true_stmts=p.stmt0,
        false_stms=p.stmt1,
    )

  @_('WHILE "(" boolexpr ")" stmt')
  def while_stmt(self, p):
    return tree_nodes.WhileStmt(
        condition=p.boolexpr,
        body_stmts=p.stmt
    )

  @_('SWITCH "(" expression ")" "{" caselist DEFAULT ":" stmtlist "}"')
  def switch_stmt(self, p):
    return tree_nodes.SwitchStmt(exp=p.expression,
                                 cases=p.caselist,
                                 default_stmts=p.stmtlist, lineno=p.lineno)

  @_('caselist CASE NUM ":" stmtlist')
  def caselist(self, p):
    case_option = tree_nodes.CaseOption(val=p.NUM, stmts=p.stmtlist, lineno=p.lineno)
    return p.caselist + [case_option]

  @_('')
  def caselist(self, p):
    return []

  @_('BREAK ";"')
  def break_stmt(self, p):
    return tree_nodes.BreakStmt(lineno=p.lineno)

  @_('"{" stmtlist "}"')
  def stmt_block(self, p):
    return p.stmtlist

  @_('stmtlist stmt')
  def stmtlist(self, p):
    return p.stmtlist + p.stmt

  @_('')
  def stmtlist(self, p):
    return []

  @_('boolexpr OR boolterm')
  def boolexpr(self, p):
    return tree_nodes.BinaryOperationBooleanExpretion(
        boolean_expression1=p.boolexpr,
        boolean_expression2=p.boolterm,
        op=p.OR
    )

  @_('boolterm')
  def boolexpr(self, p):
    return p.boolterm

  @_('boolterm AND boolfactor')
  def boolterm(self, p):
    return tree_nodes.BinaryOperationBooleanExpretion(
        boolean_expression1=p.boolterm,
        boolean_expression2=p.boolfactor,
        op=p.AND
    )

  @_('boolfactor')
  def boolterm(self, p):
    return p.boolfactor

  @_('NOT "(" boolexpr ")"')
  def boolfactor(self, p):
    return tree_nodes.NotOperationBooleanExpretion(
        inner_boolean_expression=p.boolexpr
    )

  @_('expression RELOP expression')
  def boolfactor(self, p):
    return tree_nodes.SimpleBooleanExpression(
        expression1=p.expression0,
        expression2=p.expression1,
        op=p.RELOP
    )

  @_('expression ADDOP term')
  def expression(self, p):
    return tree_nodes.BinaryOperationExpression(
        expression1=p.expression,
        expression2=p.term,
        op=p.ADDOP
    )

  @_('term')
  def expression(self, p):
    return p.term

  @_('term MULOP factor')
  def term(self, p):
    return tree_nodes.BinaryOperationExpression(
        expression1=p.term,
        expression2=p.factor,
        op=p.MULOP
    )

  @_('factor')
  def term(self, p):
    return p.factor

  @_('"(" expression ")"')
  def factor(self, p):
    return p.expression

  @_('CAST "(" expression ")"')
  def factor(self, p):
    return tree_nodes.CastExpression(
        target=p.CAST,expression=p.expression)

  @_('ID')
  def factor(self, p):
    return tree_nodes.VarExpression(var_name=p.ID, lineno=p.lineno)

  @_('NUM')
  def factor(self, p):
    return tree_nodes.NumExpression(num=p.NUM)

  def error(self, tok):
    if tok is not None:
      self.error_manager.add_parser_error(tok.lineno, f"Invalid token: {tok.type}")
    else:
      self.error_manager.add_parser_error(self.files_lines, "Files cannot ended here")
    while True:
      tok = next(self.tokens, None)
      if not tok or tok.type == ';':
        self.errok()
        return tok