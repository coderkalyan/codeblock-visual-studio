from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QFrame
from mainwindow import MainWindow
import sys, inspect
from modulefinder import  ModuleFinder
testvar = "hi"

class Main(MainWindow):
    def __init__(self):
        super().__init__()
        lib = self.get_imports("mainwindow.py")
        print(self.get_vars("mainwindow.MainWindow"))
        print(self.get_functions("mainwindow.MainWindow"))
        print(lib)

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
                    functions[i] = inspect.getsourcelines(getattr(dirvar, i))
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