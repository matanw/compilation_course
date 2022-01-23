import sys
def print_to_stderr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class ErrorLogger():
    def log_error(self, message):
        print_to_stderr(message)