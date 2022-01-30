from __future__ import annotations
from dataclasses import dataclass
from typing import List
import enums


@dataclass
class Program():
  declarations: List[Declaration]
  stmts: List[Stmt]


@dataclass
class Declaration():
  ids: List[str]
  var_type: enums.VarType
  lineno: int


@dataclass
class Stmt():
  pass


@dataclass
class AssigmentStmt(Stmt):
  var_name: str
  value: Expression
  lineno: int


@dataclass
class InputStmt(Stmt):
  var_name: str
  lineno: int

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
class CaseOption:
  val: str
  stmts: List[Stmt]
  lineno: int


@dataclass
class SwitchStmt(Stmt):
  exp: Expression
  cases: List[CaseOption]
  default_stmts: List[Stmt]
  lineno: int


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
  op: enums.ComparisionOperation


@dataclass
class BinaryOperationBooleanExpretion(BooleanExpression):
  boolean_expression1: BooleanExpression
  boolean_expression2: BooleanExpression
  op: enums.BooleanBinaryOp


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
  op: enums.BinaryOp


@dataclass
class VarExpression(Expression):
  var_name: str


@dataclass
class NumExpression(Expression):
  num: str


@dataclass
class CastExpression(Expression):
  target: enums.VarType
  expression: Expression
