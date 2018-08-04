# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QSizePolicy, QTabWidget, QMenuBar, QStatusBar, QApplication, QTreeWidget, \
    QTreeWidgetItem, QVBoxLayout, QScrollArea, QFrame, QSplitter, QPushButton, QMenu, QAction, QDesktopWidget
from PyQt5.QtGui import QIcon, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(flags=QtCore.Qt.Window)
        self.setWindowIcon(QIcon(QPixmap(":/icon/codeblock_icon.svg")))
        scale_x = QDesktopWidget().screenGeometry().width()/1920
        scale_y = QDesktopWidget().screenGeometry().height()/1080
        self.resize(1280*scale_x, 720*scale_y)
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QSplitter(self.centralwidget)

        self.tabWidget = QTabWidget(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())

        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QWidget()
        self.tab.setObjectName("tab")

        self.verticalLayout2 = QVBoxLayout(self.tab)
        self.classView = QTreeWidget(self.tab)
        self.classView.header().setVisible(False)
        self.verticalLayout2.addWidget(self.classView)

        self.tabWidget.addTab(self.tab, "")

        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")

        self.tabWidget.addTab(self.tab_2, "")

        self.splitter.addWidget(self.tabWidget)

        self.tabWidget_2 = QTabWidget(self.centralwidget)
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget_2.addTab(self.tab_4, "")

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 184, 148))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(7)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())

        self.tabWidget_2.setSizePolicy(sizePolicy)
        self.tabWidget_2.setTabsClosable(False)
        self.tabWidget_2.setMovable(True)
        self.tabWidget_2.setObjectName("tabWidget_2")

        self.splitter.addWidget(self.tabWidget_2)

        self.horizontalLayout.addWidget(self.splitter)
        self.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuHelp = QMenu(self.menubar)

        self.actionOpen = QAction(self)
        self.actionOpen.setText("Open")

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.setTitle("File")
        self.menubar.addAction(self.actionOpen)

        self.actionAbout = QAction(self)
        self.actionAbout.setText("About Codeblock Visual Studio")

        self.actionTutorial = QAction(self)
        self.actionTutorial.setText("Rerun Tutorial")

        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionTutorial)
        self.menuHelp.setTitle("Help")
        self.menubar.addAction(self.menuHelp.menuAction())

        self.setMenuBar(self.menubar)

        self.statusbar = QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.frameLayout = QHBoxLayout(self.tab_3)
        self.scroll = QScrollArea()
        self.scrollContents = QWidget()
        self.scrollContents.setGeometry(QtCore.QRect(0, 0, 5000, 50000))
        self.scrollLayout = QHBoxLayout(self.scrollContents)

        self.codeArea = QFrame(self.scrollAreaWidgetContents)
        self.codeArea.setMinimumSize(QtCore.QSize(2000, 2000))
        self.scrollLayout.addWidget(self.codeArea)
        self.frameLayout.addWidget(self.scroll)
        self.scroll.setWidget(self.scrollContents)

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "Class View")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Tab 2")
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), "Code Area")
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), "Tab 2")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())

