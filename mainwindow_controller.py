from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget, QFrame
from mainwindow import MainWindow
import sys,imsp
from modulefinder import  ModuleFinder
testvar = "hi"

class Main(MainWindow):
    def __init__(self):
        super().__init__()
        lib = self.get_imports("mainwindow.py")
        print(self.get_vars("mainwindow.MainWindow"))
        print(lib)

    def get_imports(self, file):
        finder = ModuleFinder()
        finder.run_script("main.py")
        im = []
        for name, mod in finder.modules.items():
            im.append(name)
        return im

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
            if getattr(dirvar, attr) == getattr(super(dirvar), attr):
                inherited.append(attr)
            else:
                defined.append()
        return returnvar


if __name__ == "__main__":
    app = QApplication(sys.argv)
    maine = Main()
    maine.show()
    print(dir("mainwindow_controller.py"))
    sys.exit(app.exec_())