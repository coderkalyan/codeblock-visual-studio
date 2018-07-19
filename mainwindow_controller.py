#!/usr/bin/python3
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QFileDialog, QTreeWidgetItem
from mainwindow import MainWindow
from about_dialog import AboutDialog
import icons.icons_rc
import sys
import importlib.util
import inspect
import error_catcher
import interpreter
from modulefinder import ModuleFinder
from blocks import *
testvar = "hi"


class Main(MainWindow):
    def __init__(self):
        super().__init__()
        self.about_dialog = AboutDialog()
        self.about_dialog.hide()
        self.bind()
        self.classViewFileIndex = {}
        self.lines = []
        self.lint = ()
        self.class_list = {}

    def bind(self):
        self.actionOpen.triggered.connect(self.open_file)
        self.actionAbout.triggered.connect(self.about_dialog.show)
        self.classView.itemDoubleClicked.connect(self.classview_openclass)

    def classview_openclass(self):
        # if self.classView.selectedItems()[0].parent().text(0).split(".")[1] == "py":
        #     inspect_typed = self.classView.selectedItems(
        #     )[0].parent().text(0).split(".")[0]
        # else:
        #     inspect_typed = self.classView.selectedItems()[0].parent().text(0)
        selected_item = self.classView.selectedItems()[0].parent().text(0)
        if selected_item.split(".")[-1] in ["py", "so"]:
            inspect_typed = selected_item.split(".")[0]
        else:
            inspect_typed = selected_item
        # self.create_blocks(self.get_functions(
        #     self.class_list[],
        #     self.classView.selectedItems()[0].text(0)))
        print(self.class_list[2][inspect_typed], "throwawaygrep")
        with open(self.class_list[2][inspect_typed]) as f:
            self.lines = []
            for l in f:
                self.lines.append(l.lstrip())
        print(self.lines, "selflines")
        for line in self.lines:
            print(line.rstrip(), "derp")
        self.lint = error_catcher.get_lint(self.class_list[2][inspect_typed])
        self.create_blocks(self.class_list[0][self.class_list[2][inspect_typed]][self.classView.selectedItems()[0].text(0)])

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file for reading',
                                               '', "Python files (*.py)")[0]
        self.regenerate_classview(filename)

    def regenerate_classview(self, file):
        try:
            # Get everything in format (classes, lint, imports)
            # classes is in format {file: {class: {functions: {list_of_source}}}}
            # Lint is in format {file: [list_of_lint_warns]}
            # Imports is in format {module: file}
            self.class_list = interpreter.get_classes_all(file)
        except:
            self.class_list = {}
        class_list_sorted = {}
        for k, v in self.class_list[0].items():
            # Get name of modules
            try:
                filename = list(self.class_list[2].keys())[list(self.class_list[2].values()).index(k)]
            except ValueError:
                print("assuming main file, skipping")
                filename = file.split("/")[-1]
            if len(filename.split(".")) < 2:
                # Use module-style naming (.py or .so extension)
                filename = filename+"."+k.split(".")[-1]

            class_list_sorted[filename] = {}
            print(v)
            for i,j in v.items():
                class_list_sorted[filename][i] = None
            # for i, j in self.class_list[0].items():
            #     if len(filename.split(".")) > 2:
            #         filecompare = filename
            #     else:
            #         filecompare = filename.split(".")[0]
            #     if filecompare in str(j):
            #         class_list_sorted[filename][i] = j
        class_tree_index = {}
        print("generating tree view...")
        self.classView.clear()
        ind0 = 0
        # class_list_sorted should be in the format {module_name: {class_name:[arbitrary val]}}
        for k2, v2 in class_list_sorted.items():
            class_tree_index[ind0] = QTreeWidgetItem(self.classView)
            class_tree_index[ind0].setText(0, k2)
            for k3, v3 in v2.items():
                class_tree_index[v3] = QTreeWidgetItem(class_tree_index[ind0])
                class_tree_index[v3].setText(0, k3)
            ind0 = ind0 + 1

    def create_blocks(self, funcs):
        for child in self.codeArea.children():
            child.deleteLater()
        self.codeArea.setUpdatesEnabled(True)
        print(funcs, "funcs")
        self.function_blocks = self.generate_function_blocks(funcs)
        self.code_blocks = self.generate_code_blocks(funcs)
        for k, v in self.function_blocks.items():
            print(v, self.code_blocks[k][-1].content, "attach_child")
            v.attach_child(self.code_blocks[k][0])
            v.raiseEvent()
            self.code_blocks[k].append(v)

        # svgWidget = HatBlock("test", self.code_blocks['test'][-1], self.codeArea)
        # self.function_blocks.append(svgWidget)
        # svgWidget.show()
        for i in list(self.function_blocks.values()):
            i.move_recurse(list(self.function_blocks.values()).index(i)*400, i.geometry().y())
            i.raiseEvent()
            print(i, "eye")

        print(self.code_blocks['ctrlbar'], "ctrlbar")
        for bar in self.code_blocks['ctrlbar']:
            bar.adjust_bar()
            bar.show()
            bar.raise_()

        for comment in self.code_blocks['comments']:
            comment.adjust()
            comment.show()

    def generate_function_blocks(self, funcs):
        f = 0
        retblocks = {}
        for func, func_def in funcs.items():
            if func != "":
                if "def " in func_def[0].strip():
                    retblocks[func] = CapBlock(func_def[0].strip(), parent=self.codeArea)
                else:
                    retblocks[func] = CapBlock(func_def[1].strip(), parent=self.codeArea)
            f = f + 1
        return retblocks

    def generate_code_blocks(self, funcs_list):
        f = 0
        retblocks = {}
        funcs = funcs_list
        retblocks['comments'] = []
        retblocks['ctrlbar'] = []
        ctrl_bar_count = 0
        for func, code in funcs.items():
            f = 0
            retblocks[func] = []
            control_block_map = {}
            not_done = True
            for line in code:
                if func != "" and "def " not in line:
                    if line.lstrip().startswith("#"):
                        self.lint[2][line.lstrip()] = self.lines.index(line.lstrip())+1
                        continue
                    print(line, "thisisline")
                    line_leading_whitespace = len(line) - len(line.lstrip())
                    if line_leading_whitespace in control_block_map.keys():
                        # CtrlBottom detected (must be before ifblock)
                        print(line, line_leading_whitespace, control_block_map, "control_map")
                        sorted_keys = list(control_block_map.keys())
                        sorted_keys.sort()
                        if not line_leading_whitespace == \
                                sorted_keys[-1]:
                                    print(sorted_keys[-1], line_leading_whitespace, "sorted keys")
                                    line = line.lstrip()
                                    for l in range(sorted_keys[-1]):
                                        print(l)
                                        line = " " + line
                                        print(line)
                        retblocks[func].append(CtrlBottom(line, parent=self.codeArea))
                        code.insert(f+1, line)
                        retblocks['ctrlbar'].append(CtrlBar(parent=self.codeArea))
                        retblocks['ctrlbar'][ctrl_bar_count].attach_top(control_block_map[len(line) - len(line.lstrip())])
                        retblocks['ctrlbar'][ctrl_bar_count].attach_bottom(retblocks[func][f])
                        print(control_block_map, 'controlmap in prog')
                        ctrl_bar_count = ctrl_bar_count + 1
                        del control_block_map[len(line) - len(line.lstrip())]
                    elif line.strip()[-1] == ':':
                        # Indented Block - use CtrlTop block
                        retblocks[func].append(CtrlTop(line, parent=self.codeArea))
                        # Store [whitespace, satisfied] values for ctrltop
                        control_block_map[len(line) - len(line.lstrip())] = retblocks[func][f]
                    else:
                        # Just a regular CodeBlock
                        try:
                            if self.lines.index(line.lstrip())+1 in self.lint[0].values():
                                color = "red"
                                lintline = list(self.lint[0].keys())[list(self.lint[0].values()).index(self.lines.index(line.lstrip())+1)]
                            elif self.lines.index(line.lstrip())+1 in self.lint[1].values():
                                color = "#FFBB33"
                                lintline = list(self.lint[1].keys())[list(self.lint[1].values()).index(self.lines.index(line.lstrip())+1)]
                            else:
                                color = "#496BD3"
                                lintline = None
                        except ValueError as v:
                            print(self.lines.index(line.lstrip()))
                            print(line, "thisislinevalue")
                            color = "#496BD3"
                            lintline = None
                            print(v, "ValeError")
                        print(lintline, "lintline")
                        retblocks[func].append(CodeBlock(line, color, parent=self.codeArea))
                        if lintline is not None:
                            retblocks['comments'].append(CommentBubble(lintline, retblocks[func][f], parent=self.codeArea))
                    if f != 0:
                        retblocks[func][f-1].attach_child(retblocks[func][f])
                    f = f + 1
                    print(line)
                    if f == len(code)-1 and len(control_block_map) > 0 and not_done:
                        # CtrlBottom detected (must be before ifblock)
                        print(line, line_leading_whitespace, control_block_map, "control_map")
                        sorted_keys = list(control_block_map.keys())
                        sorted_keys.sort()
                        if not line_leading_whitespace == \
                                sorted_keys[-1]:
                                    print(sorted_keys[-1], line_leading_whitespace, "sorted keys")
                                    line = line.lstrip()
                                    for l in range(sorted_keys[-1]):
                                        print(l)
                                        line = " " + line
                                        print(line)

                        retblocks[func].append(CtrlBottom(line, parent=self.codeArea))
                        code.insert(f+1, line)
                        retblocks['ctrlbar'].append(CtrlBar(parent=self.codeArea))
                        retblocks['ctrlbar'][ctrl_bar_count].attach_top(control_block_map[len(line) - len(line.lstrip())])
                        retblocks['ctrlbar'][ctrl_bar_count].attach_bottom(retblocks[func][f])
                        print(control_block_map, 'controlmap in prog')
                        ctrl_bar_count = ctrl_bar_count + 1
                        del control_block_map[len(line) - len(line.lstrip())]
                        not_done = False
        print(control_block_map, "controlmap remain")
        return retblocks

    def get_imports(self, file):
        finder = ModuleFinder()
        finder.run_script(file)
        im = []
        for name, mod in finder.modules.items():
            im.append(name)
        print(im, "imports")
        return im

    def get_functions(self, file, class_name):
        spec = importlib.util.spec_from_file_location("foo", file)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        dirvar = getattr(foo, class_name)
        functions = {}
        for i in dir(dirvar):
            if inspect.isroutine(getattr(dirvar, i)):
                try:
                    functions[i] = list(filter(None, inspect.getsource(
                        getattr(dirvar, i)).splitlines()))
                    print([s for s in functions[i]
                           if "            " in s], "function_list")
                except TypeError:
                    pass
        return functions

    def get_classes(self, file):
        classes = {}
        try:
            sys.path.append("/".join(file.split("/")[:-1]))
            print(file)
            spec = importlib.util.spec_from_file_location(
                file.split("/")[-1], file)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            for name, obj in inspect.getmembers(foo):
                if inspect.isclass(obj):
                    classes[name] = obj
                    print(str(classes[name]).split("'")[1::2][0], "objc")
                    try:
                        self.classViewFileIndex[
                            str(classes[name]).split("'")[1::2][0]] = inspect.getfile(obj)
                    except TypeError:
                        print(
                            obj, "is likely main file, using circumventation measures.")
                        self.classViewFileIndex[
                            str(classes[name]).split("'")[1::2][0].replace(".py", "")] = file
        except FileNotFoundError:
            print("invalid file")
            # do stuff
        return classes


    def get_vars(self, file):
        defined = []
        try:
            importvar = __import__(file)
            dirvar = importvar
            returnvar = dir(dirvar)
        except ImportError:
            importvar = __import__(file.split(".")[0])
            dirvar = getattr(importvar, file.split(".")[1])
            returnvar = dir(dirvar)
        for attr in returnvar:
            if not callable(getattr(dirvar, attr)):
                defined.append(attr)
            else:
                print(attr)
        returnvar = defined
        return returnvar


if __name__ == "__main__":
    app = QApplication(sys.argv)
    maine = Main()
    maine.show()
    print(dir("mainwindow_controller.py"))
    sys.exit(app.exec_())


