# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class HelpDialog(QtWidgets.QWizard):
    def __init__(self):
        super().__init__()
        self.setObjectName("Wizard")
        self.resize(400, 300)
        self.wizardPage1 = QtWidgets.QWizardPage()
        self.wizardPage1.setObjectName("wizardPage1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.wizardPage1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.wizardPage1)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.wizardPage1)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.wizardPage1)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.addPage(self.wizardPage1)
        self.wizardPage2 = QtWidgets.QWizardPage()
        self.wizardPage2.setObjectName("wizardPage2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.wizardPage2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.wizardPage2)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.wizardPage2)
        self.label_5.setScaledContents(False)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.addPage(self.wizardPage2)

        QtCore.QMetaObject.connectSlotsByName(self)

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Wizard", "Wizard"))
        self.label.setText(_translate("Wizard", "Welcome To"))
        self.label_2.setText(_translate("Wizard", "<html><head/><body><p align=\"center\"><img src=\":/icons/codeblock-icon.png\"/></p></body></html>"))
        self.label_3.setText(_translate("Wizard", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">Codeblock Visual Studio</span></p></body></html>"))
        self.label_4.setText(_translate("Wizard", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">Quick Start</span></p></body></html>"))
        self.label_5.setText(_translate("Wizard", "<html><head/><body><p>Use File &gt; Open to convert a Python Source file into Code Blocks. This can help with visualizing the flow of your code.</p></body></html>"))

import icons.icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = HelpDialog()
    ui.show()
    sys.exit(app.exec_())

