# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QApplication

class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("About")
        self.resize(400, 287)
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
        self.setWindowTitle(_translate("About", "About"))
        self.label.setText(_translate("self", "<html><head/><body><p align=\"center\"><img src=\":/icons/codeblock-icon.png\"/></p></body></html>"))
        self.label_2.setText(_translate("self", "<html><head/><body><p align=\"center\">Codeblock Visual Studio v0.6.3</p><p align=\"center\"><span style=\" font-size:9pt;\">This program breaks down source files into colorful and visually descriptive chains of blocks. It includes various debugging and coding tools, such as the CodeBlock tool.</span></p><p align=\"center\"><span style=\" font-size:9pt;\">Codeblock Visual Studio is licensed under the LGPL license.</span></p><p align=\"center\"><span style=\" font-size:9pt;\">Copyright (C) Tremolo Tech, LLC 2018.</span></p></body></html>"))

import icons.icons_rc

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    self = QDialog()
    ui = AboutDialog()
    ui.show()
    sys.exit(app.exec_())

