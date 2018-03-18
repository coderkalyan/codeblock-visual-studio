# Building executable on native platform (execute this first)
# WARNING: cx_Freeze will only generate an executable for the platform it runs on.

python3 setup.py build

# Building for MacOS, first command builds dmg, second builds .app, select one
# Only works on MacOS...

python3 setup.py bdist_dmg
python3 setup.py bdist_mac

# Building for Windows, creates an MSI installer
# Only works on Windows

python3 setup.py bdist_msi
