import asyncio
from base64 import b64encode

import json

import aiohttp
import requests
from win32api import Sleep
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from psutil import process_iter

from urllib3 import disable_warnings
from requests import request
from Summoner import GetSummonerMatch
import logging


class LcuRequest:
    disable_warnings()

    def __init__(self, wait_lcu_thread=3):
        self.logger = logging.getLogger('my_logger')
        self.lcu_args = self.get_lcu_args()
        self.ws_session = None
        self.ws_client = None
        self.event_call_back = {}
        if self.lcu_args:
            self.port, self.token = self.lcu_args.get('app-port', '0000'), self.lcu_args.get("remoting-auth-token", 'None')
            self.url = 'https://127.0.0.1:' + self.port
            self.headers = {
                "User-Agent": "LeagueOfLegendsClient",
                'Authorization': 'Basic ' + b64encode(('riot' + ':' + self.token).encode()).decode(),

            }

            while True:
                try:
                    res = self.getdata('/riotclient/ux-state')
                    if res.status_code == 200:
                        break
                except requests.exceptions.ConnectionError:
                    print('等待客户端加载完毕')


        elif wait_lcu_thread > -1:
            self.logger.warning(f'未找到Lcu进程,将在{wait_lcu_thread}秒后重试...')
            Sleep(wait_lcu_thread * 1000)
            self.__init__()
        else:
            self.logger.warning('未找到Lcu进程,已退出')

    def get_lcu_args(self):
        cmd_line = []
        for prs in process_iter():
            if prs.name() in ['LeagueClient', 'LeagueClientUx.exe']:
                cmd_line = prs.cmdline()
                break
        return {
            line[2:].split('=', 1)[0]: line[2:].split('=', 1)[1]
            for line in cmd_line
            if '=' in line
        }

    def getdata(self, path, method='get', data=None) -> requests.Response:
        """
        :param path:路径
        :param method:方式,默认get
        :param headers:参数
        :param data:内容body
        :return:数据
        """
        return request(method, self.url + path, headers=self.headers, data=json.dumps(data), verify=False)

    async def connect_websocket(self):
        self.ws_session = aiohttp.ClientSession(auth=aiohttp.BasicAuth('riot', self.token), headers={
            "User-Agent": "LeagueOfLegendsClient",
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.ws_client = await self.ws_session.ws_connect(f'wss://127.0.0.1:{self.port}', ssl=False)
        '''
     
        '''

    async def async_getdata(self, path, method='GET', data=None):
        async with await self.ws_session.request(method, f'{self.url}{path}', data=json.dumps(data), ssl=False) as resp:
            data = json.loads(await resp.text())
            return data

    async def subscribe(self, event: str, call_back):
        if event in self.event_call_back:
            pass
        else:
            await self.ws_client.send_json([5, event])
            self.event_call_back[event] = call_back

    async def unsubscribe(self, event: str):
        if event in self.event_call_back:
            del self.event_call_back[event]
        else:
            pass

    async def run(self):
        loop = asyncio.get_running_loop()
        async for msg in self.ws_client:
            if msg.type == aiohttp.WSMsgType.TEXT:
                # print(f'Received message: {msg.data}')
                loop.create_task(self.event_call_back['OnJsonApiEvent'](msg.data))
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print(f'WebSocket connection closed with exception {self.ws_client.exception()}')
        await self.ws_session.close()

    async def close_websocket(self):
        await self.ws_client.close()
        await self.ws_session.close()

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
                        self.lcu.getdata(f'/lol-champ-select/v1/session/actions/{my_cellId}', 'PATCH', {
                            "championId": self.hero_choose,
                            "completed": False
                        })
                        print(my_cellId, 'mycellid')
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
