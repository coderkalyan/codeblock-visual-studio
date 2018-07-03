import pylint.lint
import sys
from io import StringIO

stdout = sys.stdout
sys.stdout = StringIO()

def get_errors(file):
    lint = pylint.lint.Run(['-r', 'n', file], exit=False)

    errors = sys.stdout.getvalue()
    errors_to_return =  {}
    sys.stdout.close()
    sys.stdout = stdout

    print(errors.split('\n'))
    for i in errors.split('\n')[1:]:
        try:
            errors_to_return[i.split(",")[0][-1]] = i
        except IndexError:
            pass
    print(errors_to_return)


if __name__ == "__main__":
    get_errors("err1.py")
