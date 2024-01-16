import random
import sys

import win32gui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication
from Summoner import SummonerUIRect

s = SummonerUIRect()
app = QApplication(sys.argv)

w = s.bind_ui(2)
w.show()


app.exec_()  # 开始
