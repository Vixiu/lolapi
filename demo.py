import sys
import time
# int(time.time() / 600000)
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

import FuwenUi
from Lcu import LcuRequest, check_proc

lolpath = 'F:\\1\\英雄联盟-\\LeagueClient'

lcures = LcuRequest(lolpath)
p=''
res=lcures.getdata('/lol-regalia/v2/summoners/2935096509/regalia')
print(res.text)



# https://127.0.0.1:61621/lol-lobby/v2/comms/members
