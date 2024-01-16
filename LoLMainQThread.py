import asyncio

from win32api import Sleep
from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from Summoner import GetSummonerMatch

from Lcu import lcu
from 弃用.GetSE import FindLolQP


class LcuThread(QThread):
    set_sata = QtCore.pyqtSignal(str, str)  # 设置状态
    load_user_data = QtCore.pyqtSignal()  # 读取信息
    window_enable = QtCore.pyqtSignal(bool)  # 窗口是否可点击
    ######################################
    summoner_init = QtCore.pyqtSignal(dict)  # 初始化
    summoner_info = QtCore.pyqtSignal(str, dict)  # 设置信息
    summoner_hero = QtCore.pyqtSignal(str, int)  # 设置英雄 puuid, 英雄id
    summoner_hide = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.control_auto_accept = True
        self.control_grab_hero = {
            'sata': False,  # 开关
            'championId': 86,  # 英雄id
            'completed': False  # 是否确认
        }
        self.control_summoner = {
            "sata": True,
            "self_show": False,

        }
        self.control_ban_hero = {
            "sata": True,
            "hero_id": [-1],

        }
        ###############################
        self.summoner_match = GetSummonerMatch(40)
        self.find = FindLolQP()

    async def marketing_accept_lol(self, data: dict):
        """
        回调函数-自动接受
        :param data:
        :return:
        """
        if self.control_auto_accept and data.get('playerResponse', "") == 'None':
            await lcu.async_getdata('/lol-matchmaking/v1/ready-check/accept', 'post')

    async def game_flow_phase_lol(self, phase):
        """
        回调函数-秒选英雄
        :param phase:
        :return:
        """

        if phase == 'ChampSelect':
            s = []
            session = await lcu.async_getdata('/lol-champ-select/v1/session')
            CellId = session["localPlayerCellId"]
            if session['hasSimultaneousPicks'] and self.control_grab_hero['sata']:
                for action in session["actions"][0]:
                    if action["actorCellId"] == CellId:
                        CellId = action["id"]
                        break
                await lcu.async_getdata(f'/lol-champ-select/v1/session/actions/{CellId}', 'PATCH', {
                    "championId": self.control_grab_hero['championId'],
                    "completed": self.control_grab_hero['completed']
                })
            ppuid_floor = {}
            for team in session['myTeam']:
                if team['summonerId'] != 0:
                    ppuid_floor[team['puuid']] = team['cellId']
                    s.append(team['summonerId'])

            self.summoner_init.emit(ppuid_floor)

            loop = asyncio.get_running_loop()
            loop.create_task(self.team_se(s))
            for ppuid in ppuid_floor.keys():
                _ = loop.create_task(self.summoner_match.start(ppuid))
                _.add_done_callback(self.set_summoner_info)

        else:
            self.summoner_hide.emit()

    async def champ_select_session(self, session):
        for team in session.get('myTeam', []):
            if self.control_summoner['sata'] and team['championId'] > 0 and team['puuid'] != '':
                self.summoner_hero.emit(team['puuid'], team['championId'])

    async def main(self, event):
        loop = asyncio.get_running_loop()
        await lcu.start()
        self.load_user_data.emit()
        await asyncio.wait([loop.create_task(lcu.subscribe(k, v)) for k, v in event.items()])
        await lcu.run()

    def run(self):
        """
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
                """
        event_handling = {
            'OnJsonApiEvent_lol-matchmaking_v1_ready-check': self.marketing_accept_lol,  # 自动接受对局
            'OnJsonApiEvent_lol-gameflow_v1_gameflow-phase': self.game_flow_phase_lol,
            'OnJsonApiEvent_lol-champ-select_v1_session': self.champ_select_session,
        }
        while True:
            asyncio.run(self.main(event_handling))

    def set_summoner_info(self, task):
        result = task.result()
        self.summoner_info.emit(*result)

    async def team_se(self, sm):
        names = []
        for s in sm:
            js = await lcu.async_getdata(f'/lol-summoner/v1/summoners/{s}')
            names.append(js["displayName"])

        info = self.find.get_info(names, '暗影岛')
        print(str(info).replace("'", '').replace('{', '').replace('}', '}'))
        """
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
        """
