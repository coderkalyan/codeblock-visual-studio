#!/usr/bin/python3
import random

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QRect, QPoint, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QFont, QColor, QImage, QFontMetrics
from PyQt5.QtSvg import QSvgWidget
import time


class BasicBlock(QWidget):
    def __init__(self, content='print("Hello, World")', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.content = content
        self.child = None
        self.parent = None
        self.text_size = 50
        self.dragging = -10
        self.width = 100
        self.height = 100
        self.color = random.choice(["red", "orange", "yellow", "green", "blue"])

        temp = self.geometry()
        self.setGeometry(temp.x(), temp.y(), temp.x() + self.width, temp.y() + self.height)

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
        self.setGeometry(geom.x() + delta_x, geom.y() + delta_y, geom.width() + delta_x, geom.height() + delta_y)
        return geom.x() + delta_x, geom.y() + delta_y

    def move_to(self, x, y):
        """
        Moves the current block to a position
        :param x: x position to move to
        :param y: y position to move to
        """

        geom = self.geometry()
        self.setGeometry(x, y, self.width + x, y + self.height)

    def attach_child(self, child):
        self.child = child
        self.child.parent = self
        temp = self.child.geometry()
        cur = self.geometry()
        print(self.height)
        self.child.setGeometry(cur.x(), cur.y() + self.height, cur.x() + temp.width(),
                               cur.y() + self.height + temp.height())
        # self.child.setParent(self)

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
        print(self.drag_geom)

    def move_recurse(self, x, y):
        self.move_to(x, y)
        if self.child is not None:
            self.child.move_recurse(x, y + self.height)

    def mouseMoveEvent(self, event):
        if self.dragging == -10:
            return

        pos = self.mapToGlobal(event.pos() - self.dragging)
        deltax = abs(self.geometry().x() - self.drag_geom.x())
        deltay = abs(self.geometry().y() - self.drag_geom.y())
        print(deltax, deltay)
        if deltax > 10 or deltay > 10:
            self.detach_parent()
        posx = pos.x()
        posy = pos.y()
        cur = self
        self.move_recurse(self.drag_geom.x() + posx, self.drag_geom.y() + posy)

    def mouseReleaseEvent(self, event):
        self.dragging = -10


class CodeBlock(BasicBlock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.color = "blue"
        font = QFont("Comic Sans MS", 15)
        metric = QFontMetrics(font)
        self.width = QFontMetrics.width(metric, self.content) + 30
        self.height = metric.height() + 15
        self.text_size = 50

        temp = self.geometry()
        self.setGeometry(temp.x(), temp.y(), temp.x() + self.width, temp.y() + self.height)

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor(self.color))
        painter.setBrush(QColor(self.color))
        painter.setFont(QFont("Comic Sans MS", 15))
        painter.setRenderHint(QPainter.Antialiasing)

        geom = self.geometry()
        painter.drawRect(QRect(0, 0, geom.width() - geom.x(), geom.height() - geom.y()))
        #painter.setPen(QColor("red"))
        #painter.setBrush(QColor("red"))
        #self.content = 'print("Hello, World!")'
        #painter.drawText(0, 30, self.content)
        painter.setBrush(QColor("white"))
        painter.setPen(QColor("white"))
        painter.drawText(10, 25, self.content)
        painter.end()


class AbstractDraggableBlock(QWidget):
    """
    A QWidget subclass that can be dragged around within its parent widget.
    Note: Not intended to work if the parent widget has a layout
    """

    def __init__(self, attached, *args, **kwargs):
        self.offset_attached = kwargs.pop('offset', 0)
        super().__init__(*args, **kwargs)
        self._dragging = False
        self.offset = QSize(
            self.geometry().width() / 2,
            self.geometry().height() / 2)
        self.attached = attached
        if type(self.attached) == CtrlBottom:
            self.offset_attached = -20
            print(type(self.attached), "attached")
        else:
            print(type(self.attached), "attached not")
        print(self.offset_attached, type(self.attached) == CtrlBottom)
        self.siblingcoords = {}
        # TODO: Find a way to only calculate this once instead of for every
        # instance for performance reasons
        self.siblings = kwargs['parent'].findChildren(AbstractDraggableBlock)
        for sibling in self.siblings:
            self.siblingcoords[sibling] = QPoint(
                sibling.geometry().x(), sibling.geometry().y())
        if self.attached is not None:
            # TODO: optimizations on iterating - possibly get the length of the
            # chain?
            for i in range(199):
                self.attached.bourgeois = self
                new_geometry_attached = QRect(
                    self.geometry().x(),
                    self.geometry().y() + self.geometry().height() - 17,
                    self.attached.geometry().width(),
                    self.attached.geometry().height())
                self.attached.setGeometry(new_geometry_attached)
                self.attached.moveChild()

    def mousePressEvent(self, event):
        self._dragging = True
        self.raiseEvent()
        try:
            self.bourgeois.attached = None
        except AttributeError:
            pass
        for i in self.siblings:
            i.moving = self

    def mouseReleaseEvent(self, event):
        self._dragging = False

        new_pos_global = event.globalPos()
        globalMap = self.parent().mapFromGlobal(new_pos_global)
        new_pos_within_parent = QPoint(
            globalMap.x() - self.offset.width(),
            globalMap.y() - self.offset.height())
        new_geometry = QRect(new_pos_within_parent, self.geometry().size())
        print(self.attached, "RELEASE")
        self.setGeometry(new_geometry)
        if self.attached is not None:
            for i in range(299):
                new_geometry_attached = QRect(
                    self.geometry().x() + self.offset_attached,
                    self.geometry().y() + self.geometry().height() - 17,
                    self.attached.geometry().width(),
                    self.attached.geometry().height())
                self.attached.setGeometry(new_geometry_attached)
                self.attached.moveChild()

    def mouseMoveEvent(self, event):
        if not self._dragging:
            return

        new_pos_global = event.globalPos()
        globalMap = self.parent().mapFromGlobal(new_pos_global)
        new_pos_within_parent = QPoint(
            globalMap.x() - self.offset.width(),
            globalMap.y() - self.offset.height())
        new_geometry = QRect(new_pos_within_parent, self.geometry().size())
        print(self.attached)
        self.setGeometry(new_geometry)
        if self.attached is not None:
            for i in range(5):
                new_geometry_attached = QRect(
                    self.geometry().x() + self.offset_attached,
                    self.geometry().y() + self.geometry().height() - 17,
                    self.attached.geometry().width(),
                    self.attached.geometry().height())
                print(self.attached.geometry(), "noo")
                self.attached.setGeometry(new_geometry_attached)
                self.attached.moveChild()

    def moveChild(self):
        if self.attached is not None:
            new_geometry_attached = QRect(
                self.geometry().x() + self.offset_attached,
                self.geometry().y() + self.geometry().height() - 17,
                self.attached.geometry().width(),
                self.attached.geometry().height())
            self.attached.a.moveChild()
            self.attached.setGeometry(new_geometry_attached)
        # temp = self.attached
        # while temp is not None:
        #     new_geometry_attached = QRect(
        #         temp.geometry().x()+self.offset_attached,
        #         temp.geometry().y()+self.geometry().height() - 17,
        #         self.attached.geometry().width(),
        #         self.attached.geometry().height())
        #     temp.setGeometry(new_geometry_attached)
        #     print(temp, temp.attached)
        #     temp = temp.attached

    def raiseEvent(self):
        self.raise_()
        if self.attached is not None:
            self.attached.raiseEvent()
            self.raise_()


class ControlBlockTop(AbstractDraggableBlock):
    """
    The top of the ControlBlock flow indicator
    """

    def __init__(self, text, attached, bar, bottom, parent, *args, **kwargs):
        super().__init__(attached, offset=20, parent=parent, *args, **kwargs)
        self.text = text
        self.scale = 1
        self.setGeometry(0, 0, 200 * self.scale, 60 * self.scale)
        self.bar = bar
        self.bottom = bottom

        print("resize")
        self.bar.setGeometry(self.geometry().x(),
                             self.geometry().y(),
                             self.bar.geometry().width(),
                             self.bottom.geometry().y() - self.geometry().y())
        if self.attached is not None:
            new_geometry_attached = QRect(
                self.geometry().x() + 20,
                self.geometry().y() + self.geometry().height() - 17,
                self.attached.geometry().width(),
                self.attached.geometry().height())
            print(self.geometry(), "NOOTO")
            self.attached.setGeometry(new_geometry_attached)

    def mouseMoveEvent(self, event):
        if not self._dragging:
            return

        new_pos_global = event.globalPos()
        globalMap = self.parent().mapFromGlobal(new_pos_global)
        new_pos_within_parent = QPoint(
            globalMap.x() - self.offset.width(),
            globalMap.y() - self.offset.height())
        new_geometry = QRect(new_pos_within_parent, self.geometry().size())
        print(self.attached)
        self.setGeometry(new_geometry)
        if self.attached is not None:
            for i in range(5):
                new_geometry_attached = QRect(
                    self.geometry().x() + self.offset_attached,
                    self.geometry().y() + self.geometry().height() - 17,
                    self.attached.geometry().width(),
                    self.attached.geometry().height())
                print(self.attached.geometry(), "noo")
                self.attached.setGeometry(new_geometry_attached)
                self.attached.moveChild()
        self.bar.setGeometry(self.geometry().x(),
                             self.geometry().y(),
                             self.geometry().x() + 20,
                             self.bottom.geometry().y() - self.geometry().y())
        print(self.bar.geometry(), "barGeometry")

    def paintEvent(self, QPaintEvent):
        print("paintevent")
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor("orange"))
        painter.setBrush(QColor("orange"))
        painter.setFont(QFont("Comic Sans MS", 15 * self.scale))

        textsize = painter.boundingRect(
            self.geometry(), 1, self.text + "       ")

        if textsize.width() > 100:
            rectwidth = textsize.width()
            self.setFixedWidth(textsize.width())
        else:
            rectwidth = 100

        print(rectwidth, "wid2")
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawRect(QRect(0, 0, rectwidth * self.scale, 45 * self.scale))
        # resize bottom block
        self.bottom.width = rectwidth
        self.bottom.resize(rectwidth, self.bottom.height())
        painter.drawChord(
            QRect(
                40 * self.scale,
                12 * self.scale,
                45 * self.scale,
                45 * self.scale),
            180 * 16,
            180 * 16)
        painter.setBrush(QColor("white"))
        painter.setPen(QColor("white"))
        painter.drawChord(QRect(20 * self.scale, -32 * self.scale,
                                45 * self.scale, 45 * self.scale), 180 * 16, 180 * 16)
        painter.drawText(
            20 * self.scale,
            (self.geometry().height() / 2) * self.scale,
            self.text)
        painter.end()


class CtrlBar(QWidget):
    """
    The bar to enclose the ControlBlock flow indicator on 3rd side.
    Will be used to show visually what blocks are in the flow loop.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.scale = 1
        self.setGeometry(10, 0, 20 * self.scale, 200 * self.scale)

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor("orange"))
        painter.setBrush(QColor("orange"))
        painter.drawRect(0, 0, 20, self.geometry().height())
        painter.end()


class CtrlBottom(AbstractDraggableBlock):
    """
    The bottom of a ControlBlock flow indicator,
    showing the end of the code block
    (equivalent to "end" statements in some languages)
    """

    def __init__(self, width, attached, parent, *args, **kwargs):
        super().__init__(attached, parent=parent, *args, **kwargs)
        self.scale = 1
        self.width = width
        self.setGeometry(0, 0, 200 * self.scale, 60 * self.scale)
        if self.attached is not None:
            new_geometry_attached = QRect(
                self.geometry().x(),
                self.geometry().y() + self.geometry().height() - 17,
                self.attached.geometry().width(),
                self.attached.geometry().height())
            print(self.geometry(), "NOOTO")
            self.attached.setGeometry(new_geometry_attached)

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor("orange"))
        painter.setBrush(QColor("orange"))
        painter.setFont(QFont("Comic Sans MS", 15 * self.scale))

        print(self.width, "selfidth")
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawRect(QRect(0, 0, self.width * self.scale, 45 * self.scale))
        painter.drawChord(
            QRect(
                20 * self.scale,
                12 * self.scale,
                45 * self.scale,
                45 * self.scale),
            180 * 16,
            180 * 16)
        painter.setBrush(QColor("white"))
        painter.setPen(QColor("white"))
        painter.drawChord(QRect(40 * self.scale, -32 * self.scale,
                                45 * self.scale, 45 * self.scale), 180 * 16, 180 * 16)
        painter.end()


class HatBlock(AbstractDraggableBlock):
    """
    A HatBlock, meant to represent things such as functions/methods
    """

    def __init__(self, text, attached, parent, *args, **kwargs):
        super().__init__(attached, parent=parent, *args, **kwargs)
        self.img = QImage("./blocks/hat.svg")
        self.img = self.img.smoothScaled(
            self.geometry().size().width(),
            self.geometry().size().height())
        self.text = text
        self.scale = 1
        self.setGeometry(0, 0, 200 * self.scale, 75 * self.scale)
        if self.attached is not None:
            new_geometry_attached = QRect(
                self.geometry().x(),
                self.geometry().y() + self.geometry().height() - 17,
                self.attached.geometry().width(),
                self.attached.geometry().height())
            self.attached.setGeometry(new_geometry_attached)

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor("dark green"))
        painter.setBrush(QColor("dark green"))
        painter.setFont(QFont("Comic Sans MS", 15 * self.scale))

        textsize = painter.boundingRect(
            self.geometry(), 1, "def" + self.text + "():")
        print(textsize)
        if textsize.width() > 200:
            rectwidth = textsize.width()
            self.setFixedWidth(textsize.width())
        else:
            rectwidth = 200

        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawChord(
            QRect(
                0,
                0,
                rectwidth *
                self.scale,
                60 *
                self.scale),
            0 *
            16,
            180 *
            16)
        painter.drawRect(
            QRect(
                0,
                30 *
                self.scale,
                rectwidth *
                self.scale,
                30 *
                self.scale))
        painter.drawChord(
            QRect(
                20 * self.scale,
                28 * self.scale,
                45 * self.scale,
                45 * self.scale),
            180 * 16,
            180 * 16)

        painter.setPen(QColor("white"))
        painter.drawText(
            20 * self.scale,
            (self.geometry().height() / 2 + 10) * self.scale,
            self.text)
        painter.end()


"""class CodeBlock(AbstractDraggableBlock):
"""
    #A puzzle-piece type CodeBlock meant to represent code in a program
"""

    def __init__(self, text, attached, parent, *args, **kwargs):
        super().__init__(attached, parent=parent, *args, **kwargs)
        self.text = text
        self.scale = 1
        self.setGeometry(0, 0, 200 * self.scale, 60 * self.scale)
        if self.attached is not None:
            new_geometry_attached = QRect(
                self.geometry().x(),
                self.geometry().y() + self.geometry().height() - 17,
                self.attached.geometry().width(),
                self.attached.geometry().height())
            print(self.geometry(), "NOOTO")
            self.attached.setGeometry(new_geometry_attached)

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor("#496BD3"))
        painter.setBrush(QColor("#4A6CD4"))
        painter.setFont(QFont("Comic Sans MS", 15 * self.scale))

        textsize = painter.boundingRect(
            self.geometry(), 1, self.text + "       ")

        if textsize.width() > 100:
            rectwidth = textsize.width()
            self.setFixedWidth(textsize.width())
        else:
            rectwidth = 100

        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawRect(QRect(0, 0, rectwidth * self.scale, 45 * self.scale))
        painter.drawChord(
            QRect(
                20 * self.scale,
                12 * self.scale,
                45 * self.scale,
                45 * self.scale),
            180 * 16,
            180 * 16)
        painter.setBrush(QColor("white"))
        painter.setPen(QColor("white"))
        painter.drawChord(QRect(20 * self.scale, -32 * self.scale,
                                45 * self.scale, 45 * self.scale), 180 * 16, 180 * 16)
        painter.drawText(
            20 * self.scale,
            (self.geometry().height() / 2) * self.scale,
            self.text)
        painter.end()
"""

if __name__ == "__main__":
    app = QApplication([])

    w = QWidget()
    w.setMinimumWidth(500)
    w.setMinimumHeight(500)
    # l2 = CtrlBar(parent=w)
    # l3 = CtrlBottom(100, None, parent=w)
    # trivial = CodeBlock("hi", l3, parent=w)
    # trivial2 = CodeBlock("hi again", trivial, parent=w)
    # label = ControlBlockTop("if song == Never Gonna Give You Up:", trivial2, l2, l3, parent=w)
    # trivial = CodeBlock("hi", None, parent=w)
    # trivial1 = CodeBlock("hi", trivial, parent=w)
    # trivial2 = CodeBlock("hi", trivial1, parent=w)
    # trivial3 = CodeBlock("hi", trivial2, parent=w)
    # trivial4 = HatBlock("hi", trivial3, parent=w)
    b1 = CodeBlock(parent=w)
    b2 = CodeBlock(parent=w)
    b3 = CodeBlock(parent=w)
    b4 = CodeBlock(parent=w)
    b5 = CodeBlock(parent=w)
    # b2.move(0,45)
    b1.attach_child(b2)
    b2.attach_child(b3)
    b3.attach_child(b4)
    b4.attach_child(b5)
    # b1.move(20, 20)

    w.show()
    w.raise_()

    app.exec_()
