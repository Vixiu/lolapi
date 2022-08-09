import sys
import time
# int(time.time() / 600000)
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

import Fuwen
from Lcu import LcuRequest, CheckProc
from lol_find import FindLolQP
a = FindLolQP()
s1=a.get_info(["李青信迎者LeeSin","航哥ZZZZ","丿蔑视灬一切"],'HN11')
print(s1)
for i in s1:
    if s1[i]:
        print(i)
        for j in s1[i]:
            print()
    else:
        print(i+":未找到")

#for i in ["[", "]", '\'', '{', '}']:
 #   s1 = s1.replace(i,'')


