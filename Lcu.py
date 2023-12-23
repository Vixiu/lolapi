from base64 import b64encode

import json

from win32api import Sleep

from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from psutil import process_iter

from urllib3 import disable_warnings
from requests import request

from Summoner import GetSummonerMatch


class LcuRequest:
    disable_warnings()

    def __init__(self):
        self.is_process = False
        self.lcu_args = self.get_lcu_args()
        self.port, self.token = self.lcu_args.get('app-port', '0000'), self.lcu_args.get("remoting-auth-token", 'None')
        self.url = 'https://127.0.0.1:' + self.port
        self.headers = {
            "User-Agent": "LeagueOfLegendsClient",
            'Authorization': 'Basic ' + b64encode(('riot' + ':' + self.token).encode()).decode(),

        }

    def get_lcu_args(self):

        return {
            line[2:].split('=', 1)[0]: line[2:].split('=', 1)[1]
            for line in self.find_lcu_cmdline()
            if '=' in line
        }

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
        return request(method, self.url + path, headers=self.headers, data=json.dumps(data), verify=False)

    def find_lcu_cmdline(self):
        for prs in process_iter():
            if prs.name() in ['LeagueClient', 'LeagueClientUx.exe']:
                self.is_process = True
                return prs.cmdline()
        self.is_process = False
        return []

    def reset(self):
        self.__init__()


class LcuThread(QThread):
    set_text = QtCore.pyqtSignal(str, str)  # 设置文本
    add_text = QtCore.pyqtSignal(str)  # 增加文本
    load_user_data = QtCore.pyqtSignal()  # 读取信息
    window_enable = QtCore.pyqtSignal(bool)  # 窗口是否可点击
    ######################################
    summoner_init = QtCore.pyqtSignal(dict)  # 初始化
    summoner_info = QtCore.pyqtSignal(str, dict)  # 设置信息
    summoner_hero = QtCore.pyqtSignal(str, int)  # 设置英雄 puuid, 英雄id
    summoner_hide = QtCore.pyqtSignal()

    def __init__(self, lcu_request: LcuRequest):
        super().__init__()
        self.accept_flag = True
        self.summoner_ishow = False
        self.summoner_my_ishow = True
        self.ban_hero = [350]
        self.ban_flag = True
        self.ban_second = 1000
        ################
        self.lcu = lcu_request
        self.hero_choose = -1
        self.summoner_match = GetSummonerMatch()
        self.summoner_match.summoner_data.connect(self.set_summoner_info)
        self.stop = True

    def run(self):
        while self.stop:

            #  try:
            if self.lcu.is_process:
                self.add_text.emit("客户端已开启!")
                self.load_user_data.emit()

                while self.stop:
                    state = self.lcu.getdata('/lol-gameflow/v1/gameflow-phase').json()
                    if state == "ChampSelect":
                        self.set_text.emit("选择英雄中", "#FF1493")
                        my_cellId, ppuid_floor = self.get_team_information()
                        self.lcu.getdata(f'/lol-champ-select/v1/session/actions/{my_cellId}', 'PATCH', {}, {
                            "championId": self.hero_choose,
                            "completed": False
                        })

                        chat_id = ''
                        for chat_info in self.lcu.getdata("/lol-chat/v1/conversations").json():
                            if chat_info["type"] == 'championSelect':
                                chat_id = chat_info['id']
                                break
                        # environment = self.lcu.getdata("/riotclient/v1/crash-reporting/environment").json()['environment']
                        # self.team_se(list(teammate_names.keys()), environment, chat_id)
                        # mode_queues = self.lcu.getdata('/lol-gameflow/v1/session').json()['gameData']['queue'][ 'id']
                        if self.summoner_ishow:
                            self.summoner_init.emit(ppuid_floor)
                            self.summoner_match.get_match(ppuid_floor.keys(), self.lcu.port, self.lcu.headers)

                        # 进入房间前的初始化
                        if self.summoner_my_ishow:
                            my_cellId = -998
                        ban_pick = True
                        while self.lcu.getdata('/lol-gameflow/v1/gameflow-phase').json() == "ChampSelect":
                            session = self.lcu.getdata('/lol-champ-select/v1/session').json()

                            if ban_pick and self.ban_flag and session["timer"]["phase"] == 'BAN_PICK':
                                for hero_id in self.ban_hero:
                                    pass
                                res = self.lcu.getdata(f"/lol-champ-select/v1/session/actions/{session['localPlayerCellId']}", 'patch', data={
                                    "championId": 350,
                                    "completed": True
                                }).text
                                self.lcu.getdata("/lol-chat/v1/conversations/" + chat_id + "/messages", method='post', data={
                                    "body": "ban.",
                                    "type": "ban"  # String,
                                })
                                print(res)
                                ban_pick = False
                            for team in session.get('myTeam', []):
                                if self.summoner_ishow and team['championId'] > 0 and team['puuid'] != '' and team['cellId'] != my_cellId:
                                    self.summoner_hero.emit(team['puuid'], team['championId'])
                            self.set_text.emit("选择英雄中", "#FF1493")
                        self.summoner_hide.emit()
                    elif state == "ReadyCheck":
                        if self.accept_flag:
                            self.lcu.getdata('/lol-matchmaking/v1/ready-check/accept', 'post')
                            self.set_text.emit("已接受", "#FF1493")
                        else:
                            self.set_text.emit("已找到对局", "#FF1493")
                    elif state == "InProgress":
                        self.set_text.emit("游戏开始", "#FF1493")
                    elif state == "Matchmaking":
                        self.set_text.emit("寻找对局中", "#FF1493")
                    elif state == "Lobby":
                        self.set_text.emit("房间内", "#FF1493")
                    elif state == "None":
                        self.set_text.emit("大厅中", "#FF1493")
                    elif state == "EndOfGame":
                        self.set_text.emit("结算界面内", "#FF1493")
                    Sleep(100)
                    # 不加延迟可能会卡
            else:
                self.set_text.emit("等待客户端开启", "#FF1493")
                Sleep(400)
                self.lcu.reset()
            ''''    
            except :
                self.set_text.emit("等待客户端", "#FF1493")
                Sleep(400)
                self.lcu.reset()
            '''

    def get_team_information(self):
        """
        :return:
        我的楼层， { 名字:楼层}
        """

        ppuid_floor = {}
        session = self.lcu.getdata('/lol-champ-select/v1/session').json()
        my_team = session['myTeam']
        my_cellId = session['localPlayerCellId']
        for team in my_team:
            pass
        return my_cellId, ppuid_floor

    def set_summoner_info(self, puuid, data):
        self.summoner_info.emit(puuid, data)
