# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QApplication, QDialogButtonBox

class SourceCodeWarning(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("Size Warning")
        self.resize(400, 250)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QLabel(self)
        font = QFont()
        font.setFamily("Ubuntu")
        self.label_2.setFont(font)
        self.label_2.setTextFormat(Qt.RichText)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        QMetaObject.connectSlotsByName(self)

        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Source Code Not Available", "Source Code Not Available"))
        self.label.setText(_translate("self", "<html><head/><body><p align=\"center\"><img src=\":/icons/dialog-warning.svg\"/></p></body></html>"))
        self.label_2.setText(_translate("self", "<html><head/><body><p align=\"center\" style=\"font-size:16pt;\">Error</p><p align=\"center\"><span style=\" font-size:9pt;\">The source code for this file is not available.</span></p>"))

import icons.icons_rc

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    self = QDialog()
    ui = SourceCodeWarning()
    ui.show()
    sys.exit(app.exec_())

