from sly import Lexer

import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class SlyLexerExtention(Lexer):
    # Set of token names.   This is always required
    tokens = { NUMBER, ID, BREAK, CASE, DEFAULT, ELSE, FLOAT,
               IF, INPUT, INT, OUTPUT, SWITCH, WHILE
               PLUS, MINUS, TIMES, DIVIDE, ASSIGN,
               EQ, LT, LE, GT, GE, NE ,AND, OR}


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
    AND      = r'!='
    OR      = r'\|\|'

    NUMBER = r'\d+(\.\d*)?'

    # Identifiers and keywords
    ID = r'[a-Za-z]([a-Za-z0-9])*'
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


def get_text():
    if len(sys.argv) != 2:
        raise Exception('need exactly  one argument')
    file_path = sys.argv[1] #todo: handle error
    with open(file_path, 'r') as file:
        return file.read()

def main():
    lexer = SlyLexerExtention()
    a=lexer.tokenize(get_text())
    for x in a:
        print(x)

if __name__ == '__main__':
    main()
