#!/usr/bin/python3
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtCore import QRect, QPoint, QSize, Qt
from PyQt5.QtGui import QPainter, QFont, QColor, QImage
from PyQt5.QtSvg import QSvgWidget
import time


class AbstractDraggableBlock(QWidget):
    """
    A QWidget subclass that can be dragged around within its parent widget.
    Note: Not intended to work if the parent widget has a layout (e.g. QVBoxLayout).
    """

    def __init__(self, attached, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dragging = False
        self.offset = QSize(self.geometry().width()/2, self.geometry().height()/2)
        self.attached = attached
        if self.attached is not None:
            self.attached.bourgeois = self
            new_geometry_attached = QRect(self.geometry().x(), self.geometry().y()+self.geometry().height()-17,
                                          self.attached.geometry().width(), self.attached.geometry().height())
            print(self.geometry(), "NOOO")
            self.attached.setGeometry(new_geometry_attached)
            self.attached.moveChild()


    def mousePressEvent(self, event):
        self._dragging = True
        self.raiseEvent()
        try:
            self.bourgeois.attached = None
        except AttributeError:
            pass

    def mouseReleaseEvent(self, event):
        self._dragging = False

        new_pos_global = event.globalPos()
        globalMap = self.parent().mapFromGlobal(new_pos_global)
        new_pos_within_parent = QPoint(globalMap.x() - self.offset.width(), globalMap.y() - self.offset.height())
        new_geometry = QRect(new_pos_within_parent, self.geometry().size())
        print(self.attached, "RELEASE")
        self.setGeometry(new_geometry)
        if self.attached is not None:
            for i in range(299):
                new_geometry_attached = QRect(self.geometry().x(), self.geometry().y() + self.geometry().height() - 17,
                                              self.attached.geometry().width(), self.attached.geometry().height())
                print(self.attached.geometry(), "noo")
                self.attached.setGeometry(new_geometry_attached)
                self.attached.moveChild()

    def mouseMoveEvent(self, event):
        if not self._dragging:
            return

        new_pos_global = event.globalPos()
        globalMap = self.parent().mapFromGlobal(new_pos_global)
        new_pos_within_parent = QPoint(globalMap.x()-self.offset.width(), globalMap.y()-self.offset.height())
        new_geometry = QRect(new_pos_within_parent, self.geometry().size())
        print(self.attached)
        self.setGeometry(new_geometry)
        if self.attached is not None:
            for i in range(5):
                new_geometry_attached = QRect(self.geometry().x(), self.geometry().y()+self.geometry().height()-17,
                                              self.attached.geometry().width(), self.attached.geometry().height())
                print(self.attached.geometry(), "noo")
                self.attached.setGeometry(new_geometry_attached)
                self.attached.moveChild()

    def moveChild(self):
        if self.attached is not None:
            new_geometry_attached = QRect(self.geometry().x(), self.geometry().y()+self.geometry().height()-17,
                                          self.attached.geometry().width(), self.attached.geometry().height())
            print(self.attached.geometry(), "noo")
            self.attached.moveChild()
            self.attached.setGeometry(new_geometry_attached)

    def raiseEvent(self):
        self.raise_()
        if self.attached is not None:
            self.attached.raiseEvent()
            self.raise_()


class HatBlock(AbstractDraggableBlock):
    def __init__(self, text, attached, parent, *args, **kwargs):
        super().__init__(attached, parent=parent, *args, **kwargs)
        self.img = QImage("./blocks/hat.svg")
        self.img = self.img.smoothScaled(self.geometry().size().width(), self.geometry().size().height())
        self.text = text
        self.scale = 1
        self.setGeometry(0, 0, 200 * self.scale, 75 * self.scale)
        if self.attached is not None:
            new_geometry_attached = QRect(self.geometry().x(), self.geometry().y()+self.geometry().height()-17,
                                          self.attached.geometry().width(), self.attached.geometry().height())
            print(self.geometry(), "NOOTO")
            self.attached.setGeometry(new_geometry_attached)

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor("dark green"))
        painter.setBrush(QColor("dark green"))
        painter.setFont(QFont("Comic Sans MS", 15*self.scale))

        textsize = painter.boundingRect(self.geometry(), 1, "def" + self.text + "():")
        print(textsize)
        if textsize.width() > 200:
            rectwidth = textsize.width()
            self.setFixedWidth(textsize.width())
        else:
            rectwidth = 200

        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawChord(QRect(0, 0, rectwidth*self.scale, 60*self.scale), 0*16, 180*16)
        painter.drawRect(QRect(0, 30*self.scale, rectwidth*self.scale, 30*self.scale))
        painter.drawChord(QRect(20*self.scale, 28*self.scale, 45*self.scale, 45*self.scale), 180*16, 180*16)

        painter.setPen(QColor("white"))
        painter.drawText(20*self.scale, (self.geometry().height()/2+10)*self.scale, self.text)
        painter.end()


class CodeBlock(AbstractDraggableBlock):
    def __init__(self, text, attached, parent, *args, **kwargs):
        super().__init__(attached, parent=parent, *args, **kwargs)
        self.text = text
        self.scale = 1
        self.setGeometry(0, 0, 200*self.scale, 60*self.scale)
        if self.attached is not None:
            new_geometry_attached = QRect(self.geometry().x(), self.geometry().y()+self.geometry().height()-17,
                                          self.attached.geometry().width(), self.attached.geometry().height())
            print(self.geometry(), "NOOTO")
            self.attached.setGeometry(new_geometry_attached)

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(QColor("red"))
        painter.setBrush(QColor("red"))
        painter.setFont(QFont("Comic Sans MS", 15*self.scale))

        textsize = painter.boundingRect(self.geometry(), 1, self.text + "       ")

        if textsize.width() > 100:
            rectwidth = textsize.width()
            self.setFixedWidth(textsize.width())
        else:
            rectwidth = 100

        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawRect(QRect(0, 0, rectwidth*self.scale, 45*self.scale))
        painter.drawChord(QRect(20*self.scale, 12*self.scale, 45*self.scale, 45*self.scale), 180*16, 180*16)
        painter.setBrush(QColor("white"))
        painter.setPen(QColor("white"))
        painter.drawChord(QRect(20*self.scale, -32*self.scale, 45*self.scale, 45*self.scale), 180*16, 180*16)
        painter.drawText(20*self.scale, (self.geometry().height()/2)*self.scale, self.text)
        painter.end()



if __name__ == "__main__":
    app = QApplication([])

    w = QWidget()
    label = HatBlock(parent=w)
    w.show()
    w.raise_()

    app.exec_( )
