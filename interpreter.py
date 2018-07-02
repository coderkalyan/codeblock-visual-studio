from modulefinder import ModuleFinder
import ast
import _ast

finder = ModuleFinder()
path = "/home/kai/git/codeblock-visual-studio/tkintertest.py"
file = open(path).readlines()
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

def get_functions(file):
    funcs = {}
    removeend = []
    for line in file:
        if line.startswith("def "):
            func_full = line.split("def ")[1]
            print(func_full)
            for char in func_full:
                if char == "(":
                    removeend.append(char)
    print(removeend[0])



get_functions(file)
