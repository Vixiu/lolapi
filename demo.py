
import qdarktheme
from PyQt5 import QtWidgets, uic
import sys

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUiType

main_ui, _ = loadUiType('lolapi.ui')


class MainGui(QMainWindow, main_ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)  # 构造界面
    #  self.resize(1500, 1100)


def test1():
    global window
    window = MainGui()
    window.show()
    window.help.clicked.connect(test1)
    print(1)


app = QtWidgets.QApplication(sys.argv)

app.setStyleSheet(qdarktheme.load_stylesheet("light"))
window = MainGui()
window.show()
window.help.clicked.connect(test1)
sys.exit(app.exec_())
