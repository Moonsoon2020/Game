# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Learning.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1076, 650)
        self.back_button = QtWidgets.QPushButton(Form)
        self.back_button.setGeometry(QtCore.QRect(20, 580, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(22)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.back_button.setFont(font)
        self.back_button.setStyleSheet("font: 22pt \"Berlin Sans FB\"; color: rgb(175,238,238);\n"
"background-color: rgb(204, 204, 204, 0);")
        self.back_button.setObjectName("back_button")
        self.next_btn = QtWidgets.QPushButton(Form)
        self.next_btn.setGeometry(QtCore.QRect(880, 580, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Berlin Sans FB")
        font.setPointSize(22)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.next_btn.setFont(font)
        self.next_btn.setStyleSheet("font: 22pt \"Berlin Sans FB\"; color: rgb(175,238,238);\n"
"background-color: rgb(204, 204, 204, 0);")
        self.next_btn.setObjectName("next_btn")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(190, 20, 641, 121))
        self.label.setStyleSheet("font: 22pt \"Berlin Sans FB\"; color: rgb(175,238,238);\n"
"background-color: rgb(204, 204, 204, 0);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(0, 120, 1061, 451))
        self.label_2.setStyleSheet("font: 22pt \"Berlin Sans FB\"; color: rgb(175,238,238);\n"
"background-color: rgb(204, 204, 204, 0);")
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Обучение"))
        self.back_button.setText(_translate("Form", "Назад"))
        self.next_btn.setText(_translate("Form", "Далее"))
        self.label.setText(_translate("Form", "<html><head/><body><p align=\"center\">Добро пожаловать в игру</p><p align=\"center\">Flight Of The Clones</p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Здесь вам предстоит отстроить собственную базу,</span></p><p align=\"center\"><span style=\" font-weight:600;\">защищищая ее от врагов. </span></p><p align=\"center\"><span style=\" font-weight:600;\">Давайте пройдемся по основам игры...</span></p></body></html>"))
