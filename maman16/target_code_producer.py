from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple
import generator, tree_nodes, enums, errror_logger

@dataclass
class TargetOp:
  pass

@dataclass
class TargetStmt(TargetOp):
  stmt: str # can have one %s for label
  label_to_insert: Optional[str] = None # label to add in stmt

@dataclass
class TargetLabel(TargetOp):
  label_name: str

@dataclass
class ExpressionResult:
  result_var: str
  result_type: enums.VarType
  stmts: List[TargetOp]

@dataclass
class BooleanExpressionResult:
  result_var: str
  stmts: List[TargetOp]

def get_assigment_target_stmt(var_to_assign: str, var_value: str,
    vars_type: enums.VarType) -> TargetStmt:
  cmd = "IASN" if vars_type == enums.VarType.INT else "RASN"
  return TargetStmt(f"{cmd} {var_to_assign} {var_value}")

def get_print_target_stmt(var: str,
    var_type: enums.VarType) -> TargetStmt:
  cmd = "IPRT" if var_type == enums.VarType.INT else "RPRT"
  return TargetStmt(f"{cmd} {var}")

def get_read_target_stmt(var: str,
    var_type: enums.VarType) -> TargetStmt:
  cmd = "IINP" if var_type == enums.VarType.INT else "RINP"
  return TargetStmt(f"{cmd} {var}")

def get_set_1_if_equals_target_stmt(var1: str, var2: str,
    var_result: str, vars_type: enums.VarType) -> TargetStmt:
  cmd = "IEQL" if vars_type == enums.VarType.INT else "REQL"
  return TargetStmt(f"{cmd} {var_result} {var1} {var2}")

def get_set_1_if_not_equals_target_stmt(var1: str, var2: str,
    var_result: str, vars_type: enums.VarType) -> TargetStmt:
  cmd = "INQL" if vars_type == enums.VarType.INT else "RNQL"
  return TargetStmt(f"{cmd} {var_result} {var1} {var2}")

def get_set_1_if_less_target_stmt(var1: str, var2: str,
    var_result: str, vars_type: enums.VarType) -> TargetStmt:
  cmd = "ILSS" if vars_type == enums.VarType.INT else "RLSS"
  return TargetStmt(f"{cmd} {var_result} {var1} {var2}")

def get_set_1_if_great_target_stmt(var1: str, var2: str,
    var_result: str, vars_type: enums.VarType) -> TargetStmt:
  cmd = "IGRT" if vars_type == enums.VarType.INT else "RGRT"
  return TargetStmt(f"{cmd} {var_result} {var1} {var2}")

def get_add_target_stmt(var1: str, var2: str,
    var_result: str, vars_type: enums.VarType) -> TargetStmt:
  cmd = "IADD" if vars_type == enums.VarType.INT else "RADD"
  return TargetStmt(f"{cmd} {var_result} {var1} {var2}")

def get_sub_target_stmt(var1: str, var2: str,
    var_result: str, vars_type: enums.VarType) -> TargetStmt:
  cmd = "ISUB" if vars_type == enums.VarType.INT else "RSUB"
  return TargetStmt(f"{cmd} {var_result} {var1} {var2}")

def get_mul_target_stmt(var1: str, var2: str,
    var_result: str, vars_type: enums.VarType) -> TargetStmt:
  cmd = "IMLT" if vars_type == enums.VarType.INT else "RMLT"
  return TargetStmt(f"{cmd} {var_result} {var1} {var2}")

def get_div_target_stmt(var1: str, var2: str,
    var_result: str, vars_type: enums.VarType) -> TargetStmt:
  cmd = "IDIV" if vars_type == enums.VarType.INT else "RDIV"
  return TargetStmt(f"{cmd} {var_result} {var1} {var2}")

def get_covert_type_target_stmt(source_var: str, target_var: str,
    target_type: enums.VarType) -> TargetStmt:
  cmd = "RTOI" if target_type == enums.VarType.INT else "ITOR"
  return TargetStmt(f"{cmd} {target_var} {source_var}")

def get_jump_stmt(label: str) -> TargetStmt:
  return TargetStmt(f"JUMP %s", label_to_insert=label)

def get_jump_if_zero_stmt(var: str, label: str) -> TargetStmt:
  return TargetStmt(f"JMPZ %s {var}", label_to_insert=label)

def get_halt_stmt() -> TargetStmt:
  return TargetStmt("HALT")


def to_target_var_name(source_var_name: str) -> str:
  return f"source_{source_var_name}"



#todo: move aff all log_error, handle  line and return value
class TargetCodeProducer:

  def __init__(self, error_logger: errror_logger.ErrorLogger):
    self.error_logger = error_logger
    self.varname_to_type : Dict[str, enums.VarType] = dict()
    self.label_generator = generator.Generator("L")
    self.var_generator = generator.Generator("t")

  def get_code(self, program: tree_nodes.Program) -> str:
    self.handle_declerations(program.declarations)
    target_ops = self.handle_stmts(program.stmts, None)
    target_ops.append(get_halt_stmt())
    #todo if errors exit
    target_stmts, label_dict = self.filter_out_labels(target_ops)
    final_code = self.get_final_code(target_stmts, label_dict)
    return final_code

  def filter_out_labels(self, target_ops: List[TargetOp]
  ) -> Tuple[List[TargetStmt], Dict[str, int]]:
    target_stmts: List[TargetStmt] = []
    label_dict: Dict[str,int] = {}
    for i, op in enumerate(target_ops):
      if isinstance(op, TargetStmt):
        target_stmts.append(op)
      else:
        label_dict[op.label_name] = len(target_stmts) +1
    return target_stmts, label_dict

  def get_final_code(self,  target_stmts: List[TargetStmt],
      label_dict: Dict[str,int]) -> str:
    lines : List[str] = []
    for stmt in target_stmts:
      if stmt.label_to_insert is None:
        lines.append(stmt.stmt)
      else:
        lines.append(stmt.stmt % label_dict[stmt.label_to_insert])
    return "\n".join(lines)


  def handle_declerations(self, declerations: List[tree_nodes.Declaration]) ->  None:
    for decleration in declerations:
      for id in decleration.ids:
        if id in self.varname_to_type:
          self.error_logger.log_error(f"duplicate var{id}")
        self.varname_to_type[id] = decleration.var_type

  def handle_stmts(self, stmts: List[tree_nodes.Stmt],
      label_for_break: Optional[str]) -> List[TargetOp]:
    result: List[TargetOp] = []
    for stmt in stmts:
      result += self.handle_stmt(stmt, label_for_break)
    return result

  def handle_stmt(self, stmt: tree_nodes.Stmt,
      label_for_break: Optional[str]) -> List[TargetOp]:
    if isinstance(stmt, tree_nodes.AssigmentStmt):
      expr_result = self.handle_expression(stmt.value)
      result = list(expr_result.stmts)
      # todo: ..if not stmt.var_name in self.varname_to_type
      var_type = self.varname_to_type[stmt.var_name]
      if var_type == expr_result.result_type:
        result.append(get_assigment_target_stmt(to_target_var_name(stmt.var_name), expr_result.result_var,
                                                var_type))
        return result
      elif var_type == enums.VarType.FLOAT:
        result.append(get_covert_type_target_stmt(expr_result.result_var, stmt.var_name,
                                                  enums.VarType.FLOAT))
        return result
      else:
        print(var_type)
        print(expr_result.result_type)
        raise Exception("todo")#todo :error
    elif isinstance(stmt, tree_nodes.OutputStmt):
      expr_result = self.handle_expression(stmt.value)
      output_stmt = get_print_target_stmt(expr_result.result_var,
                                          expr_result.result_type)
      return expr_result.stmts + [output_stmt]
    elif isinstance(stmt, tree_nodes.InputStmt):
      #todo - not exists var
      return [get_read_target_stmt(to_target_var_name(stmt.var_name),
                                   self.varname_to_type[stmt.var_name])]
    elif isinstance(stmt, tree_nodes.IfStmt):
      bool_exp_result = self.handle_boolean_expression(stmt.condition)
      true_stmts = self.handle_stmts(stmt.true_stmts, label_for_break)
      false_stmts = self.handle_stmts(stmt.false_stms, label_for_break)
      else_label = self.label_generator.get_next()
      exit_label = self.label_generator.get_next()
      result : List[TargetOp] = []
      result.extend(bool_exp_result.stmts)
      result.append(get_jump_if_zero_stmt(bool_exp_result.result_var, else_label))
      result.extend(true_stmts)
      result.append(get_jump_stmt(exit_label))
      result.append(TargetLabel(else_label))
      result.extend(false_stmts)
      result.append(TargetLabel(exit_label))
      return result
    elif isinstance(stmt, tree_nodes.WhileStmt):
      start_label = self.label_generator.get_next()
      exit_label = self.label_generator.get_next()
      condition_result = self.handle_boolean_expression(stmt.condition)
      body_stmts = self.handle_stmts(stmt.body_stmts, exit_label)
      result : List[TargetOp] = []
      result.append(TargetLabel(start_label))
      result.extend(condition_result.stmts)
      result.append(get_jump_if_zero_stmt(condition_result.result_var, exit_label))
      result.extend(body_stmts)
      result.append(get_jump_stmt(start_label))
      result.append(TargetLabel(exit_label))
      return result
    elif isinstance(stmt, tree_nodes.SwitchStmt):
      exit_label = self.label_generator.get_next()
      default_label = self.label_generator.get_next()
      case_labels: List[str] = list(self.label_generator.get_next()
                                    for _ in stmt.cases)
      cond_var = self.var_generator.get_next()
      exp_result = self.handle_expression(stmt.exp)
      #if exp_result.result_var == enums.VarType.FLOAT
      result : List[TargetOp] = []
      result.extend(exp_result.stmts)
      for i, case in enumerate(stmt.cases):
        #todo:  if get_num_type(case.val) == enums.VarType.FLOAT
        result.append(get_set_1_if_not_equals_target_stmt(exp_result.result_var,
                                                          case.val, cond_var,
                                                          enums.VarType.INT))
        result.append(get_jump_if_zero_stmt(cond_var, case_labels[i]))
      for i, case in enumerate(stmt.cases):
        case_stmts = self.handle_stmts(case.stmts, exit_label)
        result.append(TargetLabel(case_labels[i]))
        result.extend(case_stmts)
      default_stmts = self.handle_stmts(stmt.default_stmts, exit_label)
      result.append(TargetLabel(default_label))
      result.extend(default_stmts)
      result.append(TargetLabel(exit_label))
      return result
    elif isinstance(stmt, tree_nodes.BreakStmt):
      #todo: if label_for_break is None
      return [get_jump_stmt(label_for_break)]
    else:
      raise Exception(f"Internal error: unrecognized stmt type : {type(stmt)}")

  def handle_boolean_expression(self, boolean_expression: tree_nodes.BooleanExpression
    )-> BooleanExpressionResult:
      if isinstance(boolean_expression, tree_nodes.SimpleBooleanExpression):
        expr1_result = self.handle_expression(boolean_expression.expression1)
        expr2_result = self.handle_expression(boolean_expression.expression2)
        result_stmt : List[TargetOp] = []
        if expr1_result.result_type == expr2_result.result_type:
          var1 = expr1_result.result_var
          var2 = expr2_result.result_var
          vars_type = expr1_result.result_type
        else:
          vars_type = enums.VarType.FLOAT
          if expr1_result.result_type == enums.VarType.FLOAT:
            var1 = expr1_result.result_var
            var2 = self.var_generator.get_next()
            result_stmt.append(get_covert_type_target_stmt(expr2_result.result_var, var2,
                                                      enums.VarType.FLOAT))
          else:
            var1 = self.var_generator.get_next()
            result_stmt.append(get_covert_type_target_stmt(expr1_result.result_var, var1,
                                                      enums.VarType.FLOAT))
            var2 = expr2_result.result_var
        result_var = self.var_generator.get_next()
        if boolean_expression.op == enums.ComparisionOperation.EQUAL:
          result_stmt.append(get_set_1_if_equals_target_stmt(var1, var2, result_var, vars_type))
        elif boolean_expression.op == enums.ComparisionOperation.NOT_EQUAL:
          result_stmt.append(get_set_1_if_not_equals_target_stmt(var1, var2, result_var, vars_type))
        elif boolean_expression.op == enums.ComparisionOperation.GREAT:
          result_stmt.append(get_set_1_if_great_target_stmt(var1, var2, result_var, vars_type))
        elif boolean_expression.op == enums.ComparisionOperation.LESS:
          result_stmt.append(get_set_1_if_less_target_stmt(var1, var2, result_var, vars_type))
        elif boolean_expression.op == enums.ComparisionOperation.LESS_EQUAL:
          result_stmt.append(get_set_1_if_great_target_stmt(var1, var2, result_var, vars_type))
          result_stmt.extend(self.get_stmt_for_opposite_boolen_var(result_var))
        elif boolean_expression.op == enums.ComparisionOperation.GREAT_EQUAL:
          result_stmt.append(get_set_1_if_less_target_stmt(var1, var2, result_var, vars_type))
          result_stmt.extend(self.get_stmt_for_opposite_boolen_var(result_var))
        else:
          raise Exception("internal errror, minus x points")
        return BooleanExpressionResult(result_var=result_var,stmts=result_stmt)
      elif isinstance(boolean_expression, tree_nodes.BinaryOperationBooleanExpretion):
        boolean_expression1_result = self.handle_boolean_expression(boolean_expression.boolean_expression1)
        boolean_expression2_result = self.handle_boolean_expression(boolean_expression.boolean_expression2)
        result_stmt: List[TargetOp] = []
        result_stmt.extend(boolean_expression1_result.stmts)
        result_stmt.extend(boolean_expression2_result.stmts)
        if boolean_expression.op == enums.BooleanBinaryOp.OR:
          exit_label = self.label_generator.get_next()
          result_stmt.append(get_jump_if_zero_stmt(boolean_expression2_result.result_var, exit_label))
          result_stmt.append(get_assigment_target_stmt(boolean_expression1_result.result_var, "1", enums.VarType.INT))
          result_stmt.append(TargetLabel(exit_label))
          return BooleanExpressionResult(result_var=boolean_expression1_result.result_var,
                                         stmts=result_stmt)
        elif boolean_expression.op == enums.BooleanBinaryOp.AND:
          exit_label = self.label_generator.get_next()
          mark_first_bool_exp_as_0_label = self.label_generator.get_next()
          result_stmt.append(get_jump_if_zero_stmt(boolean_expression2_result.result_var, mark_first_bool_exp_as_0_label))
          result_stmt.append(get_jump_stmt(exit_label))
          result_stmt.append(TargetLabel(mark_first_bool_exp_as_0_label))
          result_stmt.append(get_assigment_target_stmt(boolean_expression1_result.result_var, "0", enums.VarType.INT))
          result_stmt.append(TargetLabel(exit_label))
          return BooleanExpressionResult(result_var=boolean_expression1_result.result_var,
                                         stmts=result_stmt)
        else:
          raise Exception("internal error")
      elif isinstance(boolean_expression, tree_nodes.NotOperationBooleanExpretion):
        inner_result = self.handle_boolean_expression(boolean_expression.inner_boolean_expression)
        return BooleanExpressionResult(
            result_var=inner_result.result_var,
            stmts=inner_result.stmts + self.get_stmt_for_opposite_boolen_var(inner_result.result_var)
        )
      else:
        raise Exception("iternal error")


  def handle_expression(self, expression: tree_nodes.Expression
  )-> ExpressionResult:
    if isinstance(expression, tree_nodes.BinaryOperationExpression):
      expr1_result = self.handle_expression(expression.expression1)
      expr2_result = self.handle_expression(expression.expression2)
      result_stmt : List[TargetOp] = []
      if expr1_result.result_type == expr2_result.result_type:
        var1 = expr1_result.result_var
        var2 = expr2_result.result_var
        vars_type = expr1_result.result_type
      else:
        vars_type = enums.VarType.FLOAT
        if expr1_result.result_type == enums.VarType.FLOAT:
          var1 = expr1_result.result_var
          var2 = self.var_generator.get_next()
          result_stmt.append(get_covert_type_target_stmt(expr2_result.result_var, var2,
                                                         enums.VarType.FLOAT))
        else:
          var1 = self.var_generator.get_next()
          result_stmt.append(get_covert_type_target_stmt(expr1_result.result_var, var1,
                                                         enums.VarType.FLOAT))
          var2 = expr2_result.result_var
      result_var = self.var_generator.get_next()
      if expression.op == enums.BinaryOp.ADD:
        result_stmt.append(get_add_target_stmt(var1, var2, result_var, vars_type))
      elif expression.op == enums.BinaryOp.SUB:
        result_stmt.append(get_sub_target_stmt(var1, var2, result_var, vars_type))
      elif expression.op == enums.BinaryOp.MUL:
        result_stmt.append(get_mul_target_stmt(var1, var2, result_var, vars_type))
      elif expression.op == enums.BinaryOp.DIV:
        result_stmt.append(get_div_target_stmt(var1, var2, result_var, vars_type))
      else:
        raise Exception("intermnal error")
      return ExpressionResult(result_var=result_var, result_type=vars_type,
                              stmts=result_stmt)
    elif isinstance(expression, tree_nodes.VarExpression):
      #todo:if expression.var_name not in self.varname_to_type
      return ExpressionResult(result_var=to_target_var_name(expression.var_name),
                              result_type=self.varname_to_type[expression.var_name],
                              stmts=[])
    elif isinstance(expression, tree_nodes.NumExpression):
      return ExpressionResult(result_var=expression.num,
                              result_type=enums.VarType.FLOAT if "." in expression.num
                                           else enums.VarType.INT,
                              stmts=[])
    elif isinstance(expression,tree_nodes.CastExpression):
      inner_result = self.handle_expression(expression.expression)
      if inner_result.result_type == expression.target:
        return inner_result
      else:
        new_var = self.var_generator.get_next()
        stmts: List[TargetOp] = []
        stmts.extend(inner_result.stmts)
        stmts.append(get_covert_type_target_stmt(inner_result.result_var, new_var, expression.target))
        return ExpressionResult(result_var=new_var,
                                result_type=expression.target,
                                stmts=stmts)
    else:
      raise Exception("intenal error")




  def get_stmt_for_opposite_boolen_var(self, var_name: str) -> List[TargetOp]:
    exit_label = self.label_generator.get_next()
    make_var_1_label = self.label_generator.get_next()
    return [
        get_jump_if_zero_stmt(var_name, make_var_1_label),
        get_assigment_target_stmt(var_name, "0", enums.VarType.INT),
        get_jump_stmt(exit_label),
        TargetLabel(make_var_1_label),
        get_assigment_target_stmt(var_name, "1", enums.VarType.INT),
        TargetLabel(exit_label)
    ]

