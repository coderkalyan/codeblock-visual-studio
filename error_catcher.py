import sys, os

def get_errors(file):
    lint = os.popen("flake8 " + file).read()

    print(lint)

if __name__ == "__main__":
    get_errors("tkintertest.py")
