import os
import re

x = 11
imports = "os","re"

for vars in dir():
    if vars.startswith("__") == 0 and vars not in imports:
        print (vars)
