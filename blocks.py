#!/usr/bin/python3
import random

from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget
from PyQt5.QtCore import QRect, QPoint, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QColor, QImage, QFontMetrics
import time

blocks = []


class BasicBlock(QWidget):
    def __init__(self, content='print("Hello, World")', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.content = content
        self.child = None
        self.parent = None
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

class CodeBlock(BasicBlock):
    def __init__(self, text, color="#496BD3", *args, **kwargs):
        super().__init__(text, *args, **kwargs)

        self.color = "#496BD3"
        font = QFont("Comic Sans MS", 15)
        metric = QFontMetrics(font)
        if QFontMetrics.width(metric, self.content) + 30 > 150*self.scale:
            self.width = QFontMetrics.width(metric, self.content) + 30
        else:
            self.width = 150*self.scale
        self.height = metric.height() + 30*self.scale
        print(self.height, "hight")
        self.text_size = 50

        temp = self.geometry()
        self.setGeometry(temp.x(), temp.y(), temp.x() + self.width, self.height)
        self.repaint()

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor(self.color))
        painter.setBrush(QColor(self.color))
        painter.setFont(QFont("Comic Sans MS", 15))
        painter.setRenderHint(QPainter.Antialiasing)
        #painter.drawRoundedRect(0, 5, self.geometry().width() - 5, self.geometry().height() - 7, 3, 3)
        painter.drawChord(QRect(20, self.height-50, 45, 45), 180 * 16, 180 * 16)
        geom = self.geometry()
        painter.drawRoundedRect(QRect(0, 0, geom.width(), geom.height() - 15), 6*self.scale, 6*self.scale)
        painter.setBrush(QColor("white"))
        painter.setPen(QColor("white"))
        painter.drawText(10, self.height/2, self.content)
        painter.drawChord(QRect(20, -37, 45, 45), 180 * 16, 180 * 16)
        painter.end()



class CapBlock(BasicBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.color = "dark green"
        font = QFont("Comic Sans MS", 15)
        metric = QFontMetrics(font)
        print(self.scale, QDesktopWidget().screenGeometry(), "scale")
        self.height = metric.height() + 56*self.scale
        print(self.height)
        if QFontMetrics.width(metric, self.content) + 30 > 150*self.scale:
            self.width = QFontMetrics.width(metric, self.content) + 30
        else:
            self.width = 150*self.scale
        self.text_size = 50
        self.attaches = False

        temp = self.geometry()
        self.setGeometry(temp.x(), temp.y(), temp.x() + self.width, self.height)
        self.repaint()

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor(self.color))
        painter.setBrush(QColor(self.color))
        painter.setFont(QFont("Comic Sans MS", 15))
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawRoundedRect(QRect(0, 30*self.scale, self.geometry().width(), self.height-16-29*self.scale),
                6*self.scale, 6*self.scale)
        painter.drawChord(QRect(0, 5, self.width, 60*self.scale), 0 * 16, 180 * 16)
        geom = self.geometry()
        painter.drawChord(QRect(20, self.height-51, 45, 45), 180 * 16, 180 * 16)
        #painter.drawRoundedRect(QRect(0, 20, geom.width(), geom.height() - 15), 3, 3)
        painter.setBrush(QColor("white"))
        painter.setPen(QColor("white"))
        # painter.drawChord(QRect(20, 60, 45, 45), 180 * 16, 180 * 16)
        painter.drawText(10, 50*self.scale, self.content)
        painter.end()


class CtrlTop(BasicBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.color = "orange"
        self.bar = None
        font = QFont("Comic Sans MS", 15)
        metric = QFontMetrics(font)
        if QFontMetrics.width(metric, self.content) + 30 > 100:
            self.width = QFontMetrics.width(metric, self.content) + 30
        else:
            self.width = 150
        self.height = (metric.height() + 30)*self.scale
        print(self.height, "hight")
        self.text_size = 50

        temp = self.geometry()
        self.setGeometry(temp.x(), temp.y(), temp.x() + self.width, self.height)
        self.repaint()

    def move_recurse(self, x, y):
        self.move_to(x, y)
        if self.bar is not None:
            print(x, y)
            print(self.bar.geometry(), "bargeom report")
            self.bar.move_to(x, y)
        if self.child is not None:
            self.child.move_recurse(x + 20, y + self.geometry().height() - 15)

    def paintEvent(self, QPaintEvent):
        print("paintevent")
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor(self.color))
        painter.setBrush(QColor(self.color))
        painter.setFont(QFont("Comic Sans MS", 15))
        painter.setRenderHint(QPainter.Antialiasing)
        #painter.drawRoundedRect(0, 5, self.geometry().width() - 5, self.geometry().height() - 7, 3, 3)
        painter.drawChord(QRect(40, self.height-50, 45, 45), 180 * 16, 180 * 16)
        geom = self.geometry()
        painter.drawRoundedRect(QRect(0, 0, geom.width(), geom.height() - 15), 6*self.scale, 6*self.scale)
        painter.setBrush(QColor("white"))
        painter.setPen(QColor("white"))
        painter.drawText(10, 25*self.scale, self.content)
        painter.drawChord(QRect(20, -37, 45, 45), 180 * 16, 180 * 16)
        painter.end()


class CtrlBar(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = 23
        self.height = 120
        self.color = "orange"
        self.scale = QDesktopWidget().screenGeometry().height()/1080

        self.repaint()

    def attach_top(self, block: CtrlTop):
        self.setGeometry(block.geometry().x(), block.geometry().y(), self.width, self.height)
        self.top = block
        block.bar = self

    def attach_bottom(self, block):
        self.setGeometry(self.geometry().x(), self.geometry().y(),
                block.geometry().x() - self.top.geometry().x(),
                block.geometry().y() - self.top.geometry().y())
        self.bottom = block
        self.height = block.geometry().y() - self.top.geometry().y() + 10
        print(self.geometry(), "bargeom")
        print(self.top.geometry(), self.bottom.geometry())

    def adjust_bar(self):
        print(self.top.geometry(), self.bottom.geometry(), "newbot")
        global_pos_top = self.mapToGlobal(self.top.pos())
        global_pos_bottom = self.mapToGlobal(self.bottom.pos())
        self.setGeometry(self.top.geometry().x(), self.top.geometry().y(),
                self.width,
                self.bottom.geometry().y() - self.top.geometry().y() + 10)
        self.height = self.bottom.geometry().y() - self.top.geometry().y() + 10

    def move_to(self, x, y):
        """
        Moves the current block to a position
        :param x: x position to move to
        :param y: y position to move to
        """

        geom = self.geometry()
        self.setGeometry(x, y, self.width, self.height)

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor(self.color))
        painter.setBrush(QColor(self.color))
        painter.setFont(QFont("Comic Sans MS", 15))
        painter.setRenderHint(QPainter.Antialiasing)
        geom = self.geometry()
        painter.drawRoundedRect(QRect(0, 0, geom.width(), geom.height()), 6*self.scale, 6*self.scale)
        painter.end()


class CtrlBottom(BasicBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.color = "orange"
        font = QFont("Comic Sans MS", 15)
        metric = QFontMetrics(font)
        if QFontMetrics.width(metric, self.content) + 30 > 100:
            self.width = QFontMetrics.width(metric, self.content) + 30
        else:
            self.width = 150
        self.height = (metric.height() + 30)*self.scale
        print(self.height, "hight")
        self.text_size = 50

        temp = self.geometry()
        self.setGeometry(temp.x(), temp.y(), temp.x() + self.width, self.height)
        self.repaint()

    def move_recurse(self, x, y):
        self.move_to(x-20, y)
        if self.child is not None:
            self.child.move_recurse(x-20, y + self.geometry().height() - 15)

    # Override mouse events for CtrlBottom so that the user cannot drag it
    # independently from CtrlTop
    def mousePressEvent(self, event):
        #Override mouseReleaseEvent method from BasicBlock
        pass

    def mouseMoveEvent(self, event):
        #Override mouseReleaseEvent method from BasicBlock
        pass

    def mouseReleaseEvent(self, event):
        #Override mouseReleaseEvent method from BasicBlock
        pass

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor(self.color))
        painter.setBrush(QColor(self.color))
        painter.setRenderHint(QPainter.Antialiasing)
        #painter.drawRoundedRect(0, 5, self.geometry().width() - 5, self.geometry().height() - 7, 3, 3)
        painter.drawChord(QRect(20, self.height-50, 45, 45), 180 * 16, 180 * 16)
        geom = self.geometry()
        painter.drawRoundedRect(QRect(0, 0, geom.width(), geom.height() - 15), 6*self.scale, 6*self.scale)
        painter.setBrush(QColor("white"))
        painter.setPen(QColor("white"))
        painter.end()




if __name__ == "__main__":
    app = QApplication([])

    w = QWidget()
    w.setMinimumWidth(500)
    w.setMinimumHeight(500)
    w.setStyleSheet("background-color:white")
    # l2 = CtrlBar(parent=w)
    # l3 = CtrlBottom(100, None, parent=w)
    # trivial = CodeBlock("hi", l3, parent=w)
    # trivial2 = CodeBlock("hi again", trivial, parent=w)
    # label = ControlBlockTop("if song == Never Gonna Give You Up:", trivial2, l2, l3, parent=w)
    # trivial = CodeBlock("hi", None, parent=w)
    # trivial1 = CodeBlock("hi", trivial, parent=w)
    # trivial2 = CodeBlock("hi", trivial1, parent=w)
    # trivial3 = CodeBlock("hi", trivial2, parent=w)
    # b1 = CodeBlock("test", parent=w)
    # b5 = CodeBlock("test2", parent=w)
    # b4 = CodeBlock("test3", parent=w)
    # b3 = CodeBlock("test4", parent=w)
    # b2 = CodeBlock("test5", parent=w)
    # # trivial4 = HatBlock("hi", trivial3, parent=w)
    # b6 = CapBlock("test6", parent=w)
    # # # b2.move(0,45)

    # b1.attach_child(b2)
    # b2.attach_child(b3)
    # b3.attach_child(b4)
    # b4.attach_child(b5)

    b6 = CapBlock("fewa", parent=w)
    b9 = CodeBlock("teeeeest", parent=w)
    b10 = CodeBlock("another tessst", parent=w)
    c1 = CtrlTop("tests", parent=w)
    c2 = CtrlBottom("tetss", parent=w)
    c3 = CtrlBar(parent=w)

    b6.attach_child(c1)
    c1.attach_child(b9)
    b9.attach_child(b10)
    b10.attach_child(c2)
    c3.attach_top(c1)
    c3.attach_bottom(c2)

    b6.move_recurse(20,20)
    # b1.move(20, 20)
    test = []
    #b6.raiseEvent()
    #for j in range(len(test)):
    #    test[j].attach_child(test[j-1])
    w.show()
    w.raise_()

    app.exec_()
