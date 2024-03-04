from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from ContolBD import ControlDataBase
from UIWindow import New_world
import random
from UIRealization.EndWindow import End
from game import Game


class New_world_window(QMainWindow, New_world.Ui_Form):
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
        self.back_button.clicked.connect(self.back)
        self.create_btn.clicked.connect(self.generate)
        self.accidentally_name_btn.clicked.connect(self.accidentally_name_rev)
        self.accidentally_key_btn.clicked.connect(self.accidentally_key_rev)
        self.accidentally_key_rev()
        self.accidentally_name_rev()
        self.setWindowIcon(QtGui.QIcon('data/bot.png'))

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
            self.my = self.obj
        else:
            self.my = End(info[0], info[1], self.obj)
        self.my.show()

    def back(self):
        self.obj.show()
        self.hide()