import asyncio
import json
import time

import aiohttp
import pygetwindow
from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from Lcu import LcuRequest


class GetSummonerMatch(QThread):
    summoner_data = QtCore.pyqtSignal(dict)

    def __init__(self, max_match=20):
        super().__init__()
        #    self.wegame_cookie = ""
        self.names = []
        self.region = None
        self.lcu = LcuRequest()
        self.max_match = max_match
        self.tier_zh = {
            'unranked': '暂无段位',
            'none': '暂无段位',
            'emerald': '流光翡翠',
            'iron': '坚韧黑铁',
            'bronze': '英勇黄铜',
            'silver': '不屈白银',
            'gold': '荣耀黄金',
            'platinum': '华贵铂金',
            'diamond': '璀璨钻石',
            'master': '超凡大师',
            'grandmaster': '傲世宗师',
            'challenger': '最强王者',
        }

    def get_match(self, names, region=None):
        self.names = names
        self.region = region
        self.start()

    def count_consecutive_elements(self, lst):
        count_num = 1
        first = lst[0]
        if first == lst[1]:
            for bl in lst[1:]:
                if first == bl:
                    count_num += 1
                else:
                    break
            return f"{count_num}连{'胜' if first else '败'}" if count_num > 1 else ''
        else:
            first = not first
            count_num = 0
            for bl in lst[1:]:
                if first == bl:
                    count_num += 1
                else:
                    break
            return f"{count_num}连{'胜' if first else '败'}中断" if count_num > 2 else ''

    def get_lol_match(self, name):
        ppuid = self.lcu.getdata(f"/lol-summoner/v1/summoners?name={name}").json()['puuid']
        tier = self.lcu.getdata(f"/lol-ranked/v1/ranked-stats/{ppuid}").json()['highestCurrentSeasonReachedTierSR']
        games = self.lcu.getdata(
            f"/lol-match-history/v1/products/lol/{ppuid}/matches?begIndex=0&endIndex={self.max_match}"
        ).json()['games']['games']
        wins = []
        hero_worl = {}
        for game in games:
            participants = game['participants'][0]
            if not participants['championId'] in hero_worl:
                hero_worl[participants['championId']] = {
                    'wins': 0,
                    'lost': 0
                }
            if participants['stats']['win']:
                hero_worl[participants['championId']]['wins'] += 1
                wins.append(True)
            else:
                hero_worl[participants['championId']]['lost'] += 1
                wins.append(False)
        masteries = self.lcu.getdata(f"/lol-collections/v1/inventories/{ppuid}/champion-mastery").json()
        hero_collections = {}
        sorted_masteries = sorted(masteries, key=lambda x: x["championPoints"], reverse=True)
        for i, mastery in enumerate(sorted_masteries):
            hero_collections[mastery['championId']] = {
                'championPoints': mastery['championPoints'],
                'championPoints_no': i + 1
            }

        return {
            name: {
                "wins": wins.count(True),
                "lost": wins.count(False),
                #   "wins_rate":
                "state": self.count_consecutive_elements(wins),
                #   'hero_collections': hero_collections,
                'tier': self.tier_zh.get(tier.lower(), str(tier)),
                'hero_worl': hero_worl
            }
        }

    def run(self):
        for name in self.names:
            match = self.get_lol_match(name)
            print(match)

    # 此函数暂时作废
    async def get_wegame_match(self, name, region) -> dict:
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://www.wegame.com.cn/helper/lol/record/profile.html',
            'Cookie': self.wegame_cookie
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
                    res = json.loads(await resp.text())
        res = res["players"]
        for i in list(res):
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
                        return {}
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

        return summoner_info


class SummonerRect(QThread):
    def __init__(self, summoner_widows):
        super().__init__()
        self.sw = summoner_widows

    def run(self):
        windows = pygetwindow.getAllWindows()
        # 循环遍历所有窗口
        for window in windows:
            if "League" in window.title:
                print(f"窗口标题：{window.title}, 位置：{window.topleft}, 大小：{window.size}")
                # 检查窗口是否最小化
                if window.isMinimized:
                    print(f"窗口 '{window.title}' 已最小化")
                if not window.isActive:
                    print(f"窗口 '{window.title}' 被遮挡")
        time.sleep(1)
