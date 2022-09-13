from base64 import b64encode

import json
import os
import re
import time
import traceback
import requests

import urllib3

import win32com.client
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, QMutex, QWaitCondition

from lol_find import FindLolQP

'''
def check_proc(name):
    ps = os.popen("C:/WINDOWS/system32/tasklist.exe", "r")
    pp = ps.readlines()
    ps.close()
    for i in pp:
        if name in i:
            return True
    return False
'''


def check_proc(name):
    print(1)
    is_exist = False
    wmi = win32com.client.GetObject('winmgmts:')
    processCodeCov = wmi.ExecQuery('select * from Win32_Process where name=\"%s\"' % name)
    if len(processCodeCov) > 0:
        is_exist = True
    return is_exist


class LcuRequest:
    urllib3.disable_warnings()

    def __init__(self, path):
        self.path = path
        self.port, self.pw = self.getportpw(path)
        self.url = 'https://127.0.0.1:' + self.port
        self.Authorization = b64encode(('riot' + ':' + self.pw).encode()).decode()
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
    set_fuwen_show = QtCore.pyqtSignal(bool)  #
    set_fuwen_hero = QtCore.pyqtSignal(str, str, str)

    def __init__(self, lcu_request: LcuRequest):
        super().__init__()

        self.loading_thread = []
        self.mutex = QMutex()
        self.mutex.lock()
        self.cond = QWaitCondition()

        self.accept_flag = False
        self.choice_flag = False
        self.stop = True
        self.lcu = lcu_request
        self.hero_choose = -1
        self.my_summoner_id = ''
        self.find = FindLolQP()

    def hang(self):
        self.cond.wait(self.mutex)

    def wake(self):
        self.cond.wakeAll()

    '''
    def run(self):
        while self.stop:
            try:
                self.lcures.resetport()  # 重置端口密码
                while 'errorCode' in self.lcures.getdata('/lol-summoner/v1/current-summoner').json():
                    pass
                # 二级加载，通过异常判断客户端是否加载完毕
                self.add_text.emit("客户端已经载入!")
                self.summoner_id = self.lcures.getdata('/lol-summoner/v1/current-summoner').json()['summonerId']
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
                                if self.accept_flag:
                                    self.lcures.getdata('/lol-champ-select/v1/session/actions/' + str(my_cellid), 'PATCH', {}, {
                                        "championId": self.hero_choose,
                                        "completed": False
                                    })
                                # 秒抢
                              
                                # 预获取信息
                                while self.lcures.getdata("/lol-gameflow/v1/gameflow-phase").json() == 'ChampSelect':
                                    name = self.lcures.getdata(f'/lol-champ-select/v1/summoners/{str(my_cellid - 1)}').json()["championName"]
                                    self.set_fuwen_hero.emit(name)
                            elif self.accept_flag:
                                self.lcures.getdata('/lol-matchmaking/v1/ready-check/accept', 'post')
                        except Exception as e:
                            traceback.print_exc()
                            print("错误--------------:", e)
                            self.add_test.emit("客户端退出!")
                            break
            except Exception as e:
                traceback.print_exc()
                print("错误--------------:", e)

                self.set_text.emit("等待客户端开启", "#FF1493")
'''

    def run(self):
        while self.stop:
            try:
                if 'errorCode' not in self.lcu.getdata('/lol-summoner/v1/current-summoner').json():
                    # if self.lcu.getdata('/lol-gameflow/v1/gameflow-phase').json() == 'None':
                    t1=time.time()
                    self.add_text.emit("客户端已经开启,准备初始化")
                    self.gameLoad.emit()  # 初始化

                    self.hang()  # 挂起线程,获取要读取的资源
                    for th in self.loading_thread:
                        th.wait()
                    self.loading_thread = []
                    self.add_text.emit(f"初始化完毕,共用时{time.time()-t1}秒")
                    self.my_summoner_id = str(self.lcu.getdata('/lol-summoner/v1/current-summoner').json()['summonerId'])
                    while self.stop:
                        state = self.lcu.getdata('/lol-gameflow/v1/gameflow-phase').json()
                        if state == "ChampSelect":
                            self.set_text.emit("选择英雄", "#FF1493")
                            self.set_fuwen_show.emit(True)
                            my_info, my_team = self.get_team_information()
                            #  自动接受
                            self.lcu.getdata(f'/lol-champ-select/v1/session/actions/{my_info["cellId"]}', 'PATCH', {}, {
                                "championId": self.hero_choose,
                                "completed": False
                            })

                            #  chat_id = self.lcu.getdata("/lol-chat/v1/conversations").json()[0]['id']
                            # environment = self.lcu.getdata("/riotclient/v1/crash-reporting/environment").json()['environment']
                            #  self.team_se([my_team[_]['name']for _ in my_team], environment, chat_id)

                            get_team_info = self.random_mode if len(self.lcu.getdata('/lol-champ-select/v1/session').json().get('actions', [])) == 0 else self.pick_mode
                            mode_queues = self.lcu.getdata('/lol-gameflow/v1/session').json()['gameData']['queue']['id']
                            while self.lcu.getdata('/lol-gameflow/v1/gameflow-phase').json() == "ChampSelect":
                                team_info = get_team_info()
                                if team_info is None:
                                    break
                                if team_info[my_info['cellId']] != 0:
                                    self.set_fuwen_hero.emit(str(team_info[my_info['cellId']]), my_info['lane'], str(mode_queues))

                            self.set_fuwen_show.emit(False)
                        elif state == "ReadyCheck":
                            if self.accept_flag:
                                self.lcu.getdata('/lol-matchmaking/v1/ready-check/accept', 'post')
                            self.set_text.emit("接受", "#FF1493")
                        elif state == "InProgress":
                            self.set_text.emit("游戏开始", "#FF1493")
                         #   self.wait(1000)
                        elif state == "Matchmaking":
                            self.set_text.emit("寻找对局中", "#FF1493")
                        elif state == "Lobby":
                            self.set_text.emit("房间内", "#FF1493")
                        elif state == "None":
                            self.set_text.emit("大厅中", "#FF1493")
            except requests.exceptions.ConnectionError:
                self.set_text.emit("等待客户端开启", "#FF1493")
                self.lcu.resetport()  # 重置端口密码

            except Exception as e:
                self.set_text.emit(f'未知错误:{e}', "#FF1493")
                traceback.print_exc()
                print("错误--------------:", e)

    def get_team_information(self):
        """
        :return:
        """
        my_info = {}
        team_info = {}
        info = self.lcu.getdata('/lol-champ-select/v1/session').json()
        for _ in info.get("myTeam", {}):
            if str(_["summonerId"]) == self.my_summoner_id:
                my_info = {
                    'cellId': _["cellId"],
                    'floor': _["cellId"] if _["cellId"] < 4 else _["cellId"] - 5,  # int
                    'lane': 'support' if _["cellId"] == 'utility' else _['assignedPosition']

                }
            else:
                team_info[_["cellId"]] = {
                    "name": self.lcu.getdata("/lol-summoner/v1/summoners/" + str(_["summonerId"])).json()["displayName"],
                    'floor': _["cellId"] if _["cellId"] < 4 else _["cellId"] - 5,  # int
                    #  "summonerId": info["summonerId"],
                }
        return my_info, team_info

    def team_se(self, names, daqu, chat_id):
        info = self.find.get_info(names, daqu)
        for i in info:
            if info[i]:
                self.lcu.getdata(
                    "/lol-chat/v1/conversations/" + chat_id + "/messages",
                    method='post', headers=None, data={
                        "body": i + ':',  # String
                        "type": "celebration"  # String,
                    })
                for j in info[i]:
                    self.lcu.getdata(
                        "/lol-chat/v1/conversations/" + chat_id + "/messages",
                        method='post', headers=None, data={
                            "body": "*" + j + ':' + ' , '.join(info[i][j]),  # String
                            "type": "celebration"  # String,
                        })
            else:
                self.lcu.getdata(
                    "/lol-chat/v1/conversations/" + chat_id + "/messages",
                    method='post', headers=None, data={
                        "body": i + ':未找到',  # String
                        "type": "celebration"  # String,
                    })
            self.lcu.getdata(
                "/lol-chat/v1/conversations/" + chat_id + "/messages",
                method='post', headers=None, data={
                    "body": "---------------------------------------------------------------",
                    # String
                    "type": "ban"  # String,
                })

    def random_mode(self):
        team_info = self.lcu.getdata('/lol-champ-select/v1/session').json()
        if 'actions' not in team_info:
            return None
        return {_['cellId']: _['championId'] for _ in team_info['myTeam']}

    def pick_mode(self):
        team_info = self.lcu.getdata('/lol-champ-select/v1/session').json()
        if 'actions' not in team_info:
            return None
        action = team_info['actions'][-1]
        return {_: 0 if action[_]['type'] != 'pick' else action[_]['championId'] for _ in range(len(action))}
