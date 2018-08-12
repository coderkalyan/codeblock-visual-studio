import sys, os
import importlib
import flake8.api.legacy
from io import StringIO

def get_lint(file):
    # Temporarily redirect stdout to the lintstdout variable to get flake8 output
    oldstdout = sys.stdout
    sys.stdout = lintstdout = StringIO()

    # Get output using Flake8's "legacy" API
    guide = flake8.api.legacy.get_style_guide()
    guide.check_files(["mainwindow_controller.py"])

    # Reset stdout
    sys.stdout = oldstdout

    # set lint variable to captured output
    lint = lintstdout.getvalue()

    errors_to_return = {}
    warnings_to_return = {}
    verified_packages = []
    sys.path.append("/".join(file.split("/")[:-1]))
    for i in lint.split("\n"):
        try:
            print(i)
            if any(error in i for error in ["F402",
                                            "F403",
                                            "F404",
                                            "F405",
                                            "F406",
                                            "F407",
                                            "F8",
                                            "F901",
                                            "E999"]):
                if "F403" in i:
                    print((i))
                    if not scan_import(i):
                        i = ":".join(i.split(":")[:3]) + ": F403 Package not installed or is unavailable."
                    else:
                        verified_packages.append(i.split("'")[1].split()[1])
                        continue
                        print("skipped")
                elif "F405" in i:
                    if any(pkg in verified_packages for pkg in i.split(":")[-1][1:].split(", ")):
                        continue
                        print("skipped")
                    else:
                        i = ":".join(i.split(":")[:3]) + ": F405 '" + i.split("'")[1] + "'" + "is undefined."
                i = "E: " + i
                errors_to_return[i] = int(i.split(":")[2])
            else:
                i = "W: " + i
                warnings_to_return[i] = int(i.split(":")[2])
        except IndexError:
            pass
    return errors_to_return, warnings_to_return, dict()


def scan_import(line):
    print(line, "KABOOOOOM")
    print(line.split("'")[1])
    line = line.split("'")[1]
    try:
        if line.startswith("from"):
            importlib.import_module(
                    line.split()[1]) # import package
        else:
            importlib.import_module(
                    line.split("import")[-1]) # import module
        return True
    except ImportError:
        return False


if __name__ == "__main__":
    print(get_lint("mainwindow_controller.py"))
