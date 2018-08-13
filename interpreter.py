import ast
import _ast
import importlib
import inspect
import sys, os

def get_imports_kai(file):
    # filetxt = open(file).readlines()

    importsfull = []

    for line in filetxt:
        if " import " in line or line.startswith("import "): importsfull.append(line)

# this is what you meant to do, kai...
# Reference Implementation of get_imports
def get_imports(file):
    # Initialize variables for storage
    imports = {}
    curpath = file
    # Add file itself to list of imports
    imports[file.split("/")[-1].split(".")[0]] = file
    paths_to_search = sys.path
    # Reverse sys.path - search backwards (this way path hierarchy is saved)
    paths_to_search.reverse()

    # Remove unsearchable paths (eggs and zip archives)
    for p in paths_to_search:
        if p.endswith(".egg") or p.endswith(".zip"):
            paths_to_search.remove(p)
    with open(file, "r") as f:
        for line in f:
            # Scan for imports, if none found, continue to next line
            line = line.lstrip()
            if line.startswith("import "):
                mod = line.split("import ")[-1]
            elif line.startswith("from "):
                mod = line.split("from ")[-1].split("import")[0]
            else:
                continue
            if mod.split(".")[0] != '':
                # Import is absolute
                for path in paths_to_search:
                        # Iterate through all files in current directory (could be optimized)
                        # If name of file matches module and file extension is .py or .so,
                        # module is found
                        for file in os.listdir(path):
                            if file.split(".")[0] == mod.rstrip().split(".")[0]:
                                if file.split(".")[-1] in ["py", "so"]:
                                    # If detected as module available in sys.path, append to imports
                                    imports[mod.rstrip()] = os.path.join(path, file)
                                    break
                                elif os.path.isdir(os.path.join(path, file)):
                                    # Detected as package, recurse through directories
                                    # TODO: Optimize this code
                                    # (could try adapting relative import code)
                                    if len(mod.split(".")) > 1:
                                        path = os.path.join(path, file)
                                        # Search for each part of package
                                        # split by . and go through directory
                                        for j in mod.split(".")[1:]:
                                            for file2 in os.listdir(path):
                                                if os.path.isdir(os.path.join(path, file2)) and \
                                                        file2 == j:
                                                            path = os.path.join(path, file2)
                                                elif file2.split(".")[0] == mod.split(".")[-1].rstrip():
                                                    imports[mod.rstrip()] = os.path.join(path, file2)
                                                    break
                                    else:
                                        # User imported whole package, treat as __init__.py
                                        imports[mod.rstrip()] = os.path.join(path, file)+"/__init__.py"
                                        break
                            elif mod.rstrip() in sys.builtin_module_names:
                                imports[mod.rstrip()] = mod.rstrip() + " - builtin"
                            else:
                                pass
            else:
                # Import is relative
                os.chdir("/".join(curpath.split("/")[:-1]))
                for part in mod.split(".")[1:]:
                    try:
                        os.chdir(part.rstrip())
                    except NotADirectoryError:
                        for file in os.listdir():
                            if file.split(".")[0] == mod.split(".")[-1].rstrip() and \
                                    file.split(".")[1] in [".py", ".so"]:
                                        imports[mod.rstrip()] = os.path.join(path, file)
                    except FileNotFoundError:
                        for file in os.listdir():
                            if file.split(".")[0] == mod.split(".")[-1].rstrip() and \
                                    file.split(".")[-1] in ["py", "so"]:
                                        imports[mod.rstrip()] = os.path.join(os.getcwd(), file)
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

    for loc in linenumofclass:
        clsname = [filetxt[loc-1]]
        top_leading_whitespace = len(filetxt[loc]) - len(filetxt[loc].lstrip())
        for body in filetxt[loc:]:
            leading_whitespace = len(body) - len(body.lstrip())
            if leading_whitespace < top_leading_whitespace:
                if body != "\n" and len(body) - len(body.lstrip()) != top_leading_whitespace:
                    break
            classlines.append(body)
        fullclasslines.append(classlines)
        classlines = []
    classes = dict(zip(classnames, fullclasslines))
    return classes

# this is what you meant to do, kai...
def get_classes(file):
    classes = dict()
    funcnames = list()
    funcs = dict()
    cache = []
    toplvlcache = []
    toplvlcache.append("on run:")
    saved_indent_class = -1
    saved_indent_func = -1
    class_name = ""

    with open(file, "r") as f:
        for line in f:
            indent_level = len(line) - len(line.lstrip())
            if line.strip() == '':
                continue

            if saved_indent_func != -1 and indent_level > saved_indent_func:
                # Found line within function
                cache.append(line)
            elif saved_indent_func != -1 and indent_level <= saved_indent_func:
                # Found end of function
                saved_indent_func = -1
                funcs[func_name] = cache
                cache = []

            if saved_indent_class != -1 and indent_level <= saved_indent_class:
                # Found end of class, add funcs to class
                classes[class_name] = funcs
                funcs = {}
                saved_indent_class = -1
            elif saved_indent_class == -1 and saved_indent_func == 0:
                # Found toplevel funcs (no class), append to ++main++ class
                classes["++main++"] = funcs

            if line.lstrip().startswith("class "):
                if saved_indent_class != -1 and indent_level <= saved_indent_class:
                    classes[class_name] = funcs
                    funcs = {}
                saved_indent_class = -1
                class_name = line.split("class ")[-1].split("(")[0]
                saved_indent_class = indent_level
                continue

            if line.lstrip().startswith("def ") and saved_indent_func == -1:
                func_name = line.split("def ")[-1].split("(")[0]
                saved_indent_func = indent_level
                cache.append(line)
                continue

            elif saved_indent_func == -1 and saved_indent_class == -1 \
                    and not \
                    line.lstrip().startswith("class ") and not line.startswith("#!"):
                # toplvl code
                toplvlcache.append(line)

        # Flush any remaining classes and functions
        if cache != [] and funcs != {}:
            saved_indent_func = -1
            funcs[func_name] = cache
            classes[class_name] = funcs
            cache = []
            funcs = {}
            saved_indent_class = -1

        if "++main++" in classes.keys():
            classes["++main++"]["on run"] = toplvlcache
        else:
            if len(toplvlcache) != 0:
                classes["++main++"] = {"on run": toplvlcache}


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
            finalfuncnames.append(line)

    for lof in funcnumlines:
        funcname = filetxt[lof-1]
        top_leading_whitespace = len(filetxt[lof]) - len(filetxt[lof].lstrip())
        funcbody = filetxt[lof]
        for body in filetxt[lof:]:
            leading_whitespace = len(body) - len(body.lstrip())
            if leading_whitespace < top_leading_whitespace:
                if body != "\n" and len(body) - len(body.lstrip()) != top_leading_whitespace:
                    break
            funclines.append(body)
        fullfunclines.append(funclines)
        funclines = []

    funcs = dict(zip(finalfuncnames, fullfunclines))

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
                finalfuncnames.append(line)

    for lof in funcnumlines:
        funcname = filetxt[lof-1]
        top_leading_whitespace = len(filetxt[lof]) - len(filetxt[lof].lstrip())
        funcbody = filetxt[lof]
        for body in filetxt[lof:]:
            leading_whitespace = len(body) - len(body.lstrip())
            if leading_whitespace < top_leading_whitespace:
                if body != "\n" and len(body) - len(body.lstrip()) != top_leading_whitespace:
                    break
            funclines.append(body)
        fullfunclines.append(funclines)
        funclines = []

    funcs = dict(zip(finalfuncnames, fullfunclines))

    return funcs

def get_classes_all(file):
    imports = get_imports(file)
    ret_classes = {}
    ret_lint = {}
    for i,v in imports.items():
        if v.endswith(".so") or v.endswith("builtin"):
            uninspectable_classes = {}
            foo = importlib.import_module(i)
            for name, obj in inspect.getmembers(foo):
                if inspect.isclass(obj):
                    try:
                        uninspectable_classes[name] = None
                    except:
                        print("Class is not inspectable")
            ret_classes[v] = uninspectable_classes
            continue
        ret_classes[v] = get_classes(v)
    ret_classes[file] = get_classes(file)
    return ret_classes, (), imports

# get_imports(file)
