import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

import Fuwen

app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Fuwen.Ui_FuWen()
ui.setupUi(MainWindow)
MainWindow.show()
app.exec_()  # 开始

