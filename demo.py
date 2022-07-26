import sys
import time
# int(time.time() / 600000)
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

import Fuwen
from Lcu import LcuRequest, CheckProc
from lol_find import FindLolQP
lolpath = 'F:\\英雄联盟-\\LeagueClient'
lolpath = 'F:\\1\\英雄联盟-\\LeagueClient'
lcu = LcuRequest(lolpath)
print(CheckProc('League of Legends.exe'))
print(lcu.getdata("/lol-champ-select/v1/session/actions/1").json())
