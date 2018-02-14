#!/usr/bin/python3
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QFrame
from PyQt5.QtSvg import QSvgWidget
from mainwindow import MainWindow
from collections import defaultdict
import sys, inspect
from modulefinder import  ModuleFinder
from blocks import *
testvar = "hi"

class Main(MainWindow):
    def __init__(self):
        super().__init__()
        # print(self.get_vars("mainwindow.MainWindow"))
        funcs = self.get_functions("example.MainWindow")
        self.create_blocks(funcs)
        self.function_blocks = self.generate_function_blocks(funcs), "ineedabetterwaytodebug"

    def create_blocks(self, funcs):
        self.code_blocks = self.generate_code_blocks(funcs)
        # svgWidget = HatBlock("test", self.code_blocks['test'][-1], self.codeArea)
        # self.function_blocks.append(svgWidget)
        print(funcs.items(), "NOOTTT")
        # svgWidget.show()


    def generate_function_blocks(self, funcs):
        f = 0
        retblocks = {}
        print(funcs, "grr")
        for func, func_def in funcs.items():
            print(func_def[-1].strip(), "YEEEE")
            if func != "":
                retblocks[func] = (HatBlock(func_def[-1].strip(), None, self.codeArea))
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
                print(retblocks[func])
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

    def get_functions(self, file):
        try:
            importvar = __import__(file)
            dirvar = importvar
        except ImportError:
            importvar = __import__(file.split(".")[0])
            dirvar = getattr(importvar, file.split(".")[1])
        functions = {}
        for i in dir(dirvar):
            if inspect.isroutine(getattr(dirvar, i)):
                try:
                    functions[i] = inspect.getsource(getattr(dirvar, i)).splitlines()
                except TypeError:
                    pass
        return functions


    def get_vars(self, file):
        inherited = []
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


