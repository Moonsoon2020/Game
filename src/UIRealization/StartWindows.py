from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

from UIRealization.AuthorsWindows import Authors
from UIRealization.LIstBestWindows import ListBest
from UIRealization.LearnWindow import Learn
from UIRealization.NewWorldWindow import New_world_window
from UIRealization.OldWorldWindow import Old_world_w
from UIWindow import Start_window


class StartW(QMainWindow, Start_window.Ui_Flight_Of_The_Clones):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet("""QMainWindow {
        background-image: url("data/fon.jpg");
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
        self.setWindowIcon(QtGui.QIcon('data/bot.png'))

    def open_game(self):
        self.n_world = New_world_window(self)
        self.hide()
        self.n_world.show()

    def open_list_best(self):
        self.list_best = ListBest(self)
        self.hide()
        self.list_best.show()

    def open_authors(self):
        self.authors = Authors(self)
        self.hide()
        self.authors.show()

    def open_download(self):
        self.load = Old_world_w(self)
        self.hide()
        self.load.show()

    def open_learn(self):
        self.load = Learn(self)
        self.hide()
        self.load.show()