import json
import pymysql
import urllib3
from PyQt5.QtCore import QThread
from requests import request

urllib3.disable_warnings()


class FindLolQP:
    def __init__(self):
        self.cookie = "pgv_pvid=9826136483; ts_uid=2854892420; _qimei_q36=; _qimei_h38=fdeddbe39c4925647f83e2ef0200000f617901; _qimei_fingerprint=0350d64b0b18b3ef09eb225be21a97c5; app_env=prod; app_version=607000; platform=qq; colorMode=1; puin=1332575979; pt2gguin=o01332575979; uin=o01332575979; tgp_id=70602779; geoid=104; lcid=2052; tgp_env=online; tgp_user_type=0; pkey=000365A6AB230070B37E15B157B077A9F468BC2A35049B8FEE19EACE3BD370220EC9AE57EB2A19C7980F81BE0164F5BBC867A0E734A77A62559B4A2579F5ACF7740687A1B8BE0FACB7AB3A34E9EC3368BD33CF2A655A4A997A2213CC84AF42C47C5333D9C6522AB3B127C389434CF07232C519DF4047AC37; tgp_ticket=7512621141242D67C27E729C63C55912718618E0AC95C3BCF56A81284E96787A93762668E40C6E7A21DEA7D43D8D7788DE2E991495DAF8F343C4D3D874B3B0B3C0E563CE0482F6B87D609D9E903DD9130F07C59FB46A8E8594433C383BFC686092E4F526C6B83B784659C7C4BA5A9C1CF8B3DF2E64A59760E1A6B3D90C077AD5; tgp_biz_ticket=010000000000000000EFF2C6B6617F8B3B65B6E980F3F9D8CCE63A43689065380875CA1AD771C3552A6067C4A6D33C03CDE74AEAE5C1EF13CE01811DDF22B973F6EA07BC2D838A8FDE; colorMode=1; BGTheme=[object Object]; pgv_info=ssid=s4562427625; ts_last=www.wegame.com.cn/helper/lol/search/index.html"
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://www.wegame.com.cn/helper/lol/record/profile.html',
            'Cookie': self.cookie
        }
        self.connect = pymysql.connect(host='localhost',  # 本地数据库
                                       user='root',
                                       password='123456',
                                       db='se',
                                       charset='utf8')  # 服务器名,账户,密码，数据库名称
        self.region_information = [
            [1, '艾欧尼亚', "HN1"],
            [15, "暗影岛", "HN11"]
        ]
        self.openid = []

    def get_lastname(self, name, region):

        """
        :param name: 名字-字符串
        :param region: 大区-字符串
        :return:历史名字 数组-第一个元素为初始名字
        """
        region = self.set_region(region)[0]
        lastname = {name}  # 集合去重
        openid = ""
        res = {}
        while "players" not in res:
            res = request('post',
                          "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/SearchPlayer",
                          # /GetBattleList
                          headers=self.headers,
                          data=json.dumps({
                              "nickname": name,
                              "from_src": "lol_helper"
                          }),
                          verify=False
                          ).json()
        for i in list(res["players"]):
            if i["area"] == region:
                print(i["openid"],44444)
                openid = i["openid"]
                break
        # 获取 openid

        while "snapshots" not in res:
            res = request('post',
                          "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetUserSnapshot",
                          headers=self.headers, data=json.dumps({
                    "account_type": 2,
                    "id": openid,
                    "area": region,
                    "action_type": 0,
                    "offset": 0,  # 开始
                    "limit": 999,  # 结束
                    "from_src": "lol_helper"
                }),
                          verify=False
                          ).json()

        for i in list(res['snapshots']):
            if i["player_name"] != '':
                lastname.add(i["player_name"])
        lastname.remove(name)
        lastname = list(lastname)
        lastname.append(name)
        lastname.reverse()  # 反向列表
        return lastname

    def info(self, game_name, region):
        region = self.set_region(region)[1]
        if len(region) != 3:
            region = region[0:2]
        cur = self.connect.cursor()
        info_dict = {
            "历史ID": set(),
            "QQ": set(),
            "手机号": set(),
            "姓名": set(),
            "身份证": set(),
            "住址": set(),
            "学历": set(),
        }
        info_dict["历史ID"].update(game_name[1:])
        for i in game_name:
            cur.execute(
                f"SELECT * FROM qq_phone WHERE qq in (SELECT qq FROM lol WHERE `name`='{i}' AND region='{region}')")
            data = cur.fetchall()
            for j in data:
                info_dict['QQ'].add(j[0])
                info_dict['手机号'].add(j[1])
        if info_dict['手机号']:
            if len(info_dict['手机号']) == 1:
                cur.execute(f"SELECT * from phone  WHERE phone ='{list(info_dict['手机号'])[0]}'")
            else:
                cur.execute("SELECT * from phone  WHERE phone in" + str(tuple(info_dict['手机号'])))
            data = cur.fetchall()
            for i in data:
                info_dict['姓名'].add(i[0])
                info_dict['身份证'].add(i[2])
                info_dict['住址'].add(i[3])
                info_dict['学历'].add(i[4])
        cur.close()
        for i in list(info_dict.keys()):
            info_dict[i].discard(None)
            if not info_dict[i]:
                del info_dict[i]

        return info_dict

    def get_info(self, names, region):
        """

        :param names:  名字-数组,
        :param region:  大区-字符串
        :return: 历史Id，QQ，手机号，姓名，身份证，住址，学历 -字典 ,键为字符串,值固定为数组（数组内值为字符串）形式，只返回找到的信息,返回的字典格式如下:
    {
    'name1':{
        '历史id:':["123",444]
        'QQ':[1234]
        '手机号':[1234]
        '地址':["111"]
        '身份证':['1234']
                  }
    'name2':{
        '历史id:':[123,444]
        'QQ':[1234]
        '手机号':[1234]
        '地址':"[111"]
        '身份证':['1234']
                    }
    'name3':{}
    }
        """
        info = {}
        for i in names:
            info[i] = self.info(self.get_lastname(i, region), region)
        return info

    def set_region(self, region):
        for i in self.region_information:
            if region in i:
                region = i
                break
        if region not in self.region_information:
            raise Exception("大区不存在", region)
        else:
            return region


#f = FindLolQP()
#text = f.get_info(['还是好朋友啦'], '暗影岛')

