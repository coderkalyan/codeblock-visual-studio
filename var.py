import ast
import _ast

def get_variables(node):
    variables = set()
    if hasattr(node, 'body'):
        for subnode in node.body:
            variables = variables.union(get_variables(subnode))
    elif isinstance(node, _ast.Assign):
        for name in node.targets:
            if isinstance(name, _ast.Name):
                variables.add(name.id)
    return variables

print(get_variables(ast.parse(open('tkintertest.py').read())))
