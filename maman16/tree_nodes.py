from __future__ import annotations
from dataclasses import dataclass
from typing import List
from enum import Enum

class VarType(Enum):
  INT = 'INT'
  FLOAT = 'FLOAT'

@dataclass
class Program():
  declarations: List[Declaration]
  stmts: List[Stmt]

@dataclass
class Declaration():
  ids: List[str]
  var_type: VarType

@dataclass
class Stmt():
  pass

@dataclass
class AssigmentStmt(Stmt):
  var_name: str
  value: Expression

@dataclass
class InputStmt(Stmt):
  var_name: str

@dataclass
class OutputStmt(Stmt):
  value: Expression

@dataclass
class IfStmt(Stmt):
  condition: BooleanExpression
  true_stmts: List[Stmt]
  false_stms: List[Stmt]

@dataclass
class WhileStmt(Stmt):
  condition: BooleanExpression
  body_stmts: List[Stmt]

@dataclass
class CaseOption():
  val:  int #todo: represent num
  stmts: List[Stmt]

@dataclass
class SwitchStmt(Stmt):
  exp: Expression
  cases: List[CaseOption]
  default_stmts: List[Stmt]


@dataclass
class BreakStmt(Stmt):
  pass


@dataclass
class BooleanExpression():
  pass

@dataclass
class SimpleBooleanExpression(BooleanExpression):
  expression1: Expression
  expression2: Expression
  op: str #todo: ennu

@dataclass
class BinaryOperationBooleanExpretion(BooleanExpression):
  boolean_expression1: BooleanExpression
  boolean_expression2: BooleanExpression
  op: str #todo: ennu

@dataclass
class NotOperationBooleanExpretion(BooleanExpression):
  inner_boolean_expression: BooleanExpression

@dataclass
class Expression():
  pass

@dataclass
class BinaryOperationExpression(Expression):
  expression1: Expression
  expression2: Expression
  op: str #todo: ennu

@dataclass
class VarExpression(Expression):
  var_name: str

@dataclass
class NumExpression(Expression):
  num: str #todo

@dataclass
class CastExpression(Expression):
  target: str #todo
  expression: Expression


