import base64
import json
import os
import re
import sys
import time

import requests
import urllib3
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore
import traceback
from lol_find import FindLolQP


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
    test = QtCore.pyqtSignal(int)
    fuwen = QtCore.pyqtSignal(bool)

    def __init__(self, lcu_request):
        super().__init__()
        self.acceptflag = False
        self.choiceflag = False
        self.stop = True
        self.lcures = lcu_request
        self.herochoose = -1
        self.l = FindLolQP()

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
                        # ----------------------
                        while self.stop and CheckProc('LeagueClient.exe'):
                            if CheckProc('League of Legends.exe'):
                                self.stext.emit("游戏已经开始", "#FF1493")
                            # time.sleep()
                            else:
                                try:
                                    if self.lcures.getdata("/lol-gameflow/v1/gameflow-phase").json() == 'ChampSelect':
                                        # 选人

                                        # self.fuwen.emit(True)

                                        summoner_id = self.lcures.getdata('/lol-summoner/v1/current-summoner').json()[
                                            'summonerId']
                                        cellid = 0
                                        teamsummid = []
                                        names = []

                                        res = self.lcures.getdata("/lol-champ-select/v1/session").json()

                                        for i in list(res['myTeam']):
                                            if i['summonerId'] == summoner_id:
                                                cellid = i['cellId']
                                            else:
                                                teamsummid.append(i['summonerId'])

                                        print('er-', cellid)

                                        for i in teamsummid:
                                            na = self.lcures.getdata("/lol-summoner/v1/summoners/" + str(i)).json()
                                            names.append(na['displayName'])

                                        roomyid = self.lcures.getdata("/lol-chat/v1/conversations").json()[0]['id']
                                        environment = \
                                            self.lcures.getdata("/riotclient/v1/crash-reporting/environment").json()[
                                                'environment']

                                        res = self.lcures.getdata("/lol-champ-select/v1/session").json()['actions'][0]
                                        for i in range(len(res)):
                                            if res[i]['actorCellId'] == cellid:
                                                cellid = i
                                                break
                                        print('yi-', cellid)
                                        self.lcures.getdata('/lol-champ-select/v1/session/actions/' + str(cellid + 1),
                                                            'PATCH', {}, {
                                                                "championId": self.herochoose,
                                                                "completed": False
                                                            })
                                        for i in names:
                                            cod17 = self.l.getName_newApi(i, environment)
                                            s1 = ''
                                            if list(cod17[0].values())[0]:
                                                s1 = str(cod17[0])

                                            else:
                                                for i in cod17:
                                                    if list(i.values())[0]:
                                                        s1 = list(cod17[0].keys())[0] + ' 历史id: ' + str(
                                                            cod17[1:]).replace(
                                                            "{}", '未找到')
                                                        break
                                            if s1 == '':
                                                s1 = str(i) + '未找到'
                                            print(s1)
                                            for i in ["[", "]", '\'', '{', '}']:
                                                s1 = s1.replace(i, '')
                                            self.lcures.getdata(
                                                "/lol-chat/v1/conversations/" + roomyid + "/messages",
                                                method='post', headers=None, data={
                                                    "body": s1,  # String
                                                    "type": "celebration"  # String,
                                                })
                                            self.lcures.getdata(
                                                "/lol-chat/v1/conversations/" + roomyid + "/messages",
                                                method='post', headers=None, data={
                                                    "body": "---------------------------------------------------------------",
                                                    # String
                                                    "type": "ban"  # String,
                                                })

                                        # 预获取信息
                                        while self.lcures.getdata(
                                                "/lol-gameflow/v1/gameflow-phase").json() == 'ChampSelect':
                                            my_actions = \
                                                self.lcures.getdata("/lol-champ-select/v1/session").json()['actions'][
                                                    0][
                                                    cellid]
                                            self.test.emit(my_actions['championId'])
                                        # self.fuwen.emit(False)

                                    elif self.acceptflag:
                                        self.lcures.getdata('/lol-matchmaking/v1/ready-check/accept', 'post')
                                    #   self.gtext.emit("接受中...")
                                except Exception as e:
                                    traceback.print_exc()
                                    print("错误:", e)
                                    self.gtext.emit("客户端退出!")
                                    break

                        break
                    except Exception:
                        # 二级加载
                        self.stext.emit("等待客户端加载", "#FF1493")
                        time.sleep(1)
                else:
                    self.stext.emit("等待客户端开启", "#FF1493")
