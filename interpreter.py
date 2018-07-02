from modulefinder import ModuleFinder
import ast
import _ast

finder = ModuleFinder()
path = "/home/kai/git/codeblock-visual-studio/tkintertest.py"
file = open(path).readlines()
testvar = "poop to you!"

def get_imports():
    finder.run_script(path)
    for name, mod in finder.modules.items():
        pass

def get_variables(node):
    variables = set()
    if hasattr(node, 'body'):
        for subnode in node.body:
            variables |= get_variables(subnode)
    elif isinstance(node, _ast.Assign):
        for name in node.targets:
            if isinstance(name, _ast.Name):
                variables.add(name.id)
    return variables

def get_functions():
    funcs = []
    for line in file:
        if line.startswith("def "):
            funcs.append(line)
            print(funcs)
