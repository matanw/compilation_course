
from sly import Lexer
import sys
import re

class AtleteLexer(Lexer):
    tokens = {TITLE, SERIAL_NUMBER,SPACE,TIME_FIELD_NAME,TIME_VALUE,
              ATHLETE_FIELD_NAME,STRING_LITERAL,COUNTRY_FIELD_NAME, 
              DATE_FIELD_NAME, DATE_VALUE}
              
    TITLE = r'World Record'
    SERIAL_NUMBER = r'\[\d\]'
    SPACE = r' '
    TIME_FIELD_NAME=      r'\<time\>'
    TIME_VALUE= r'\d\.\d\d'
    ATHLETE_FIELD_NAME=r'\<athlete\>'
    STRING_LITERAL=r'\"[a-zA-Z ]*\"'
    COUNTRY_FIELD_NAME= r'\<country\>'
    DATE_FIELD_NAME = r'\<date\>'
    DATE_VALUE= r'\d\d? (January|February|March|April|May|June|July|August|September|October|November|December) \d\d\d\d'

    def error(self, t):
        self.index += 1
        return t

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

class  ProcessedToken:
    def __init__(self, token_type, lexeme, attributes):
        self.token_type =  token_type
        self.lexeme = lexeme
        self.attributes =  attributes

def get_text():
    if len(sys.argv) != 2:
        raise Exception('need exactly  one argument')
    file_path = sys.argv[1] #todo: handle error
    with open(file_path, 'r') as file:
        return file.read()

def get_sly_tokens(text):
    return list(AtleteLexer().tokenize(text))

def filter_out_non_tokens(sly_tokens):
    return [t for t in sly_tokens if t.type  not in ['SPACE','ERROR']]

def  print_errors(sly_tokens):
    for token in sly_tokens:
        if token.type == 'ERROR':
            print(f"Error  in line  {token.lineno}:  Illegal  character {token.value[0]}")

def get_attributes(sly_token):
    if sly_token.type == 'SERIAL_NUMBER':
      match = re.match(r'\[(\d)\]',sly_token.value)
      number =  int(match.group(1))
      return {"number" :  number}

    if sly_token.type == 'STRING_LITERAL':
      match = re.match(r'\"([a-zA-Z ]*)\"', sly_token.value)
      content =  match.group(1)
      return {"content" :  content}    

    if sly_token.type == 'TIME_VALUE':
      return {"value" :  float(sly_token.value)}

    if sly_token.type == 'DATE_VALUE':
        match = re.match(
            r'(\d\d?) (January|February|March|April|May|June|July|August|September|October|November|December) (\d\d\d\d)',
             sly_token.value)
        day  = int(match.group(1))
        month  = match.group(2)
        year  = int(match.group(3))
        
        return {"day": day, "month":  month, "year":  year}


    return  {}


def get_processed_tokens(sly_tokens):
    return [ProcessedToken(t.type, t.value, get_attributes(t))  for t in  sly_tokens]

def print_processed_tokens(processed_tokens):
    print("TOKEN\tLEXEME\tATTRIBUTE")
    for processed_token in processed_tokens:
        attributes_str = ','.join([f"{k}={v}" for k, v  in processed_token.attributes.items()])
        print(f"{processed_token.token_type}\t{processed_token.lexeme}\t{attributes_str}")

def main():
    text = get_text()
    sly_tokens = get_sly_tokens(text)
    print_errors(sly_tokens)
    sly_tokens = filter_out_non_tokens(sly_tokens)
    processed_tokens = get_processed_tokens(sly_tokens)
    print_processed_tokens(processed_tokens)

if __name__ == '__main__':
    main()
