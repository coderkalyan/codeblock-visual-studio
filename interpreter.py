import ast
import _ast
import importlib

file = "/home/kalyan/git/codeblock-visual-studio/blocks.py"

def get_imports_kai(file):
    # filetxt = open(file).readlines()

    importsfull = []

    for line in filetxt:
        if " import " in line or line.startswith("import "):
            importsfull.append(line)
    print(imports)

# this is what you meant to do, kai...
def get_imports(file):
    imports = []
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
            try:
                imports.append(importlib.import_module(mod.rstrip()).__file__)
            except ImportError as e:
                print(e)
                continue
            except AttributeError as e:
                print(e)
                print("assuming builtin, continuing")
                continue
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
    return classes, funcs

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

# get_imports(file)
if __name__ == "__main__":
    get_classes("mainwindow_controller.py")
    print(get_imports("mainwindow_controller.py"))
