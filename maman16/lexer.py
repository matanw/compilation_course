import sly 
import enums
import program_errors


class Lexer(sly.Lexer):
    """This is an extention to sly.Lexer to parse  the CPL  langunage
    This class *do not*  implement the interfacce in question"""
    tokens = { COMMMENT_START, COMMMENT_END,NUM, ID,
               BREAK, CASE, DEFAULT, ELSE, FLOAT,
               IF, INPUT, INT, OUTPUT, SWITCH, WHILE,
               RELOP,ADDOP,MULOP,OR,AND,NOT, CAST}


    literals = { '(', ')', '{','}', ',', ':', ';', '='}

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    COMMMENT_START = r'/\*'
    COMMMENT_END = r'\*/'



    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        t.value = t.value[0]
        self.index += 1
        return t

    @_(r'static_cast\<int\>|static_cast\<float\>')
    def CAST(self, t):
        t.value = enums.VarType.INT  if t.value == 'static_cast<int>' else enums.VarType.FLOAT
        return t

    @_(r'&&')
    def AND(self, t):
        t.value = enums.BooleanBinaryOp.AND
        return t

    @_(r'\|\|')
    def OR(self, t):
        t.value = enums.BooleanBinaryOp.OR
        return t

    @_(r'\+|-')
    def ADDOP(self, t):
        t.value = enums.BinaryOp.ADD if t.value == '+' else enums.BinaryOp.SUB
        return t

    @_(r'\*|/')
    def MULOP(self, t):
        t.value = enums.BinaryOp.MUL if t.value == '*' else enums.BinaryOp.DIV
        return t

    @_(r'==|!=|<=|>=|>|<')
    def RELOP(self, t):
        chars_to_op = {
            '==' : enums.ComparisionOperation.EQUAL,
            '!=' : enums.ComparisionOperation.NOT_EQUAL,
            '<=' : enums.ComparisionOperation.LESS_EQUAL,
            '>=' : enums.ComparisionOperation.GREAT_EQUAL,
            '<' : enums.ComparisionOperation.LESS,
            '>' : enums.ComparisionOperation.GREAT,
        }
        t.value = chars_to_op[t.value]
        return t

    @_(r'int')
    def INT(self, t):
        t.value = enums.VarType.INT
        return t

    @_(r'float')
    def FLOAT(self, t):
        t.value = enums.VarType.FLOAT
        return t

    NUM = r'\d+(\.\d*)?'
    ID = r'[A-Za-z]([A-Za-z0-9])*'
    NOT =r'!'
    ID['break'] = BREAK
    ID['case'] = CASE
    ID['default'] = DEFAULT
    ID['else'] = ELSE
    ID['if'] = IF
    ID['input'] = INPUT
    ID['output'] = OUTPUT
    ID['switch'] = SWITCH
    ID['while'] = WHILE


def get_token_set():
    result = Lexer.tokens.copy()
    result.remove('COMMMENT_START')
    result.remove('COMMMENT_END')
    return result

def get_filtered_tokrens(text, errors_manager: program_errors.ErrorsManager):
  in_comment = False
  line_comment_start =None
  for sly_token in Lexer().tokenize(text):
      if in_comment:
          if sly_token.type == 'COMMMENT_END':
              in_comment = False
          continue
      if sly_token.type == 'ERROR':
          errors_manager.add_lexer_error(sly_token.lineno, f"Bad character: '{sly_token.value}'")
      elif sly_token.type == 'COMMMENT_START':
          in_comment = True
          line_comment_start = sly_token.lineno
      elif sly_token.type == 'COMMMENT_END':
          error_logger.log_error(f"Error in line {sly_token.lineno}: close comment without open it")
      else:
          yield sly_token
  if in_comment:
      error_logger.log_error(f"Opened comment in line {line_comment_start} and didn't close")


def main():#todo delete
    import program_errors
    logger  = errror_logger.ErrorLogger()
    for token in get_filtered_tokrens("3 if; 5-7/*ccc*/ 45",logger):
        print(token)
if __name__ == '__main__':
    main()

