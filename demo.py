import sys
import time
#int(time.time() / 600000)
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

import Fuwen

app = QApplication(sys.argv)
MainWindow = QMainWindow()





fuwenmain = QDialog()
#fuwenmain = QWidget
uis = Fuwen.Ui_FuWen()
uis.setupUi(fuwenmain)
fuwenmain.show()
app.exec_()  # 开始
