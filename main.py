import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

from eng import assistant

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        loadUi("resources/main.ui", self)
        self.setWindowTitle('voice assistant')
        self.setGeometry(380, 200, 490, 410)
        but = QPushButton(self)
        but.setIcon(QIcon('resources/but.png'))
        but.setIconSize(QSize(100, 100))
        but.setGeometry(200, 170, 100, 100)
        but.clicked.connect(assistant)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
