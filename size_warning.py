# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QApplication, QDialogButtonBox

class SizeWarning(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("Size Warning")
        self.resize(400, 287)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.No|QDialogButtonBox.Yes)
        self.buttonBox.setCenterButtons(True)
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
        self.verticalLayout.addWidget(self.buttonBox)

        QMetaObject.connectSlotsByName(self)

        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Size Warning", "Size Warning"))
        self.label.setText(_translate("self", "<html><head/><body><p align=\"center\"><img src=\":/icons/dialog-warning.svg\"/></p></body></html>"))
        self.label_2.setText(_translate("self", "<html><head/><body><p align=\"center\">Warning</p><p align=\"center\"><span style=\" font-size:9pt;\">The file you are attempting to open is very large (2000+ lines). Codeblock Visual Studio may freeze or lag. Are you sure you want to continue?</span></p>"))

import icons.icons_rc

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    self = QDialog()
    ui = SizeWarning()
    ui.show()
    sys.exit(app.exec_())

