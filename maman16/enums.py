from enum import Enum

class VarType(Enum):
  INT = 'INT'
  FLOAT = 'FLOAT'
  UNKNOWN = 'UNKNOWN' #used  in case of semantic error

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
  LESS_EQUAL = 'LESS_EQUAL'
  GREAT_EQUAL = 'GREAT_EQUAL'
  LESS = 'LESS'
  GREAT = 'GREAT'
