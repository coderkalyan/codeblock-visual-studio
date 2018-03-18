from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = ["PyQt5.QtWebEngineCore", "PyQt5.QtQuick"])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('mainwindow_controller.py', base=base, targetName = 'codeblock_visual_studio')
]

setup(name='Codeblock Visual Studio',
      version = '0.1a',
      description = 'A code visuaizer for humans.',
      options = dict(build_exe = buildOptions),
      executables = executables)
