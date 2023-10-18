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
from lol_find import FindLolQP

from urllib3 import disable_warnings
from requests import request


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
    summoner_info = QtCore.pyqtSignal(int, dict)
    summoner_hero = QtCore.pyqtSignal(int, int)
    summoner_rect = QtCore.pyqtSignal()
    summoner_show = QtCore.pyqtSignal()

    def __init__(self, lcu_request: LcuRequest):
        super().__init__()
        self.loading_thread = []
        self.mutex = QMutex()
        self.mutex.lock()
        self.cond = QWaitCondition()
        self.accept_flag = True
        self.stop = True
        self.lcu = lcu_request
        self.hero_choose = -1
        self.my_summoner_id = ''
        self.find = FindLolQP()

    def hang(self):
        # 挂起线程
        self.cond.wait(self.mutex)

    def wake(self):
        # 唤醒线程
        self.cond.wakeAll()

    def run(self):
        while self.stop:
            try:
                if self.lcu.is_process:
                    print(self.lcu.getdata('/lol-gameflow/v1/gameflow-phase').text)
                    self.my_summoner_id = str(
                        self.lcu.getdata('/lol-summoner/v1/current-summoner').json()['summonerId'])

                    self.add_text.emit("客户端已开启!")
                    self.load_user_data.emit()
                    while self.stop:
                        state = self.lcu.getdata('/lol-gameflow/v1/gameflow-phase').json()
                        if state == "ChampSelect":
                            self.summoner_rect.emit()
                            self.set_text.emit("选择英雄中", "#FF1493")
                            my_cellid, teammate_names = self.get_team_information()
                            print(my_cellid, teammate_names)
                            self.lcu.getdata(f'/lol-champ-select/v1/session/actions/{my_cellid}', 'PATCH', {}, {
                                "championId": self.hero_choose,
                                "completed": False
                            })

                            chat_id = ''
                            for chat_info in self.lcu.getdata("/lol-chat/v1/conversations").json():
                                if chat_info["type"] == 'championSelect':
                                    chat_id = chat_info['id']
                                    break
                            environment = self.lcu.getdata("/riotclient/v1/crash-reporting/environment").json()[
                                'environment']
                            ##################
                            self.team_se(list(teammate_names.keys()), environment, chat_id)
                            ###############
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            task = []
                            '''
                            for k, v in teammate_names.items():
                                _ = loop.create_task(self.get_summoner(v, k, environment))
                                _.add_done_callback(self.set_summoner_info)
                                task.append(_)
                            if len(task) != 0:
                                loop.run_until_complete(asyncio.wait(task))
                            ###############
                            '''
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

    def set_summoner_info(self, summoner_info):
        floor, info = summoner_info.result()
        if info == -1:
            pass
        else:
            self.summoner_info.emit(floor, info)

    async def get_summoner(self, floor, name, region):
        cookie = "pgv_pvid=9826136483; ts_uid=2854892420; ts_last=www.wegame.com.cn/helper/lol/v2/index.html; puin=1332575979; pt2gguin=o01332575979; uin=o01332575979; tgp_id=70602779; geoid=104; lcid=2052; tgp_env=online; tgp_user_type=0; colorMode=1; pkey=0001652167B300703E7FAEE91103B4EFF24B2E01C3C57399D6D457EE0AB0543DB8307AFF9DC00DB48606825AC4231454DA168FE01632D40376E202C72069842232944A03633881D52E46846F6825EDE76E5C3BA70D306B513D5076DBDB87955252914ADDAA0B5551A9ACD22EABA579DF1FF2E09516A51151; tgp_ticket=97FE82BE7DCAE5299018262A5CDEDFDDB9039FD98702C128FC40D59D51BA3CE911CBF705E99D9850A32EBAF5CD18716C93CC523D8026B2615C55F832FA8A9A52D932BE9114ED911336F65C9B12B4426FCF4402AA2B29A793F3C1217E7B36854FEE61AC71AFB5E81CE16BC7AD2F86707259F8E3F72908AC5E2370B98D5DD7295D; tgp_biz_ticket=010000000000000000EC90F1440F1DB05BE2A09FDF4BA899AB1F5884C3182B90339D3E0DA89A80627DF524B047F1769FC9118BD1BB26AA2373422285AB89E6CCB9591436ED3E9129FA; colorMode=1; BGTheme=[object Object]; pgv_info=ssid=s2096498992"
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://www.wegame.com.cn/helper/lol/record/profile.html',
            'Cookie': cookie
        }
        region_information = [
            [1, '艾欧尼亚', "HN1"],
            [15, "暗影岛", "HN11"]
        ]

        openid = ''
        summoner_info = {}

        for i in region_information:
            if region in i:
                region = i
                break
        if region not in region_information:
            raise Exception(f"大区不存在:{region}")
        else:
            region = region[0]
        # 重置大区
        res = ''
        while "players" not in res:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, ssl=False)) as session:
                async with await session.post(
                        "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/SearchPlayer",
                        headers=headers,
                        data=json.dumps({
                            "nickname": name,
                            "from_src": "lol_helper"
                        })) as resp:
                    res = eval(await resp.text())
        for i in list(res["players"]):
            if i["area"] == region:
                openid = i["openid"]
                break
        # 获取openid
        summoner_info['near_record'] = {}
        summoner_info['record_count'] = {
            'lost': 0,
            'wins': 0
        }
        BattleReport = {}
        while "battle_count" not in BattleReport:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, ssl=False)) as session:
                async with await session.post(
                        "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetBattleReport",
                        headers=headers,
                        data=json.dumps({
                            "account_type": 2,
                            "area": region,
                            "from_src": "lol_helper",
                            "id": openid,
                        })) as resp:
                    try:
                        BattleReport = eval(await resp.text())
                    except NameError:
                        print(name, '隐藏')
                        return -1, -1
                # 用异常判断是否隐藏生涯
        summoner_info['battle_count'] = BattleReport['battle_count']
        summoner_info['season_list'] = BattleReport['season_list']
        Champion = {}
        while 'champion_list' not in Champion:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, ssl=False)) as session:
                async with await session.post(
                        "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetChampion",
                        headers=headers,
                        data=json.dumps({
                            "account_type": 2,
                            "area": region,
                            "from_src": "lol_helper",
                            "id": openid
                        })) as resp:
                    Champion = eval(await resp.text())
        summoner_info['champion_list'] = {k['champion_id']: {"total": k["total"], "wins": k["wins"]} for k in
                                          Champion["champion_list"]}
        for _ in [0, 10, 20]:
            BattleList = {}
            while 'battles' not in BattleList:
                async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, ssl=False)) as session:
                    async with await session.post(
                            "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetBattleList",
                            headers=headers,
                            data=json.dumps({
                                "account_type": 2,
                                "area": region,
                                "count": 10,
                                "filter": "",
                                "from_src": "lol_helper",
                                "id": openid,
                                "offset": _
                            })) as resp:
                        BattleList = eval(await resp.text())
            for i in BattleList['battles']:
                if i['champion_id'] not in summoner_info['near_record']:
                    summoner_info['near_record'][i['champion_id']] = {
                        'wins': 0,
                        'lost': 0
                    }
                if i['win'] == 'Fail':
                    summoner_info['record_count']['lost'] += 1
                    summoner_info['near_record'][i['champion_id']]['lost'] += 1
                elif i['win'] == 'Win':
                    summoner_info['record_count']['wins'] += 1
                    summoner_info['near_record'][i['champion_id']]['wins'] += 1
                elif i['win'] == 'LeaverFail':
                    pass
                else:
                    raise Exception(f"i['win']:{i['win']},{name},{i}")

        return floor, summoner_info
