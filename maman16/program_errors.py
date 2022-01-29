import sys
from typing import List, Tuple

def print_to_stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class ErrorsManager():
    def __init__(self):
        self._lexer_errors: List[Tuple[int, str]] = []
        self._parser_errors: List[Tuple[int, str]] = []
        self._semantic_errors: List[Tuple[int, str]] = []

    def add_lexer_error(self, lineno:int, message: str):
        self._lexer_errors.append((lineno, message))

    def add_parser_error(self, lineno:int, message: str):
        self._parser_errors.append((lineno, message))

    def add_semantic_error(self, lineno:int, message: str):
        self._semantic_errors.append((lineno, message))

    def has_errors(self) -> bool:
        return bool(self._lexer_errors or self._parser_errors or self._semantic_errors)

    def log_errors(self):
        for type, list in [("Lexer", self._lexer_errors),
                           ("Parser", self._parser_errors),
                           ("Semantic", self._semantic_errors)]:
            if list:
                print_to_stderr(f"{type} Errors:")
                for lineno, message in list:
                    print_to_stderr(f"Line {lineno}: {message}")
