import sys
import time
# int(time.time() / 600000)
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

import Fuwen
from Lcu import LcuRequest, CheckProc
from lol_find import FindLolQP
a = FindLolQP()

a.get_info("李青信迎者LeeSin",'暗影岛')


'''
            if data:
                for j in data:
                    if daqu.startswith(j[2]):
                        self.cur.execute("SELECT * FROM qbang WHERE qq=" + "\'" + j[0] + "\'")
                        data = self.cur.fetchall()
                        if data:
                            ls = []
                            for q in data:
                                ls.append(q[1])
                            qqs.append({i: {"QQ": j[0],
                                            "Phone": ls
                                            }
                                        })
                        else:
                            qqs.append({i: {"QQ": j[0]}})

                if not qqs:
                    qqs.append({i: {}})
            else:
                qqs.append({i: {}})
'''