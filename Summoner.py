import asyncio

from UI import MatchDialog

'''
def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise

    return wrapper


_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)

目前 aiohttp 存在bug ,代码正常运行出结果,但是到最后会报错：
Exception ignored in: <function _ProactorBasePipeTransport.__del__ at XXXXXXXX>
...

RuntimeError: Event loop is closed
Bug 原因:
1.https://github.com/aio-libs/aiohttp/issues/4324
2.https://github.com/aio-libs/aiohttp/issues/1925

目前解决找到的解决办法:
方案1
使用:loop.run_until_complete(main()),启动异步
方案2
async with await session.get() as resp: 
    await resp.text()
await asyncio.sleep(1)   在这里加入延迟
方案3
上面的装饰器

'''

from Lcu import lcu


class GetSummonerMatch:
    def __init__(self, max_match=20):
        super().__init__()
        self.max_match = max_match - 1
        self.tier_zh = {
            'unranked': '无段位',
            'none': '无段位',
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

    async def start(self, ppuid):
        return await self.get_lol_match(ppuid)

    def count_consecutive_elements(self, lst):
        if len(lst) < 2:
            return ''
        count_num = 1
        first = lst[0]
        if first == lst[1]:
            for bl in lst[1:]:
                if first == bl:
                    count_num += 1
                else:
                    break
            return f"{count_num}连{'胜' if first else '败'}中" if count_num > 1 else ''
        else:
            first = not first
            count_num = 0
            for bl in lst[1:]:
                if first == bl:
                    count_num += 1
                else:
                    break
            return f"{count_num}连{'胜' if first else '败'}中断" if count_num > 2 else ''

    async def get_lol_match(self, ppuid):
        tier = lcu.async_getdata(f"/lol-ranked/v1/ranked-stats/{ppuid}")
        masteries = lcu.async_getdata(f"/lol-collections/v1/inventories/{ppuid}/champion-mastery")
        games = lcu.async_getdata(
            f"/lol-match-history/v1/products/lol/{ppuid}/matches?begIndex=0&endIndex="f"{self.max_match}")
        tier, games, masteries = await asyncio.gather(tier, games, masteries)

        tier = tier['highestCurrentSeasonReachedTierSR']
        games = games['games']['games']
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
        hero_collections = {}
        sorted_masteries = sorted(masteries, key=lambda x: x["championPoints"], reverse=True)
        for i, mastery in enumerate(sorted_masteries):
            hero_collections[mastery['championId']] = {
                'championPoints': mastery['championPoints'],
                'championPoints_no': i + 1
            }
        return ppuid, {
            "wins": wins.count(True),
            "lost": wins.count(False),
            #   "wins_rate":
            "state": self.count_consecutive_elements(wins),
            'hero_collections': hero_collections,
            'tier': self.tier_zh.get(tier.lower(), str(tier)),
            'hero_worl': hero_worl
        }

    def set_max_match(self, count):
        self.max_match = count - 1


class SummonerUIRect:
    def __init__(self):
        self.bind_widows:{int:MatchDialog}= {}
        self.client_wh = '1600x900'
        self.choose_w = {
            '1600x900': 100,
            '1280x720': 0,
            '1024x576': 0,
        }
        self.offset = {
            'even': {
                '1600x900': (313, 168),
                '1280x720': (0, 0),
                '1024x576': (0, 0),
            },
            'odd': {
                '1600x900': (313, 118),
                '1280x720': (0, 0),
                '1024x576': (0, 0),
            }
        }

    def bind_ui(self, floor: int):
        """

        :param floor: 楼层
        :return:
        """

        self.bind_widows[floor] = MatchDialog()
        self.adjustment_offset()
        return self.bind_widows[floor]

    def adjustment_offset(self):
        if not self.bind_widows.keys():
            return
        floors = sorted(self.bind_widows.keys())
        count = len(floors)
        num = 0
        if count == 1:
            num = 2
        elif count == 2:
            num = 1
        elif count == 3:
            num = 1
        elif count == 4:
            num = 0
        elif count == 5:
            num = 0
        offset_w, offset_h = self.offset['even'][self.client_wh] if count % 2 == 0 else self.offset['odd'][
            self.client_wh]
        for index, value in enumerate(floors, start=num):
            self.bind_widows[value].set_offset(offset_w, offset_h + index * self.choose_w[self.client_wh])

    def close(self):
        for window in self.bind_widows.values():
            window.close()
        self.bind_widows: dict[int, MatchDialog] = {}

    def reset_client_wh(self):
        pass
