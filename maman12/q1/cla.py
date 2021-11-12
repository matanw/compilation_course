import sly 

import sys
import os

SIGNATURE = "Student Name: Matan Wiesner"


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class LexerHelper(sly.Lexer):
    """This is an extention to sly.Lexer to parse  the CPL  langunage
    This class *do not*  implement the interfacce in question"""
    # Set of token names.   This is always required
    tokens = { NUMBER, ID, BREAK, CASE, DEFAULT, ELSE, FLOAT,
               IF, INPUT, INT, OUTPUT, SWITCH, WHILE,
               PLUS, MINUS, TIMES, DIVIDE, ASSIGN,
               EQ, LT, LE, GT, GE, NE ,AND, OR,NOT, CAST}


    literals = { '(', ')', '{','}', ',', ':', ';'}

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    EQ      = r'=='
    ASSIGN  = r'='
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    NE      = r'!='
    AND      = r'&&'
    OR      = r'\|\|'
    NOT =   r'!'

    NUMBER = r'\d+(\.\d*)?'
    CAST = r'(static_cast\<int\>|static_cast\<float\>)'

    # Identifiers and keywords
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

    ignore_comment = r'\#.*'

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        eprint('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1


def get_attributes(sly_token):
    return {}

class  ProcessedToken:
    def __init__(self, token_type, lexeme, attributes):
        self.token_type =  token_type
        self.lexeme = lexeme
        self.attributes =  attributes

class Lexer():
    """ This class is the classs that implement the interface that required in question"""

    def __init__(self, text):
        self.tokens_generator = LexerHelper().tokenize(text)

    def get_next_token(self):
        """This funcction return next valid token, or None in case of  end of output"""
        try:
            sly_token=next(self.tokens_generator)
        except StopIteration:
            return None
        return ProcessedToken(sly_token.type, sly_token.value, get_attributes(sly_token)) 



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
    lexer = Lexer(text)
    out_file_path = get_out_file_path(input_file_path)
    write_output_file(out_file_path, lexer)
    eprint(SIGNATURE)


if __name__ == '__main__':
    main()
