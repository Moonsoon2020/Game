from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from ContolBD import ControlDataBase
from UIWindow import List_Best


class ListBest(QMainWindow, List_Best.Ui_List_Best):
    def __init__(self, obj):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet("""QMainWindow {
                background-image: url("data/fon.jpg");
                background-repeat: no-repeat;
                background-position: center;
            }""")
        self.initUI()
        self.obj=obj

    def initUI(self):
        self.back_button.clicked.connect(self.back)
        self.control = ControlDataBase()
        self.data = list(sorted(self.control.get_record(), key=lambda x: x[1], reverse=True))
        print(self.data)
        self.pushnaz.clicked.connect(self.past)
        self.pushvper.clicked.connect(self.next)
        self.station = 0
        self.push_start = []
        self.label_info = []
        self.setWindowIcon(QtGui.QIcon('data/bot.png'))
        for i in range(0, 5):
            self.label_info.append(QtWidgets.QLabel(self))
            # self.push_start[-1].close()
        self.repaint()
        self.remove()

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
            if i >= len(self.data):
                self.label_info[(i - self.station)].hide()
            else:
                self.label_info[(i - self.station)].show()
                self.label_info[(i - self.station)].setGeometry(
                    QtCore.QRect(120, 120 + (i - self.station) * 50, 720, 50))
                self.label_info[(i - self.station)].setText(f"{i + 1}. Игрок \""
                                                            f"{self.data[i][0] if len(self.data[i][0]) < 10 else str(self.data[i][0][:8]) + ' ...'}\"."
                                                            f"Уровень {self.data[i][1] // 30 + 1}. Ключ генерации {self.data[i][2]}")
                self.label_info[(i - self.station)].setObjectName("label_info")
                self.label_info[(i - self.station)].setStyleSheet("font: 16pt \"Berlin Sans FB\"; color: "
                                                                  "rgb(175,238,238);\n"
                                                                  "background-color: rgb(204, 204, 204, 0);")
        self.repaint()

    def back(self):
        self.obj.show()
        self.hide()