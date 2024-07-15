import sys
from contextlib import contextmanager


# redirect the stdout to a buffer
@contextmanager
def redirected_stdout(new_output):
    old_output = sys.stdout
    sys.stdout = new_output
    try:
        yield
    finally:
        sys.stdout = old_output
