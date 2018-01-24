from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QRect, QPoint, QSize
from PyQt5.QtSvg import QSvgWidget

class AbstractDraggableBlock(QSvgWidget):
    """
    A QLabel subclass that can be dragged around within its parent widget.
    Note: Not intended to work if the parent widget has a layout (e.g. QVBoxLayout).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dragging = False
        self.setGeometry(0, 0, self.geometry().size().width()*2, self.geometry().size().height()*2)
        self.offset = QSize(self.geometry().width()/2, self.geometry().height()/2)
        print(self.offset, self.geometry().size())

    def mousePressEvent(self, event):
        self._dragging = True

    def mouseReleaseEvent(self, event):
        self._dragging = False

    def mouseMoveEvent(self, event):
        if not self._dragging:
            return

        new_pos_global = event.globalPos()
        globalMap = self.parent().mapFromGlobal(new_pos_global)
        new_pos_within_parent = QPoint(globalMap.x()-self.offset.width(), globalMap.y()-self.offset.height())
        new_geometry = QRect(new_pos_within_parent, self.geometry().size())
        print(self.geometry())
        self.setGeometry(new_geometry)


class HatBlock(AbstractDraggableBlock):
    def __init__(self, parent, *args, **kwargs):
        super().__init__("./icons/hat.svg", parent=parent, *args, *kwargs)

if __name__ == "__main__":
    app = QApplication([])

    w = QWidget()
    label = AbstractDraggableBlock("./icons/hat.svg", draggable=True, parent=w)
    w.show()
    w.raise_()

    app.exec_( )