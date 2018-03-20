# Welcome to the official repository for Codeblock Visual Studio! #

What is Codeblock Visual Studio? The final goal is to create a simple,
block-based IDE that can code in powerful languages such as Python instead
of a "lite" language. (Looking at you, Scratch.)

# IMPORTANT: THERE IS A LOT OF REPOSITORY WORK TO DO #

Due to moving from a one-person project to an actually good structured one,
we need to set up the repository branch systems properly (also I will be pretty mad
if you manage to delete all my work)

When you are developing, open a new Issue (see left) describing what you are doing
and create a branch for that issue. Open a pull request when you are finished.

DO NOT EDIT THE MASTER BRANCH OR DEVELOP BRANCH UNLESS EXPLICITLY GIVEN PERMISSION.

## Instructions & To-do List ##

* Deployment/building the application: we use cx_Freeze to freeze the python scripts into an executable.
	* Prerequisites: `pip3 install cx_Freeze`
	* In order to build, run `python3 setup.py build`
		* This has the side effect of including all of the Qt Libraries, resulting in an unnecessarily huge executable. This issue is in the process of being fixed by adding to the "exclude" list in setup.py. Please help add to the list.
		* This command is also platform specific, e.g. you will get Linux executable on Linux, EXE on Windows, etc. There is no way of cross-compiling as of now.
	* In order to create a distributable file (such as an installer):
		* `python3 setup.py bdist` on Linux will build .tar.gz (not recommended because we can manually create a DEB)
		* `python3 setup.py bdist_msi` on Windows creates MSI installer
		* `python3 setup.py bdist_dmg` on Mac builds DMG "installer" (alternatively, use `bdist_mac` to generate just APP)
* To-do's will be posted in the issue tracker, however here are the most important ones:
	* Change block-dragging system to use Qt's parenting system, as the current system is extremely inefficient
	* Get flow indicator support ("if" blocks and the like), test implementation in blocks.py (just run)