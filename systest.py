import sys, os
def get_imports(file):
    imports = {}
    paths_to_search = sys.path
    paths_to_search.remove("/usr/lib/python35.zip")
    with open(file, "r") as f:
        for line in f:
            line = line.lstrip()
            if line.startswith("import "):
                mod = line.split("import ")[-1]
            elif line.startswith("from "):
                mod = line.split("from ")[-1].split("import")[0]
            else:
                continue
            print(mod, "mod")
            for path in sys.path:
                    for file in os.listdir(path):
                        if file.split(".")[0] == mod.rstrip().split(".")[0] and \
                                file.split(".")[-1] in ["py", "so"]:
                            imports[os.path.join(path, file)] = mod.rstrip()
                            print("yay")
                            break
                        else:
                            print(file, mod.rstrip())
    return imports

if __name__ == "__main__":
    print(get_imports("mainwindow_controller.py"))
