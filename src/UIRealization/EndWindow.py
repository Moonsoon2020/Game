from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from ContolBD import ControlDataBase
from UIWindow import end
class End(QMainWindow, end.Ui_MainWindow):
    def __init__(self, time, key, obj):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet("""QMainWindow {
                        background-image: url("data/fon.jpg");
                        background-repeat: no-repeat;
                        background-position: center;
                    }""")
        self.initUI()
        self.label_info.setText(f'Общее время игры: {time // 60} минут, {time % 60}секунд. Уровень: {time // 30 + 1}\n'
                                f'Ключ генерации, на котором вы  играли: {key}')
        self.time = time
        self.key = key
        self.obj = obj

    def initUI(self):
        self.pushButton.clicked.connect(self.zap)

    def zap(self):
        control = ControlDataBase()
        control.add_record(self.textEdit_name.toPlainText() if self.textEdit_name.toPlainText() != '' else 'player',
                           self.time, self.key)
        self.obj.show()
        self.hide()