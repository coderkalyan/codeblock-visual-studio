from cx_Freeze import setup, Executable
import os, pkgutil
import PyQt5

# Dependencies are automatically detected, but it might need
# fine tuning.
pyqt_exclude = [name for _, name, _ in pkgutil.iter_modules([os.path.dirname(PyQt5.__file__)])]
pyqt_exclude.remove('QtWidgets')
pyqt_exclude.remove('QtCore')
pyqt_exclude.remove('QtGui')
pyqt_exclude.remove('Qt')
for i in pyqt_exclude:
    pyqt_exclude[pyqt_exclude.index(i)] = 'PyQt5.' + i
    print("exluding", i)

print("exclude list is:", pyqt_exclude)
print("is this correct?")

buildOptions = {'packages': [], 'excludes': pyqt_exclude}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('mainwindow_controller.py', base=base, targetName = 'codeblock_visual_studio')
]

setup(name='Codeblock Visual Studio',
      version = '0.1a',
      description = 'A code visuaizer for humans.',
      options = {'build_exe': buildOptions},
      executables = executables)
