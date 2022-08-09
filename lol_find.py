import json
import pymysql
import urllib3
from requests import request

urllib3.disable_warnings()


class FindLolQP:
    def __init__(self):
        self.cookie = "pgv_pvid=1595395908; ts_uid=1211749850; PTTuserFirstTime=1656201600000; weekloop=0-27-28-29; " \
                      "isHostDate=19188; puin=3036346407; pt2gguin=o03036346407; uin=o03036346407; tgp_id=250478907; geoid=45; " \
                      "lcid=2052; tgp_env=online; tgp_user_type=0; colorMode=1; " \
                      "pkey" \
                      "=000162D117F500707E577507233AD202CC049E39295A101FD29F43265C1B079FE309F9327386689C2848D6F8B5C929DAB5AD73308DF52482F2BEF86E2E766B137EBAF7CD6890994E17808CCD09A823F6F05F30CE587267E8B73C2F4BF0E925B38FE64ABDB20C3A94DFDD1F0F7AF8AFB18AE50D798EEC6870; tgp_ticket=0E24D067BC54B031A1699F1A4D3D74DA1480ED7DA7FCF4FCDC5E95E76B2575FDE7FF8B4EE4C33A1166FBEAC758D1403C012A5BB5B5C93CB92B7E3508787131142D10AB762A71ADD8EA05A141A73128285F52B497E066EF454CFFBD1437CF5EA060EB273D2F852E1FA9A59B7D5031D5A587352ED0967832E301E966C6DC525CC0; ssr=0; colorMode=1; BGTheme=[object Object]; pgv_info=ssid=s1355991640; language=zh_CN; tgp_biz_ticket=010000000000000000E96CB543F284C2EA146DA547EFFB7187CFC26403A96A8CB1B79BD63591412CC5088E282302D30679ECDD47D92567D3BBD9880519AABD2E34A8D863A8CBC481EE; region=CN; ts_last=www.wegame.com.cn/helper/lol/search/index.html "
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

    def get_lastname(self, name, region):

        """
        :param name: 名字
        :param region: 大区
        :return:数组，第一个元素为初始名字
        """
        region = self.set_region(region)[0]
        lastname = {name}  # 集合去重
        openid = ""
        res = ''
        while "players" not in res:
            res = request('post',
                          "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/SearchPlayer",
                          # /GetBattleList
                          headers=self.headers,
                          data=json.dumps({
                              "nickname": name, "from_src": "lol_helper"
                          }),
                          verify=False
                          ).json()
        for i in list(res["players"]):
            if i["area"] == region:
                openid = i["openid"]
                break
        # 获取 openid
        res = ''
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
            if len(info_dict['手机号'])==1:
                cur.execute(f"SELECT * from phone  WHERE phone =({list(info_dict['手机号'])[0]})")
            else:
                cur.execute("SELECT * from phone  WHERE phone in" + str(tuple(info_dict['手机号'])))
            print(str(tuple(info_dict['手机号'])))
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


    def get_info(self, name, region):
        """

        :param name: 名字
        :param region: 大区
        :return: 字典
        """

        # print(self.get_lastname(name, region))
        names = ['丿蔑视灬一切', '我LOVE卢-']
        print(self.info(names, region))

    def set_region(self, region):
        for i in self.region_information:
            if region in i:
                region = i
                break
        if region not in self.region_information:
            raise Exception("大区不存在", region)
        else:
            return region


"""
ls={

    'name':{
        '历史id:':123,444
        'QQ':1234
        '手机号':1234,
        '地址':"111",
        '身份证':'1234'
    }
    
    
    
}

"""
