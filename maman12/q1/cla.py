import sly 

import sys
import os

SIGNATURE = "Student Name: Matan Wiesner"


def print_to_stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class LexerHelper(sly.Lexer):
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

class  ProcessedToken:
    def __init__(self, token_type, lexeme, attributes):
        self.token_type =  token_type
        self.lexeme = lexeme
        self.attributes =  attributes

class Lexer():
    """ This class is the classs that implement the interface that required in question"""

    def __init__(self, text, error_logger):
        self.tokens_generator = LexerHelper().tokenize(text)
        self.error_logger = error_logger


    def _get_next_sly_token(self):
        try:
            return next(self.tokens_generator)
        except StopIteration:
            return None

    def get_next_token(self):
        """This funcction return next valid token, or None in case of  end of output"""
        in_comment = False
        line_comment_start =None
        while True:
            sly_token = self._get_next_sly_token()
            if in_comment:
                if sly_token is None:
                    self.error_logger.log_error(f"Opened comment in line {line_comment_start} and didn't close")
                    return None
                elif sly_token.type == 'COMMMENT_END':
                    in_comment = False
            else:
                if sly_token is None:
                    return None
                elif sly_token.type == 'ERROR':
                    self.error_logger.log_error(f"Bad character in line {sly_token.lineno}: '{sly_token.value}'")
                elif sly_token.type == 'COMMMENT_START':
                    in_comment = True
                    line_comment_start = sly_token.lineno
                elif sly_token.type == 'COMMMENT_END':
                    self.error_logger.log_error(f"Error in line {sly_token.lineno}: close comment without open it")
                else:
                    return ProcessedToken(sly_token.type, sly_token.value, get_attributes(sly_token)) 


class ErrorLogger():
    def log_error(self, message):
        print_to_stderr(message)

def get_input_file_path():
    if len(sys.argv) != 2:
        raise Exception('need exactly  one argument')
    return sys.argv[1] 

def get_text(input_file_path):
    with open(input_file_path, 'r') as file:
        return file.read()

def get_out_file_path(input_file_path):
    return os.path.splitext(input_file_path)[0] + '.tok'

def write_output_file(out_file_path, lexer):
    with open(out_file_path, 'w') as file:
        file.write("TOKEN\tLEXEME\tATTRIBUTE\n")
        token = lexer.get_next_token()
        while token:
            attributes_str = ','.join([f"{k}={v}" for k, v  in token.attributes.items()])
            file.write(f"{token.token_type}\t{token.lexeme}\t{attributes_str}\n")
            token = lexer.get_next_token()
        file.write(SIGNATURE)



def main():
    input_file_path = get_input_file_path()
    text = get_text(input_file_path)
    lexer = Lexer(text, ErrorLogger())
    out_file_path = get_out_file_path(input_file_path)
    write_output_file(out_file_path, lexer)
    print_to_stderr(SIGNATURE)


if __name__ == '__main__':
    main()

