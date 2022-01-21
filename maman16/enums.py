from enum import Enum

class VarType(Enum):
  INT = 'INT'
  FLOAT = 'FLOAT'

class BinaryOp(Enum):
  ADD = 'ADD'
  SUB = 'SUB'
  MUL = 'MUL'
  DIV = 'DIV'

class BooleanBinaryOp(Enum):
  OR = 'OR'
  AND = 'AND'

class ComparisionOperation(Enum):
  EQUAL = 'EQUAL'
  NOT_EQUAL = 'NOT_EQUAL'
  SMALLAR_EQUAL = 'SMALLAR_EQUAL'
  BIGGER_EQUAL = 'BIGGER_EQUAL'
  SMALLER = 'SMALLER'
  BIGGER = 'BIGGER'
