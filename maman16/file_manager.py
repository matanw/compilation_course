
import sys
import os

SIGNATURE = "Student Name: Matan Wiesner"

def get_input_file_path() -> str:
    if len(sys.argv) != 2:
        raise Exception('need exactly  one argument')
    return sys.argv[1] 

def get_text() ->  str:
    with open(get_input_file_path(), 'r') as file:
        return file.read()

def get_out_file_path() -> str:
    return os.path.splitext(get_input_file_path())[0] + '.qud'

def write_output_file(final_code: str):
    with open(get_out_file_path(), 'w') as file:
        file.write(final_code)