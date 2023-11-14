import asyncio
from base64 import b64encode

import json

import time
import traceback

import aiohttp
import requests

import win32com.client
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, QMutex, QWaitCondition
from psutil import process_iter
from win32api import Sleep

from urllib3 import disable_warnings
from requests import request

#from GetSummonerMatch import GetSummonerMatch


class LcuRequest:
    disable_warnings()

    def __init__(self):
        self.is_process = False
        self.lcu_args = self.get_lcu_args()
        self.port, self.pw = self.lcu_args.get('app-port', '0000'), self.lcu_args.get("remoting-auth-token", 'None')
        self.url = 'https://127.0.0.1:' + self.port
        self.headers = {
            "User-Agent": "LeagueOfLegendsClient",
            'Authorization': 'Basic ' + b64encode(('riot' + ':' + self.pw).encode()).decode(),

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
            if prs.name() in ['LeagueClientUx', 'LeagueClientUx.exe']:
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
    summoner_info = QtCore.pyqtSignal(dict)
    summoner_hero = QtCore.pyqtSignal(int, int)
    summoner_rect = QtCore.pyqtSignal()  # 设置信息位置
    summoner_show = QtCore.pyqtSignal()

    def __init__(self, lcu_request: LcuRequest):
        super().__init__()
        self.accept_flag = True
        self.stop = True
        self.lcu = lcu_request
        self.hero_choose = -1
        self.my_summoner_id = ''
        self.get_summoner_match = GetSummonerMatch()
        self.get_summoner_match.summoner_data.connect(self.set_summoner_info)

    def run(self):
        while self.stop:
            try:
                if self.lcu.is_process:
                    print(self.lcu.getdata('/lol-gameflow/v1/gameflow-phase').text)
                    self.my_summoner_id = str(
                        self.lcu.getdata('/lol-summoner/v1/current-summoner').json()['summonerId'])
                    self.add_text.emit("客户端已开启!")
                    self.load_user_data.emit()
                    self.summoner_rect.emit()
                    while self.stop:
                        state = self.lcu.getdata('/lol-gameflow/v1/gameflow-phase').json()
                        if state == "ChampSelect":
                            self.set_text.emit("选择英雄中", "#FF1493")
                            my_cellid, teammate_names = self.get_team_information()
                            self.lcu.getdata(f'/lol-champ-select/v1/session/actions/{my_cellid}', 'PATCH', {}, {
                                "championId": self.hero_choose,
                                "completed": False
                            })
                            """
                            chat_id = ''
                            for chat_info in self.lcu.getdata("/lol-chat/v1/conversations").json():
                                if chat_info["type"] == 'championSelect':
                                    chat_id = chat_info['id']
                                    break
                            environment = self.lcu.getdata("/riotclient/v1/crash-reporting/environment").json()[
                                'environment']
                            self.team_se(list(teammate_names.keys()), environment, chat_id)
                            """

                            # mode_queues = self.lcu.getdata('/lol-gameflow/v1/session').json()['gameData']['queue'][
                            # 'id']
                            while self.lcu.getdata('/lol-gameflow/v1/gameflow-phase').json() == "ChampSelect":
                                '''
                                for _, floor in teammate_names.items():
                                    smr = self.lcu.getdata(f"/lol-champ-select/v1/summoners/{floor}").json()
                                    self.summoner_hero.emit(floor, smr["championId"])
                                '''
                                self.set_text.emit("选择英雄中", "#FF1493")

                            #   team_info = get_team_info()
                        # self.summoner_show.emit()
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
            except requests.exceptions.ConnectionError:
                self.set_text.emit("客户端关闭中", "#FF1493")
                Sleep(400)
                self.lcu.reset()

            '''     
            except Exception as e:
                self.set_text.emit(f'未知错误:{e}', "#FF1493")
                traceback.print_exc()
                print("错误--------------:", e)
            '''

    def get_team_information(self):
        """
        :return:
        cellId 选择英雄的id
        floor
        """
        cellid = ''
        names = {}
        for i in range(10):
            res = self.lcu.getdata(f'/lol-champ-select/v1/summoners/{i}').json()
            if res["summonerId"] > 0:
                if str(res["summonerId"]) == self.my_summoner_id:
                    cellid = res["cellId"]
                else:
                    names[self.lcu.getdata(f'/lol-summoner/v1/summoners/{res["summonerId"]}').json()[
                        "displayName"]] = i

        return cellid, names

    def team_se(self, names, daqu, chat_id):
        info = self.find.get_info(names, daqu)
        print(str(info).replace("'", '').replace('{', '').replace('}', '}'))
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

    def set_summoner_info(self, data):
        self.summoner_info.emit(data)
