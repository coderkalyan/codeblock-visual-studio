import sys, os
import pylint.lint

def get_errors(file):
    lint = os.popen("python3 -m flake8 " + file).read()

    errors_to_return = {}
    for i in lint.split("\n"):
        try:
            print(i)
            errors_to_return[i] = i.split(":")[1]
        except IndexError:
            pass
    return errors_to_return

def scan_imports(lines):
    pass

if __name__ == "__main__":
    print(get_errors("tkintertest.py"))
