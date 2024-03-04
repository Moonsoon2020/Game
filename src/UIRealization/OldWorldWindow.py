import random

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from ContolBD import ControlDataBase
from UIRealization.EndWindow import End
from UIWindow import Old_world
from game import Game


class Old_world_w(QMainWindow, Old_world.Ui_Form):
    def __init__(self, obj):
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
        self.pushnaz.clicked.connect(self.past)
        self.pushvper.clicked.connect(self.next)
        self.back_button.clicked.connect(self.back)
        self.station = 0
        control = ControlDataBase()
        self.data = control.get_worlds()
        self.push_start = []
        self.label_info = []
        self.setWindowIcon(QtGui.QIcon('data/bot.png'))
        for i in range(0, 5):
            self.push_start.append(QtWidgets.QPushButton(self))
            self.label_info.append(QtWidgets.QLabel(self))
            # self.push_start[-1].close()
        self.repaint()
        self.remove()

    def start(self):
        button = QApplication.instance().sender()
        dowland = self.data[int(button.info[5:])]
        newrandov = random.randint(0, 10000000)
        self.hide()
        game = Game(False, dowland[1])
        info = game.play()
        random.seed(newrandov)
        if len(info) == 0:
            self.my = self.obj
        else:
            self.my = End(info[0], info[1], self.obj)
        self.my.show()

    def past(self):
        if self.station - 5 >= 0:
            self.station -= 5
            self.remove()

    def next(self):
        if self.station + 5 <= len(self.data):
            self.station += 5
            self.remove()

    def remove(self):
        print(self.data)
        for i in range(self.station, self.station + 5):
            _translate = QtCore.QCoreApplication.translate
            if i >= len(self.data):
                self.push_start[(i - self.station)].hide()
                self.label_info[(i - self.station)].hide()
            else:
                self.push_start[(i - self.station)].show()
                self.label_info[(i - self.station)].show()
                self.push_start[(i - self.station)].clicked.connect(self.start)
                self.push_start[(i - self.station)].setGeometry(
                    QtCore.QRect(840, 120 + (i - self.station) * 50, 110, 50))
                self.push_start[(i - self.station)].setStyleSheet("font: 16pt \"Berlin Sans FB\"; color: rgb(175,238,"
                                                                  "238);\n "
                                                                  "background-color: rgb(204, 204, 204, 0);")
                self.push_start[(i - self.station)].info = f"open_{i}"
                self.label_info[(i - self.station)].setGeometry(
                    QtCore.QRect(120, 120 + (i - self.station) * 50, 720, 50))
                self.label_info[(i - self.station)].setText(f"Мир \"{self.data[i][1]}\". {self.data[i][2] // 60} минут "
                                                            f"{self.data[i][2] % 60} секунд. Уровень {self.data[i][2] // 30 + 1}. ")
                self.label_info[(i - self.station)].setObjectName("label_info")
                self.label_info[(i - self.station)].setStyleSheet("font: 16pt \"Berlin Sans FB\"; color: "
                                                                  "rgb(175,238,238);\n"
                                                                  "background-color: rgb(204, 204, 204, 0);")
                self.push_start[(i - self.station)].setText(_translate("Form", "Играть"))
                # self.push_start[-1].close()
        self.repaint()

    def back(self):
        self.obj.show()
        self.hide()