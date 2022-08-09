import json
import pymysql
import urllib3
from requests import request

urllib3.disable_warnings()


class FindLolQP:
    def __init__(self):
        self.wgcookie = "pgv_pvid=1595395908; ts_uid=1211749850; PTTuserFirstTime=1656201600000; weekloop=0-27-28-29; " \
                        "isHostDate=19188; puin=3036346407; pt2gguin=o03036346407; uin=o03036346407; tgp_id=250478907; geoid=45; " \
                        "lcid=2052; tgp_env=online; tgp_user_type=0; colorMode=1; " \
                        "pkey" \
                        "=000162D117F500707E577507233AD202CC049E39295A101FD29F43265C1B079FE309F9327386689C2848D6F8B5C929DAB5AD73308DF52482F2BEF86E2E766B137EBAF7CD6890994E17808CCD09A823F6F05F30CE587267E8B73C2F4BF0E925B38FE64ABDB20C3A94DFDD1F0F7AF8AFB18AE50D798EEC6870; tgp_ticket=0E24D067BC54B031A1699F1A4D3D74DA1480ED7DA7FCF4FCDC5E95E76B2575FDE7FF8B4EE4C33A1166FBEAC758D1403C012A5BB5B5C93CB92B7E3508787131142D10AB762A71ADD8EA05A141A73128285F52B497E066EF454CFFBD1437CF5EA060EB273D2F852E1FA9A59B7D5031D5A587352ED0967832E301E966C6DC525CC0; ssr=0; colorMode=1; BGTheme=[object Object]; pgv_info=ssid=s1355991640; language=zh_CN; tgp_biz_ticket=010000000000000000E96CB543F284C2EA146DA547EFFB7187CFC26403A96A8CB1B79BD63591412CC5088E282302D30679ECDD47D92567D3BBD9880519AABD2E34A8D863A8CBC481EE; region=CN; ts_last=www.wegame.com.cn/helper/lol/search/index.html "
        self.connect = pymysql.connect(host='localhost',  # 本地数据库
                                       user='root',
                                       password='123456',
                                       db='se',
                                       charset='utf8')  # 服务器名,账户,密码，数据库名称

    def getName_newApi(self, name, region, cookie=None):
        if cookie is None:
            cookie = self.wgcookie
        region_information = {
            "艾欧尼亚": 1,
            "暗影岛": 15,
        }
        hn_infm = {
            "HN1": 1,
            "HN11": 15
        }
        r = ''
        if region in hn_infm:
            region = hn_infm[region]
        elif region in region_information:
            region = region_information[region]
        else:
            return "不存在:" + region
        for k, v in region_information.items():
            if v == region:
                r = k

        # print(r,region)
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://www.wegame.com.cn/helper/lol/record/profile.html',
            'Cookie': cookie
        }
        lastname = {name}
        uuid = ""

        res = request('post',
                      "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/SearchPlayer",
                      # /GetBattleList
                      headers=headers,
                      data=json.dumps({
                          "nickname": name, "from_src": "lol_helper"
                      }),
                      verify=False
                      ).json()
        while "players" not in res:
            res = request('post',
                          "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/SearchPlayer",
                          # /GetBattleList
                          headers=headers,
                          data=json.dumps({
                              "nickname": name, "from_src": "lol_helper"
                          }),
                          verify=False
                          ).json()

        for i in list(res["players"]):
            if i["area"] == region:
                uuid = i["openid"]
                break

        res = request('post',
                      "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetUserSnapshot",
                      headers=headers, data=json.dumps({
                "account_type": 2,
                "id": uuid,
                "area": region,
                "action_type": 0,
                "offset": 0,  # 开始
                "limit": 999,  # 结束
                "from_src": "lol_helper"
            }),
                      verify=False
                      ).json()
        while "snapshots" not in res:
            res = request('post',
                          "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetUserSnapshot",
                          headers=headers, data=json.dumps({
                    "account_type": 2,
                    "id": uuid,
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
        ls = list(lastname)
        ls.append(name)
        ls.reverse()

        return self.get_qq(ls, r)

    def get_qq(self, names, daqu):
        qqs = []
        for i in names:
            self.cur.execute("SELECT * FROM lols WHERE lolname=" + "\'" + i + "\'")
            data = self.cur.fetchall()
            if data:
                for j in data:
                    if daqu.startswith(j[2]):
                        self.cur.execute("SELECT * FROM qbang WHERE qq=" + "\'" + j[0] + "\'")
                        data = self.cur.fetchall()
                        if data:
                            ls = []
                            for q in data:
                                ls.append(q[1])
                            qqs.append({i: {"QQ": j[0],
                                            "Phone": ls
                                            }
                                        })
                        else:
                            qqs.append({i: {"QQ": j[0]}})

                if not qqs:
                    qqs.append({i: {}})
            else:
                qqs.append({i: {}})

        return qqs


"""
ls={
    'name2':{
        'phone':1234,
        'dizhi':"111",
        '1234':'1234'
    },
    'name1':{
        'phone':[1234,],
        'dizhi':"111",
        '1234':'1234'
    }
}

"""
