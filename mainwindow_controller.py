#!/usr/bin/python3
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QFileDialog, QTreeWidgetItem
from mainwindow import MainWindow
import sys
import importlib.util
import inspect
from modulefinder import ModuleFinder
from blocks import *
testvar = "hi"


class Main(MainWindow):
    def __init__(self):
        super().__init__()
        self.bind()
        self.classViewFileIndex = {}

    def bind(self):
        self.actionOpen.triggered.connect(self.open_file)
        self.classView.itemDoubleClicked.connect(self.classview_openclass)

    def classview_openclass(self):
        if self.classView.selectedItems()[0].parent().text(0).split(".")[1] == "py":
            inspect_typed = self.classView.selectedItems(
            )[0].parent().text(0).split(".")[0]
        else:
            inspect_typed = self.classView.selectedItems()[0].parent().text(0)
        self.create_blocks(self.get_functions(
            self.classViewFileIndex[inspect_typed +
                                    "."+self.classView.selectedItems()[0].text(0)],
            self.classView.selectedItems()[0].text(0)))

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file for reading',
                                               '', "Python files (*.py)")[0]
        self.regenerate_classview(filename)

    def regenerate_classview(self, file):
        class_list = self.get_classes(file)
        class_list_sorted = {}
        for k, v in class_list.items():
            filesplit = str(v).split("'")[1::2][0].split(".")
            if len(filesplit) > 2:
                # use Package-style naming
                filename = ".".join(filesplit[:2])
            else:
                # use Module-style naming (.py extension)
                filename = ".".join([filesplit[0], "py"])
            class_list_sorted[filename] = {}
            for i, j in class_list.items():
                if len(filename.split(".")) > 2:
                    filecompare = filename
                else:
                    filecompare = filename.split(".")[0]
                if filecompare in str(j):
                    class_list_sorted[filename][i] = j
        class_tree_index = {}
        print("generating tree view...")
        self.classView.clear()
        ind0 = 0
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
        self.function_blocks = self.generate_function_blocks(funcs)
        self.code_blocks = self.generate_code_blocks(funcs)
        for k, v in self.function_blocks.items():
            print(v, self.code_blocks[k][-1].content, "attach_child")
            v.attach_child(self.code_blocks[k][0])
            v.raiseEvent()
            self.code_blocks[k].append(v)

        for i in list(self.function_blocks.values()):
            i.move_recurse(list(self.function_blocks.values()).index(i)*400, i.geometry().y())
            print(i, "eye")
        # svgWidget = HatBlock("test", self.code_blocks['test'][-1], self.codeArea)
        # self.function_blocks.append(svgWidget)
        # svgWidget.show()
        for bar in self.code_blocks['ctrlbar']:
            bar.adjust_bar()
            bar.show()
        print(self.code_blocks['ctrlbar'], "ctrlbar")

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
        retblocks['test'] = []
        retblocks['ctrlbar'] = []
        ctrl_bar_count = 0
        for func, code in funcs.items():
            f = 0
            retblocks[func] = []
            control_block_map = {}
            for line in code:
                if func != "" and "def " not in line:
                    if (len(line) - len(line.lstrip())) in control_block_map.keys():
                        # CtrlBottom detected (must be before ifblock)
                        print(line, control_block_map, "control_map")
                        retblocks[func].append(CtrlBottom(line, parent=self.codeArea))
                        code.insert(f+1, line)
                        retblocks['ctrlbar'].append(CtrlBar(parent=self.codeArea))
                        print(retblocks['ctrlbar'])
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
                        retblocks[func].append(CodeBlock(line, parent=self.codeArea))
                    if f != 0:
                        retblocks[func][f-1].attach_child(retblocks[func][f])
                    f = f + 1
                    print(line)
        print(control_block_map, "controlmap remain")
        return retblocks

    def get_imports(self, file):
        finder = ModuleFinder()
        finder.run_script(file)
        im = []
        for name, mod in finder.modules.items():
            im.append(name)
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


