import base64
import json
import os
import re
import time

import requests
import urllib3
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore


def CheckProc(name):
    ps = os.popen("C:/WINDOWS/system32/tasklist.exe", "r")
    pp = ps.readlines()
    ps.close()
    for i in pp:
        if name in i:
            return True
    return False


class LcuRequest:
    urllib3.disable_warnings()

    def __init__(self, path):
        self.path = path
        self.port, self.pw = self.getportpw(path)
        self.url = 'https://127.0.0.1:' + self.port
        self.Authorization = base64.b64encode(('riot' + ':' + self.pw).encode()).decode()
        self.headers = {
            'Authorization': 'Basic ' + self.Authorization
        }

    def getportpw(self, path):
        dirlist = os.listdir(path)
        dtlist = []
        for i in dirlist:
            if 'LeagueClientUxHelper-renderer' in i:
                dtlist.append(i)
        dtlist.sort(reverse=True)  # 排序
        too = ''
        for i in dtlist:
            with open(path + '\\' + i, 'r', encoding='ansi') as file:
                while True:
                    line = file.readline()
                    if line.find("bootstrap.html") != -1:
                        too = line
                        break
                    elif line == '':
                        break
            if too != '':
                break
        port = re.split('1:([0-9]*)', too)[1]
        pw = re.split('riot:([\\w-]*)', too)[1]
        return port, pw

    def getdata(self, path, method='get', headers=None, data=None):
        """
        :param path:路径
        :param method:方式,默认get
        :param headers:参数
        :param data:内容body
        :return:数据
        """
        if headers is None:
            headers = {}
        headers.update(self.headers)
        return requests.request(method, self.url + path, headers=self.headers, data=json.dumps(data), verify=False)

    def resetport(self):
        self.__init__(self.path)


class LcuThread(QThread):
    stext = QtCore.pyqtSignal(str, str)
    gtext = QtCore.pyqtSignal(str)  # 定义
    gamestart = QtCore.pyqtSignal()
    enable = QtCore.pyqtSignal(bool)

    def __init__(self, LcuRequest):
        super().__init__()
        self.acceptflag = False
        self.choiceflag = False
        self.stop = True
        self.lcures = LcuRequest
        self.herochoose = -1

    def run(self):
        self.enable.emit(False)
        while self.stop:
            while True:
                if CheckProc('LeagueClient.exe'):
                    # 一级加载
                    try:
                        self.enable.emit(False)
                        self.lcures.resetport()
                        while self.lcures.getdata('/lol-summoner/v1/current-summoner').json().get(
                                'errorCode') == 'RPC_ERROR':
                            pass
                        # 三级加载
                        # time.sleep(2)
                        self.gtext.emit("客户端已经载入!")
                        self.enable.emit(True)
                        self.gamestart.emit()  # 初始化
                        while self.stop and CheckProc('LeagueClient.exe'):
                            if CheckProc('League of Legends.exe'):
                                self.stext.emit("游戏已经开始", "#FF1493")
                                time.sleep(3)
                            else:
                                try:
                                    if self.herochoose > -1:
                                        self.lcures.getdata('/lol-champ-select/v1/session/actions/1', 'PATCH', {}, {
                                            "championId": self.herochoose,
                                            "completed": True
                                        })

                                    elif self.acceptflag:
                                        self.lcures.getdata('/lol-matchmaking/v1/ready-check/accept', 'post')
                                    #   self.gtext.emit("接受中...")
                                except Exception:
                                    self.gtext.emit("客户端退出!")
                                    break
                        break
                    except Exception:
                        # 二级加载
                        self.stext.emit("等待客户端加载", "#FF1493")
                        time.sleep(1)
                else:
                    self.stext.emit("等待客户端开启", "#FF1493")
