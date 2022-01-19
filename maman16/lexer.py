import sly 


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
    RELOP = r'==|!=|<=|>=|>|<'
    ADDOP=r'\+|-'
    MULOP=r'\*|/'
    OR=r'\|\|'
    AND= r'&&'
    NOT =r'!'
    CAST=r'static_cast\<int\>|static_cast\<float\>'

    NUM = r'\d+(\.\d*)?'
    ID = r'[A-Za-z]([A-Za-z0-9])*'

    ID['break'] = BREAK
    ID['case'] = CASE
    ID['default'] = DEFAULT
    ID['else'] = ELSE
    ID['float'] = FLOAT
    ID['if'] = IF
    ID['input'] = INPUT
    ID['int'] = INT
    ID['output'] = OUTPUT
    ID['switch'] = SWITCH
    ID['while'] = WHILE

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        t.value = t.value[0]
        self.index += 1
        return t


def get_attributes(sly_token):
    if sly_token.type == 'CAST':
        target = 'int' if sly_token.value == 'static_cast<int>' else 'float'
        return {'target': target}
    if sly_token.type == 'ID':
        return {'id': sly_token.value}
    if sly_token.type == 'NUM':
        if '.' in sly_token.value:
            return {'value': float(sly_token.value), 'type': 'float'}
        else:
            return {'value': int(sly_token.value), 'type': 'int'}
    if sly_token.type in ['RELOP','ADDOP','MULOP']:
        return { 'op': sly_token.value}
    return {}

def get_filtered_tokrens(text, error_logger):
  in_comment = False
  line_comment_start =None
  for sly_token in Lexer().tokenize(text):
      if in_comment:
          if sly_token.type == 'COMMMENT_END':
              in_comment = False
          continue
      if sly_token.type == 'ERROR':
          error_logger.log_error(f"Bad character in line {sly_token.lineno}: '{sly_token.value}'")
      elif sly_token.type == 'COMMMENT_START':
          in_comment = True
          line_comment_start = sly_token.lineno
      elif sly_token.type == 'COMMMENT_END':
          error_logger.log_error(f"Error in line {sly_token.lineno}: close comment without open it")
      else:
          yield sly_token
  if in_comment:
      error_logger.log_error(f"Opened comment in line {line_comment_start} and didn't close")


def main():
    import errror_logger
    logger  = errror_logger.ErrorLogger()
    for token in get_filtered_tokrens("3 if 5-7/*ccc*/ 45",logger):
        print(token)
if __name__ == '__main__':
    main()

