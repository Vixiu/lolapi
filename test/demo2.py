import sys

from PyQt5.QtWidgets import QApplication

from GetSummonerMatch import SummonerUIRect

app = QApplication(sys.argv)

s = SummonerUIRect()
w = s.bind_ui(2)



app.exec_()  # 开始
