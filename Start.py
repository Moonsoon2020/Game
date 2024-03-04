import sys

from PyQt5.QtWidgets import QApplication

from src.UIRealization.StartWindows import StartW

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartW()
    ex.show()
    sys.exit(app.exec_())
