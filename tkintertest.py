from tkinter import *
import sys, os

root = Tk()
root.title("Tkinter Test GUI!")
root.geometry('350x200')

def peekaboo():
    label2.grid(column=0, row=2)


label1 = Label(root, text="Hello!", font=("Ubuntu", 45))
label1.grid(column=0, row=0)

button = Button(root, command=peekaboo, text="Press me!", font=("Ubuntu", 25))
button.grid(column=0, row=1)

label2 = Label(root, text="Peek-a-boo!")
label2.grid(column=0, row=2)
label2.grid_forget()

root.mainloop()
