import base64
import json
import os
import re
import time
import traceback

import requests
import urllib3
from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from lol_find import FindLolQP


def check_proc(name):
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
    set_text = QtCore.pyqtSignal(str, str)  # 设置文本
    add_text = QtCore.pyqtSignal(str)  # 增加文本
    gameLoad = QtCore.pyqtSignal()  # 读取信息
    window_enable = QtCore.pyqtSignal(bool)  # 窗口是否可点击
    test = QtCore.pyqtSignal(int)  # 符文内英雄头像
    fuwen = QtCore.pyqtSignal(bool)  #

    def __init__(self, lcu_request: LcuRequest):
        super().__init__()
        self.acceptflag = False
        self.choiceflag = False
        self.stop = True
        self.lcures = lcu_request
        self.herochoose = -1
        self.find = FindLolQP()

    def run(self):
        while self.stop:
            while True:
                if check_proc('LeagueClient.exe'):
                    # 一级加载，判断客户端是否存在
                    try:
                        self.lcures.resetport()  # 重置端口密码
                        while 'errorCode' in self.lcures.getdata('/lol-summoner/v1/current-summoner').json():
                            pass
                        # 二级加载，通过异常判断客户端是否加载完毕
                        self.add_text.emit("客户端已经载入!")
                        self.gameLoad.emit()  # 初始化
                        # ----------------------
                        while self.stop and check_proc('LeagueClient.exe'):
                            if check_proc('League of Legends.exe'):
                                self.set_text.emit("游戏已经开始", "#FF1493")
                                time.sleep(2)  # 稍加延迟
                            else:
                                try:
                                    # 判断是否在房间内
                                    if self.lcures.getdata("/lol-gameflow/v1/gameflow-phase").json() == 'ChampSelect':
                                        team, my_cellid = self.get_team_information()
                                        self.lcures.getdata('/lol-champ-select/v1/session/actions/' + str(my_cellid),
                                                            'PATCH', {}, {
                                                                "championId": self.herochoose,
                                                                "completed": False
                                                            })
                                        # 秒抢
                                        chat_id = self.lcures.getdata("/lol-chat/v1/conversations").json()[0]['id']
                                        environment = \
                                            self.lcures.getdata("/riotclient/v1/crash-reporting/environment").json()[
                                                'environment']
                                        self.team_se(team.keys(), environment, chat_id)
                                        # 预获取信息
                                        while self.lcures.getdata(
                                                "/lol-gameflow/v1/gameflow-phase").json() == 'ChampSelect':
                                            pass


                                    elif self.acceptflag:
                                        self.lcures.getdata('/lol-matchmaking/v1/ready-check/accept', 'post')
                                except Exception as e:
                                    traceback.print_exc()
                                    print("错误--------------:", e)
                                    self.add_test.emit("客户端退出!")
                                    break
                        break
                    except Exception:
                        self.set_text.emit("等待客户端加载", "#FF1493")
                        time.sleep(1)
                else:
                    self.set_text.emit("等待客户端开启", "#FF1493")

    def get_team_information(self):
        """

        :return:
        """
        my_summonerid = self.lcures.getdata('/lol-summoner/v1/current-summoner').json()['summonerId']
        my_cellid = None
        team = {}
        for i in range(5):
            info = self.lcures.getdata(f'/lol-champ-select/v1/summoners/{i}').json()
            if info["summonerId"] > 0:
                if info["summonerId"] == my_summonerid:
                    my_cellid = info["cellId"] + 1
                else:
                    team[self.lcures.getdata("/lol-summoner/v1/summoners/" + str(info["summonerId"])).json()[
                        "displayName"]] = {
                        "cellId": info["cellId"] + 1,
                        "summonerId": info["summonerId"]
                    }

        return team, my_cellid

    def team_se(self, names, daqu, chat_id):
        info = self.find.get_info(names, daqu)
        for i in info:
            if info[i]:
                self.lcures.getdata(
                    "/lol-chat/v1/conversations/" + chat_id + "/messages",
                    method='post', headers=None, data={
                        "body": i + ':',  # String
                        "type": "celebration"  # String,
                    })
                for j in info[i]:
                    self.lcures.getdata(
                        "/lol-chat/v1/conversations/" + chat_id + "/messages",
                        method='post', headers=None, data={
                            "body": "*" + j + ':' + ' , '.join(info[i][j]),  # String
                            "type": "celebration"  # String,
                        })
            else:
                self.lcures.getdata(
                    "/lol-chat/v1/conversations/" + chat_id + "/messages",
                    method='post', headers=None, data={
                        "body": i + ':未找到',  # String
                        "type": "celebration"  # String,
                    })
            self.lcures.getdata(
                "/lol-chat/v1/conversations/" + chat_id + "/messages",
                method='post', headers=None, data={
                    "body": "---------------------------------------------------------------",
                    # String
                    "type": "ban"  # String,
                })
