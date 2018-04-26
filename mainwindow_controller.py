#!/usr/bin/python3
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QFileDialog, QTreeWidgetItem
from PyQt5.QtSvg import QSvgWidget
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
        # print(self.get_vars("mainwindow.MainWindow"))
        funcs = self.get_functions("./example.py", "MainWindow")
        print(self.get_classes("./blocks.py"), "valuez")
        print([s for s in funcs if "_" in s], "function_list")
        self.create_blocks(funcs)

    def bind(self):
        self.actionOpen.triggered.connect(self.open_file)

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file for reading',
                '', "Python files (*.py)")[0]
        funcs = self.get_classes(filename)
        print(funcs, "function")

    def regenerate_classview(self, file):
        class_list = self.get_classes(file)
        print(class_list, "class list")

    def create_blocks(self, funcs):
        self.function_blocks = self.generate_function_blocks(funcs)
        self.code_blocks = self.generate_code_blocks(funcs)
        for k, v in self.function_blocks.items():
            v.attached = self.code_blocks[k][-1]
            v.attached.bourgeois = v
            v.raise_()
            self.code_blocks[k].append(v)

        for i in list(self.function_blocks.values()):
            i.setGeometry(list(self.function_blocks.values()).index(i)*400, i.geometry().y(), i.geometry().width(), i.geometry().height())
            print(i, "eye")
            for j in range(199):
                if i.attached is not None:
                    print(i.attached, "eye")
                    i.attached.setGeometry(i.geometry().x(), i.geometry().y()+i.geometry().height()-17, i.attached.geometry().width(), i.attached.geometry().height())
                    i.attached.moveChild()
        # svgWidget = HatBlock("test", self.code_blocks['test'][-1], self.codeArea)
        # self.function_blocks.append(svgWidget)
        # svgWidget.show()

    def generate_function_blocks(self, funcs):
        f = 0
        retblocks = {}
        print(funcs, "grr")
        for func, func_def in funcs.items():
            print(func_def[0].strip(), "YEEEE")
            if func != "":
                if "def " in func_def[0].strip():
                    retblocks[func] = HatBlock(func_def[0].strip(), None, self.codeArea)
                else:
                    retblocks[func] = HatBlock(func_def[1].strip(), None, self.codeArea)
            f = f + 1
        return retblocks

    def generate_code_blocks(self, funcs_list):
        f = 0
        retblocks = {}
        funcs = funcs_list
        print(funcs.items(), "items")
        retblocks['test'] = []
        for func, code in funcs.items():
            f = 0
            code.reverse()
            print(code[0], "throwawaygrep")
            print(func, "NTOOOOT")
            retblocks[func] = []
            for line in code:
                if func != "" and "def " not in line:
                    if f == 0:
                        retblocks[func].append(CodeBlock(line, None, self.codeArea))
                    else:
                        retblocks[func].append(CodeBlock(line, retblocks[func][f-1], self.codeArea))
                        print(len(retblocks), " yes")
                    f = f + 1
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
                    functions[i] = inspect.getsource(getattr(dirvar, i)).splitlines()
                    print([s for s in functions[i] if "            " in s], "function_list")
                except TypeError:
                    pass
        return functions

    def get_classes(self, file):
        classes = {}
        try:
            spec = importlib.util.spec_from_file_location(file, file)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            for name, obj in inspect.getmembers(foo):
                if inspect.isclass(obj):
                    classes[name] = obj
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


