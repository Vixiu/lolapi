import sys
import time

from PyQt5.QtWidgets import QApplication
from win32api import Sleep

import lolapiUI
from Summoner import SummonerUIRect
from RoundedWindow import RoundedWindow
from UI.se import Ui_form

app = QApplication(sys.argv)
summoner_rect = SummonerUIRect()
ui = summoner_rect.bind_ui(1)

ui.show()

summoner_rect.start()
print(time.ctime())
app.exec_()  # 开始
