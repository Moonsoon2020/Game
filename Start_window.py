import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Start_window.ui', self)
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

    def open_game(self):  ################ я не знаю как открыть игру
        self.n_world = New_world()
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


class ListBest(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('List_Best.ui', self)
        self.initUI()

    def initUI(self):
        self.back_button.clicked.connect(self.back)
        # conn = sqlite3.connect('какая-то дб ')
        # self.textBrowser_best_pl.setFont(QFont('Arial', 24))
        # cursor = conn.cursor()
        # result = cursor.execute("""SELECT * FROM best_list""").fetchall()
        # for title, res, obj in sorted(result, key=lambda x: x[1], reverse=True):
        #     self.textBrowser_best_pl.append(str(title) + '\t' + str(res) + '\t' + str(obj))

        # conn.close()

    def back(self):
        self.main = MyWidget()
        self.main.show()
        self.hide()


class Authors(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Authos.ui', self)
        self.initUI()

    def initUI(self):
        self.back_button_1.clicked.connect(self.back1)

    def back1(self):
        self.main = MyWidget()
        self.main.show()
        self.hide()


class New_world(QMainWindow): ##########сделать кнопку назад
    def __init__(self):
        super().__init__()
        uic.loadUi('New_world.ui', self)
        self.setStyleSheet("""QMainWindow {
                background-image: url("01012.jpg");
                background-repeat: no-repeat;
                background-position: center;
            }""")
        self.initUI()

    def initUI(self):
        pass
        #self.back_button_1.clicked.connect(self.back1)

    def back1(self):
        self.main = MyWidget()
        self.main.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
