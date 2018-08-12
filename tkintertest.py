from tkinter import *
import sys, os

root = Tk()
root.title("Tkinter Test GUI!")
root.geometry('350x200')

class BasicBlock(QWidget):
    def __init__(self, content='print("Hello, World")', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.content = content
        self.child = None
        self.parent = None
        self.comment = None
        self.text_size = 50
        self.scale = QDesktopWidget().screenGeometry().height()/1080
        self.dragging = -10
        self.width = 100
        self.height = 100
        self.attaches = True
        self.color = random.choice(["red", "orange", "yellow", "green", "blue"])

        temp = self.geometry()
        self.setGeometry(temp.x(), temp.y(),
                temp.x() + self.width*self.scale, temp.y() + self.height*self.scale)

        blocks.append(self)

    @property
    def content(self):
        return self.content_

    @content.setter
    def content(self, new_content):
        self.content_ = new_content
        font = QFont("times", 24)
        metric = QFontMetrics(font)
        text_width = QFontMetrics.width(metric, new_content)
        self.width = text_width
        #self.height = metric.height()
        cur_geom = self.geometry()
        self.setGeometry(cur_geom.x(), cur_geom.y(), text_width, 15)

    def move(self, delta_x, delta_y):
        """
        Moves the current block RELATIVE to start position
        :param delta_x: amount to move x
        :param delta_y: amount to move y
        :return new position of this block
        """

        geom = self.geometry()
        self.setGeometry(geom.x() + delta_x, geom.y() + delta_y,
                geom.width() + delta_x, geom.height() + delta_y)

        return geom.x() + delta_x, geom.y() + delta_y

    def move_to(self, x, y):
        """
        Moves the current block to a position
        :param x: x position to move to
        :param y: y position to move to
        """

        geom = self.geometry()
        print(self.height)
        self.setGeometry(x, y, self.width, self.height)

    def attach_child(self, child):
        self.child = child
        self.child.parent = self
        temp = self.child.geometry()
        cur = self.geometry()
        #self.child.setGeometry(cur.x(), cur.y() + self.height - 15, cur.x() + temp.width(),
        #                       self.height + temp.height() - 15)
        self.child.setGeometry(cur.x(), cur.y() + self.height - 15, temp.width(),
                               temp.height())
        # self.child.setParent(self)
        self.raiseEvent()

    def detach_child(self):
        if self.child is None:
            return
        self.child.parent = None
        self.child = None

    def detach_parent(self):
        if self.parent is None:
            return

        self.parent.child = None
        self.parent = None

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor(self.color))
        painter.setBrush(QColor(self.color))
        painter.setFont(QFont("times", 50))
        painter.setRenderHint(QPainter.Antialiasing)

        geom = self.geometry()
        painter.drawRect(QRect(0, 0, geom.width() - geom.x(), geom.height() - geom.y()))
        painter.end()

    def mousePressEvent(self, event):
        self.dragging = self.mapToGlobal(event.pos())
        self.drag_geom = (self.pos())
        self.raiseEvent()

    def move_recurse(self, x, y):
        self.move_to(x, y)
        if self.child is not None:
            self.child.move_recurse(x, y + self.geometry().height() - 15)
        if self.comment is not None:
            self.comment.move_to(x+self.geometry().width()-5, y)

    def mouseMoveEvent(self, event):
        if self.dragging == -10:
            return

        pos = self.mapToGlobal(event.pos() - self.dragging)
        deltax = abs(self.geometry().x() - self.drag_geom.x())
        deltay = abs(self.geometry().y() - self.drag_geom.y())
        if deltax > 10 or deltay > 10:
            self.detach_parent()

        posx = pos.x()
        posy = pos.y()
        cur = self
        self.move_recurse(self.drag_geom.x() + posx, self.drag_geom.y() + posy)

    def mouseReleaseEvent(self, event):
        self.dragging = -10

    def raiseEvent(self):
        self.raise_()
        self.show()
        if self.child is not None:
            self.child.raiseEvent()
            self.raise_()
            self.child.show()
        if self.comment is not None:
            self.comment.raise_()
            self.comment.show()

def peekaboo(((((()))))):
    label2.grid(column=0, row=2)

def sayhi():
    print("hi")
    print("hello")
    print("greetings")

    print("bonjour")
    print("hola")
    print("konichiwa")
    print("hallo")

def saybye():
    print("bye")

label1 = Label(root, text="Hello!", font=("Ubuntu", 45))
label1.grid(column=0, row=0)

button = Button(root, command=peekaboo, text="Press me!", font=("Ubuntu", 25))
button.grid(column=0, row=1)

label2 = Label(root, text="Peek-a-boo!")
label2.grid(column=0, row=2)
label2.grid_forget()

root.mainloop()
