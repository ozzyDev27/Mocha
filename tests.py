import os
from main import runCommand
from contextlib import contextmanager
os.system("")

GREEN = "\033[1;32m"
RED = "\033[1;31m"
CLEAR = "\033[0m"

@contextmanager
def test(name):
    print(f"Running test: {name}")
    try:
        yield None
    except Exception as e:
        print(f"{RED}FAIL{CLEAR} {name} Error: {e}")
    finally:
        if success:
            print(f"{GREEN}PASS{CLEAR} {name} passed")
        else:
            print(f"{RED}FAIL{CLEAR} {name} failed")

with test(name="Functional"):
    runCommand("0")
    success = True
