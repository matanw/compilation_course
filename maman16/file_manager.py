
import sys
import os

SIGNATURE = "Student Name: Matan Wiesner"
INPUT_FILE_SUFFIX = ".ou"
OUTPUT_FILE_SUFFIX = ".qud"

def get_and_validate_input_file_path() -> str:
    if len(sys.argv) != 2:
        print('need exactly  one argument')
        exit(1)
    result = sys.argv[1]
    if not result.endswith(INPUT_FILE_SUFFIX):
        print(f" input file name need to ends with suffix {INPUT_FILE_SUFFIX}")
        exit(1)
    return result

def get_text(input_file_path: str) ->  str:
    with open(input_file_path, 'r') as file:
        return file.read()

def get_out_file_path(input_file_path) -> str:
    return input_file_path[0:-len(INPUT_FILE_SUFFIX)] + OUTPUT_FILE_SUFFIX

def write_output_file(out_file_path: str, final_code: str):
    with open(out_file_path, 'w') as file:
        file.write(final_code)