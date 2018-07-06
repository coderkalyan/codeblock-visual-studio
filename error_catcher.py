import sys, os
import pylint.lint
import importlib

def get_lint(file):
    lint = os.popen("python3 -m flake8 " + file).read()

    errors_to_return = {}
    warnings_to_return = {}
    for i in lint.split("\n"):
        try:
            print(i)
            if any(error in i for error in ["F4", "F8", "F901", "E999"]):
                if "F403" in i:
                    scan_import(i)

                errors_to_return[i] = int(i.split(":")[1])
            else:
                warnings_to_return[i] = int(i.split(":")[1])
        except IndexError:
            pass
    return errors_to_return


def scan_import(line):
    print(line, "KABOOOOOM")
    print(line.split("'")[1])
    line = line.split("'")[1]
    try:
        if line.startswith("from"):
            importlib.import_module(
                    line.split("import")[-1],
                    line.split()[1]) # import package
        else:
            importlib.import_module(
                    line.split("import")[-1]) # import module
        return True
    except ImportError:
        return False


if __name__ == "__main__":
    print(get_lint("tkintertest.py"))
