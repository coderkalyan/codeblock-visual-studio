#!/usr/bin/python3
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QFrame
from PyQt5.QtSvg import QSvgWidget
from mainwindow import MainWindow
import sys, inspect
from modulefinder import  ModuleFinder
from blocks import *
testvar = "hi"

class Main(MainWindow):
    def __init__(self):
        super().__init__()
        lib = self.get_imports("mainwindow.py")
        print(self.get_vars("mainwindow.MainWindow"))
        funcs = self.get_functions("example.MainWindow")
        self.function_blocks = []
        self.generate_function_blocks(funcs)
        svgWidget = HatBlock("test", self.function_blocks[-1], self.codeArea)
        self.function_blocks.append(svgWidget)
        svgWidget.show()
        print(funcs, "FUNCS")
        for i in funcs.items():
            print(i[1][0], "func")
        print(lib)

    def generate_function_blocks(self, funcs):
        f = 0
        for func in funcs.items():
            if func != "":
                if f == 0:
                    self.function_blocks.append(CodeBlock(func[1][0].strip(), None, self.codeArea))
                else:
                    self.function_blocks.append(CodeBlock(func[1][0].strip(), self.function_blocks[f-1], self.codeArea))
                    print(len(self.function_blocks), " yes")
            f = f + 1

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
