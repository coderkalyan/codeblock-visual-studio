# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QSizePolicy, QTabWidget, QMenuBar, QStatusBar, QApplication, QTreeWidget, \
    QTreeWidgetItem, QVBoxLayout, QScrollArea, QFrame, QSplitter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(flags=QtCore.Qt.Window)
        self.resize(1280, 720)
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QSplitter(self.centralwidget)

        self.tabWidget = QTabWidget(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())

        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QWidget()
        self.tab.setObjectName("tab")

        self.tabWidget.addTab(self.tab, "")

        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")

        self.tabWidget.addTab(self.tab_2, "")

        self.splitter.addWidget(self.tabWidget)

        self.tabWidget_3 = QTabWidget(self.centralwidget)
        self.tabWidget_3.setTabsClosable(False)
        self.tabWidget_3.setMovable(True)
        self.tabWidget_3.setObjectName("tabWidget_3")

        self.tab_5 = QWidget()
        self.tab_5.setObjectName("tab_5")

        self.tabWidget_3.addTab(self.tab_5, "")

        self.tab_6 = QWidget()
        self.tab_6.setObjectName("tab_6")

        self.tabWidget_3.addTab(self.tab_6, "")

        self.splitter.addWidget(self.tabWidget_3)

        self.tabWidget_2 = QTabWidget(self.centralwidget)

        self.verticalLayout = QVBoxLayout(self.tab_5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QScrollArea(self.tab_5)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 184, 148))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.treeWidget = QTreeWidget(self.tab_5)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QTreeWidgetItem(self.treeWidget)
        item_0.setText(0, "item0")
        item_1 = QTreeWidgetItem(self.treeWidget)
        item_1.setText(0, "item1")
        item_2 = QTreeWidgetItem(item_1)
        item_2.setText(0, "item2")
        self.treeWidget.header().setVisible(False)
        self.verticalLayout.addWidget(self.treeWidget)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())

        self.tabWidget_2.setSizePolicy(sizePolicy)
        self.tabWidget_2.setTabsClosable(False)
        self.tabWidget_2.setMovable(True)
        self.tabWidget_2.setObjectName("tabWidget_2")

        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget_2.addTab(self.tab_4, "")

        self.splitter.addWidget(self.tabWidget_2)

        self.horizontalLayout.addWidget(self.splitter)
        self.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 23))
        self.menubar.setObjectName("menubar")

        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.frameLayout = QHBoxLayout(self.tab_3)
        self.scroll = QScrollArea()
        self.scrollLayout = QHBoxLayout(self.scroll)

        self.codeArea = QFrame()
        self.codeArea.setMinimumHeight(20000)
        self.scrollLayout.addWidget(self.codeArea)
        self.frameLayout.addWidget(self.scroll)
        self.scroll.show()

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "Tab 1")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Tab 2")
        self.tabWidget_3.setTabText(self.tabWidget_2.indexOf(self.tab_3), "Code Area")
        self.tabWidget_3.setTabText(self.tabWidget_2.indexOf(self.tab_4), "Tab 2")
        self.tabWidget_2.setTabText(self.tabWidget_3.indexOf(self.tab_5), "Tab 1")
        self.tabWidget_2.setTabText(self.tabWidget_3.indexOf(self.tab_6), "Tab 2")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())

