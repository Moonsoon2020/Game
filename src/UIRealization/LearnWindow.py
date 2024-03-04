from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from ContolBD import ControlDataBase
from UIWindow import Learn
class Learn(QMainWindow, Learn.Ui_Form):
    def __init__(self, obj):
        self.status = 1
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet("""QMainWindow {
                   background-image: url("data/fon.jpg");
                   background-repeat: no-repeat;
                   background-position: center;
               }""")
        self.initUI()
        self.obj = obj

    def initUI(self):
        self.back_button.clicked.connect(self.back)
        self.next_btn.clicked.connect(self.next)
        self.setWindowIcon(QtGui.QIcon('data/bot.png'))

    def back(self):
        self.status-=1
        self.update()


    def next(self):
        self.status+=1
        self.update()

    def update(self):
        _translate = QtCore.QCoreApplication.translate
        if self.status == 0 or self.status == 5:
            self.obj.show()
            self.hide()
        elif self.status == 1:
            self.label.setText(_translate("Form",
                                          "<html><head/><body><p align=\"center\">Добро пожаловать в игру</p><p align=\"center\">Flight Of The Clones</p></body></html>"))
            self.label_2.setText(_translate("Form",
                                            "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Здесь вам предстоит отстроить собственную базу,</span></p><p align=\"center\"><span style=\" font-weight:600;\">защищищая ее от врагов. </span></p><p align=\"center\"><span style=\" font-weight:600;\">Давайте пройдемся по основам игры...</span></p></body></html>"))
        elif self.status == 2:
            self.label.setText("")
            self.label_2.setText(_translate("Form",
                                            "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">В игре есть ядро, которое нужно защищать от атак.</span></p><p align=\"center\"><span style=\" font-weight:600;\">Сам персонаж стрелять не может, </span></p><p align=\"center\"><span style=\" font-weight:600;\">но когда-нибудь он научится...</span></p></body></html>"))
        elif self.status == 3:
            self.label.setText("")
            self.label_2.setText(_translate("Form",
                                            "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">В игре есть ресурсы, которые добываются буром.</span></p><p align=\"center\"><span style=\" font-weight:600;\">С помощью сини стенок можно огородить своё ядро.</span></p><p align=\"center\"><span style=\" font-weight:600;\">Стенки не бесконечны! </span></p><p align=\"center\"><span style=\" font-weight:600;\">Поэтому Вам предстоит правильно распределить </span></p><p align=\"center\"><span style=\" font-weight:600;\">как начальные ресурсы, так и последующие...</span></p></body></html>"))
        elif self.status == 4:
            self.label.setText("")
            self.label_2.setText(_translate("Form",
                                            "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">Отстраивайте свою базу, изучайте новые локации!</span></p><p align=\"center\"><span style=\" font-weight:600;\"><br/></span></p><p align=\"center\"><span style=\" font-weight:600;\">И просто наслаждайтесь игрой!</span></p></body></html>"))
