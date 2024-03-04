from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtGui
from src.UIWindow import Authos
class Authors(QMainWindow, Authos.Ui_Form):
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
        self.setWindowIcon(QtGui.QIcon('data/bot.png'))
        self.back_button.clicked.connect(self.back)

    def back(self):
        self.obj.show()
        self.hide()