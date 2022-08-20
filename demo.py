import sys
import time
# int(time.time() / 600000)
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

import Fuwen
from Lcu import LcuRequest, check_proc

lolpath = 'F:\\英雄联盟-\\LeagueClient'

lcures = LcuRequest(lolpath)





# https://127.0.0.1:61621/lol-lobby/v2/comms/members
