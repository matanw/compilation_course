
from sly import Lexer
import sys


class CalcLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { ORDER_NUMBER,SPACE,T,TIME_VAL,A,A_VAL,C, D, DV}
    # String containing ignored characters between tokens
    ignore = '\n'
    # Regular expression rules for tokens
    ORDER_NUMBER = r'\[\d\]'
    SPACE = r' '
    T=      r'\<time\>'
    TIME_VAL= r'\d\.\d\d'
    A=r'\<athlete\>'
    A_VAL=r'\"[a-zA-Z ]*\"'
    C= r'\<country\>'
    D = r'\<date\>'
    DV= r'\d\d? (January|February|March|April|May|June|July|August|September|October|November|December) \d\d\d\d'
if __name__ == '__main__':
    file_path = sys.argv[1] #todo: handle error
    with open(file_path, 'r') as file:
        data = file.read()
    lexer = CalcLexer()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))

