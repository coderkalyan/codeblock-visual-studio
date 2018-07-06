from modulefinder import ModuleFinder
import ast
import _ast

finder = ModuleFinder()
file = "/home/kai/git/codeblock-visual-studio/mainwindow_controller.py"
testvar = "poop to you!"

def get_imports(file):
    finder.run_script(path)
    for name, mod in finder.modules.items():
        pass

def get_variables(node, file):
    variables = set()
    if hasattr(node, 'body'):
        for subnode in node.body:
            variables |= get_variables(subnode)
    elif isinstance(node, _ast.Assign):
        for name in node.targets:
            if isinstance(name, _ast.Name):
                variables.add(name.id)
    return variables

def get_classes(file):
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







def get_functions(file):
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

get_classes(file)
