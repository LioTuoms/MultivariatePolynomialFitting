# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preferencesDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(378, 174)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 120, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.labelName = QtWidgets.QLabel(Dialog)
        self.labelName.setGeometry(QtCore.QRect(70, 60, 54, 12))
        self.labelName.setObjectName("labelName")
        self.textLowPower = QtWidgets.QTextEdit(Dialog)
        self.textLowPower.setGeometry(QtCore.QRect(123, 55, 71, 21))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(11)
        self.textLowPower.setFont(font)
        self.textLowPower.setTabStopWidth(81)
        self.textLowPower.setObjectName("textLowPower")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(202, 60, 54, 12))
        self.label.setObjectName("label")
        self.textHighPower = QtWidgets.QTextEdit(Dialog)
        self.textHighPower.setGeometry(QtCore.QRect(250, 55, 61, 21))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(11)
        self.textHighPower.setFont(font)
        self.textHighPower.setObjectName("textHighPower")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labelName.setText(_translate("Dialog", "次方范围："))
        self.textLowPower.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'新宋体\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\'; font-size:9pt;\">-1</span></p></body></html>"))
        self.label.setText(_translate("Dialog", "-------"))
        self.textHighPower.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'新宋体\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'SimSun\'; font-size:9pt;\">3</span></p></body></html>"))

