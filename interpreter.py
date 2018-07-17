import ast
import _ast
import importlib
import inspect
import sys, os
import error_catcher

file = "/home/kalyan/git/codeblock-visual-studio/blocks.py"

def get_imports_kai(file):
    # filetxt = open(file).readlines()

    importsfull = []

    for line in filetxt:
        if " import " in line or line.startswith("import "): importsfull.append(line)
    print(imports)

# this is what you meant to do, kai...
def get_imports(file):
    imports = {}
    paths_to_search = sys.path
    paths_to_search.reverse()
    for p in paths_to_search:
        if p.endswith(".egg") or p.endswith(".zip"):
            paths_to_search.remove(p)
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
            if mod.split(".")[0] != '':
                # Import is absolute
                for path in paths_to_search:
                        for file in os.listdir(path):
                            if file.split(".")[0] == mod.rstrip().split(".")[0]:
                                if file.split(".")[-1] in ["py", "so"]:
                                    # If detected as module available in sys.path, append to imports
                                    imports[mod.rstrip()] = os.path.join(path, file)
                                    print("yay")
                                    break
                                elif os.path.isdir(os.path.join(path, file)):
                                    # Detected as package, recurse through directories
                                    # TODO: Optimize this code
                                    # (could try adapting relative import code)
                                    if len(mod.split(".")) > 1:
                                        print(mod, "package")
                                        path = os.path.join(path, file)
                                        for j in mod.split(".")[1:]:
                                            for file2 in os.listdir(path):
                                                if os.path.isdir(os.path.join(path, file2)) and \
                                                        file2 == j:
                                                            path = os.path.join(path, file2)
                                                elif file2.split(".")[0] == mod.split(".")[-1].rstrip():
                                                    imports[mod.rstrip()] = os.path.join(path, file2)
                                                    break
                                    else:
                                        print(mod.split("."), "modsplit")
                                        imports[mod.rstrip()] = os.path.join(path, file)+"/__init__.py"
                                        break
                            elif mod.rstrip() in sys.builtin_module_names:
                                imports[mod.rstrip()] = mod.rstrip() + " - builtin"
                            else:
                                pass
            else:
                # Import is relative
                print("relative")
                for part in mod.split(".")[1:]:
                    try:
                        os.chdir(part)
                    except NotADirectoryError:
                        for file in os.listdir():
                            if file.split(".")[0] == mod.split(".")[-1].rstrip() and \
                                    file.split(".")[1] in [".py", ".so"]:
                                        imports[mod.rstrip()] = os.path.join(path, file)

    return imports


def get_variables_kai(node, file):
    variables = set()
    if hasattr(node, 'body'):
        for subnode in node.body:
            variables |= get_variables(subnode)
    elif isinstance(node, _ast.Assign):
        for name in node.targets:
            if isinstance(name, _ast.Name):
                variables.add(name.id)
    return variables

def get_classes_kai(file):
    filetxt = open(file).readlines()

    classes = {}
    linenumofclass = []
    classnames = []
    fullclasslines = []
    classlines = []
    current_line = 0

    for line in filetxt:
        current_line = current_line + 1
        if "class " in line:
            linenumofclass.append(current_line)
            classnames.append(line)
            print(classnames, "classnames")

    for loc in linenumofclass:
        print(loc, "classlines")
        clsname = [filetxt[loc-1]]
        print(clsname, "whichclass")
        top_leading_whitespace = len(filetxt[loc]) - len(filetxt[loc].lstrip())
        print(top_leading_whitespace, "topclasswhitespace")
        for body in filetxt[loc:]:
            leading_whitespace = len(body) - len(body.lstrip())
            print(leading_whitespace)
            if leading_whitespace < top_leading_whitespace:
                print(body)
                if body != "\n" and len(body) - len(body.lstrip()) != top_leading_whitespace:
                    break
            classlines.append(body)
        fullclasslines.append(classlines)
        print(fullclasslines)
        classlines = []
    classes = dict(zip(classnames, fullclasslines))
    print("\n\n\n", classes, "totlayfinalclass")
    return classes

# this is what you meant to do, kai...
def get_classes(file):
    classes = dict()
    funcnames = list()
    funcs = dict()
    cache = []
    saved_indent_class = -1
    saved_indent_func = -1
    class_name = ""

    with open(file, "r") as f:
        for line in f:
            indent_level = len(line) - len(line.lstrip())
            if line.lstrip().startswith("class "):
                if saved_indent_class != -1 and indent_level <= saved_indent_class:
                    classes[class_name] = funcs
                    funcs = {}
                saved_indent_class = -1
                class_name = line.split("class ")[-1].split("(")[0]
                saved_indent_class = indent_level
                continue

            if line.lstrip().startswith("def "):
                func_name = line.split("def ")[-1].split("(")[0]
                saved_indent_func = indent_level
                continue

            if saved_indent_func != -1 and indent_level > saved_indent_func:
                cache.append(line)
            elif saved_indent_func != -1 and indent_level <= saved_indent_func:
                saved_indent_func = -1
                funcs[func_name] = cache
                cache = []
            if saved_indent_class != -1 and indent_level <= saved_indent_class:
                classes[class_name] = funcs
                funcs = {}
                saved_indent_class = -1

    """
    for k, v in classes.items():
        print(k)
        for a, b in v.items():
             print(a)
             print("".join(b))
    """
    return classes

def get_functions_kai(file):
    filetxt = open(file).readlines() # path may need to be changed

    current_line = 0
    finalfuncnames = []
    funcs = {}
    funcnumlines = []
    funclines = []
    fullfunclines = []
    leading_whitespace = 0
    whitespaceforchecking = 0
    for line in filetxt:
        current_line = current_line + 1
        if "def " in line:
            funcnumlines.append(current_line)
            print(funcnumlines, "linenumoffuncs")
            finalfuncnames.append(line)
            print(finalfuncnames, "funcnamesfinallist")

    for lof in funcnumlines:
        print(lof, "forlines")
        funcname = filetxt[lof-1]
        top_leading_whitespace = len(filetxt[lof]) - len(filetxt[lof].lstrip())
        print(top_leading_whitespace, "initalwhitespace")
        funcbody = filetxt[lof]
        for body in filetxt[lof:]:
            leading_whitespace = len(body) - len(body.lstrip())
            print(whitespaceforchecking, "whitespacebody")
            if leading_whitespace < top_leading_whitespace:
                if body != "\n" and len(body) - len(body.lstrip()) != top_leading_whitespace:
                    break
            funclines.append(body)
        print(funclines, "finalfunclines")
        fullfunclines.append(funclines)
        print(fullfunclines, "fullfunclines")
        funclines = []

    funcs = dict(zip(finalfuncnames, fullfunclines))

    print(funcs, "totalyfinal")
    return funcs

# this is what you meant to do, kai...
def get_functions(file):
    finalfuncnames = []
    funcs = {}
    funcnumlines = []
    funclines = []
    fullfunclines = []
    leading_whitespace = 0
    whitespaceforchecking = 0
    cache = ""
    with open(file, "r") as f:
        for line in f:
            if line.lstrip().startswith("def "):
                func_name = line.split("def ")[-1].split("(")[0]
            current_line = current_line + 1
            if "def " in line:
                funcnumlines.append(current_line)
                print(funcnumlines, "linenumoffuncs")
                finalfuncnames.append(line)
                print(finalfuncnames, "funcnamesfinallist")

    for lof in funcnumlines:
        print(lof, "forlines")
        funcname = filetxt[lof-1]
        top_leading_whitespace = len(filetxt[lof]) - len(filetxt[lof].lstrip())
        print(top_leading_whitespace, "initalwhitespace")
        funcbody = filetxt[lof]
        for body in filetxt[lof:]:
            leading_whitespace = len(body) - len(body.lstrip())
            print(whitespaceforchecking, "whitespacebody")
            if leading_whitespace < top_leading_whitespace:
                if body != "\n" and len(body) - len(body.lstrip()) != top_leading_whitespace:
                    break
            funclines.append(body)
        print(funclines, "finalfunclines")
        fullfunclines.append(funclines)
        print(fullfunclines, "fullfunclines")
        funclines = []

    funcs = dict(zip(finalfuncnames, fullfunclines))

    print(funcs, "totalyfinal")
    return funcs

def get_classes_all(file):
    imports = get_imports(file)
    ret_classes = {}
    ret_lint = {}
    for i,v in imports.items():
        if v.endswith(".so") or v.endswith("builtin"):
            uninspectable_classes = {}
            print(i, "uninspecting")
            foo = importlib.import_module(i)
            for name, obj in inspect.getmembers(foo):
                if inspect.isclass(obj):
                    try:
                        uninspectable_classes[name] = None
                    except:
                        print(i, "uninspectable")
            ret_classes[v] = uninspectable_classes
            continue
        ret_classes[v] = get_classes(v)
        ret_lint[v] = error_catcher.get_lint(v)
    ret_classes[file] = get_classes(file)
    ret_lint[file] = error_catcher.get_lint(file)
    return ret_classes, ret_lint, imports

# get_imports(file)
if __name__ == "__main__":
    print(get_classes_all("mainwindow_controller.py")[])
