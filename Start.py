import random
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow
import Authos
import Learning
import List_Best
import New_world
import Start_window
import Old_world
import end
from ContolBD import ControlDataBase
from game import Game
import pympler


names = ['Лихая туча', 'Отметина ночи', 'Грот страха', 'Рой FOGLOFF', 'Континент moon', 'Народ чудес', 'Кратер ужаса',
         'Багряный дракон', 'Карцер небес', 'Печальный серет', 'Месть FOGLOFF', 'Остров солнца', 'Фронт луны']


class StartW(QMainWindow, Start_window.Ui_Flight_Of_The_Clones):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet("""QMainWindow {
        background-image: url("01012.jpg");
        background-repeat: no-repeat;
        background-position: center;
    }""")
        self.initUI()

    def initUI(self):
        self.Btn_play.clicked.connect(self.open_game)
        self.Button_best.clicked.connect(self.open_list_best)
        self.Authors.clicked.connect(self.open_authors)
        self.dowloand_button.clicked.connect(self.open_download)
        self.learn_btn.clicked.connect(self.open_learn)

    def open_game(self):
        self.n_world = New_world_window()
        self.hide()
        self.n_world.show()

    def open_list_best(self):
        self.list_best = ListBest()
        self.hide()
        self.list_best.show()

    def open_authors(self):
        self.authors = Authors()
        self.hide()
        self.authors.show()

    def open_download(self):
        self.load = Old_world_w()
        self.hide()
        self.load.show()

    def open_learn(self):
        self.load = Learn()
        self.hide()
        self.load.show()


class ListBest(QMainWindow, List_Best.Ui_List_Best):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet("""QMainWindow {
                background-image: url("01012.jpg");
                background-repeat: no-repeat;
                background-position: center;
            }""")
        self.initUI()

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
        self.main = StartW()
        self.main.show()
        self.hide()


class Authors(QMainWindow, Authos.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet("""QMainWindow {
                        background-image: url("01012.jpg");
                        background-repeat: no-repeat;
                        background-position: center;
                    }""")
        self.initUI()

    def initUI(self):
        self.back_button.clicked.connect(self.back)

    def back(self):
        self.main = StartW()
        self.main.show()
        self.hide()


class End(QMainWindow, end.Ui_MainWindow):
    def __init__(self, time, key):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet("""QMainWindow {
                        background-image: url("01012.jpg");
                        background-repeat: no-repeat;
                        background-position: center;
                    }""")
        self.initUI()
        self.label_info.setText(f'Общее время игры: {time//60} минут, {time%60}секунд. Уровень: {time//30 + 1}\n'
                                f'Ключ генерации на котором вы  играли: {key}')
        self.time = time
        self.key = key

    def initUI(self):
        self.pushButton.clicked.connect(self.zap)

    def zap(self):
        control = ControlDataBase()
        control.add_record(self.textEdit_name.toPlainText() if self.textEdit_name.toPlainText() != '' else 'player',
                           self.time, self.key)
        self.my = StartW()
        self.my.show()
        self.hide()


class New_world_window(QMainWindow, New_world.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet("""QMainWindow {
                background-image: url("01012.jpg");
                background-repeat: no-repeat;
                background-position: center;
            }""")
        self.initUI()

    def initUI(self):
        self.back_button.clicked.connect(self.back)
        self.create_btn.clicked.connect(self.generate)
        self.accidentally_name_btn.clicked.connect(self.accidentally_name_rev)
        self.accidentally_key_btn.clicked.connect(self.accidentally_key_rev)
        self.accidentally_key_rev()
        self.accidentally_name_rev()

    def accidentally_key_rev(self):
        self.textEdit_2.setText(str(random.randint(0, 100000000)))

    def accidentally_name_rev(self):
        self.name_label.setText(names[random.randint(0, len(names)) - 1])

    def generate(self):
        name = self.name_label.toPlainText()
        key = self.textEdit_2.toPlainText()
        control = ControlDataBase()
        if name == '' or control.is_name_world(name):
            self.label_error.setText('Название мира введено неправильно')
            return
        if key == '' or len([i for i in key if i in '0123456789']) != len(key):
            self.label_error.setText('Ключ введен неправильно')
            return
        size = 1
        if self.radioButton_average.isChecked():
            size = 2
        elif self.radioButton_big.isChecked():
            size = 3
        self.hide()
        newrandov = random.randint(0, 10000000)
        game = Game(True, name, key, size)
        info = game.play()
        random.seed(newrandov)
        if len(info) == 0:
            self.my = StartW()
        else:
            self.my = End(info[0], info[1])
        self.my.show()

    def back(self):
        self.main = StartW()
        self.main.show()
        self.hide()


class Old_world_w(QMainWindow, Old_world.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet("""QMainWindow {
                background-image: url("01012.jpg");
                background-repeat: no-repeat;
                background-position: center;
            }""")
        self.initUI()

    def initUI(self):
        self.pushnaz.clicked.connect(self.past)
        self.pushvper.clicked.connect(self.next)
        self.back_button.clicked.connect(self.back)
        self.station = 0
        control = ControlDataBase()
        self.data = control.get_worlds()
        self.push_start = []
        self.label_info = []
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
            self.my = StartW()
        else:
            self.my = End(info[0], info[1])
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
                self.push_start[(i - self.station)].setGeometry(QtCore.QRect(840, 120 + (i - self.station) * 50, 110, 50))
                self.push_start[(i - self.station)].setStyleSheet("font: 16pt \"Berlin Sans FB\"; color: rgb(175,238,"
                                                                  "238);\n "
                                                                  "background-color: rgb(204, 204, 204, 0);")
                self.push_start[(i - self.station)].info = f"open_{i}"
                self.label_info[(i - self.station)].setGeometry(QtCore.QRect(120, 120 + (i - self.station) * 50, 720, 50))
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
        self.main = StartW()
        self.main.show()
        self.hide()


class Learn(QMainWindow, Learning.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet("""QMainWindow {
                   background-image: url("01012.jpg");
                   background-repeat: no-repeat;
                   background-position: center;
               }""")
        self.initUI()

    def initUI(self):
        self.back_button.clicked.connect(self.back)

    def back(self):
        self.main = StartW()
        self.main.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartW()
    ex.show()
    sys.exit(app.exec_())
