import json
import pymysql
import urllib3
from PyQt5.QtCore import QThread
from requests import request

urllib3.disable_warnings()


class FindLolQP:
    def __init__(self):
        self.cookie = "pgv_pvid=7859335832; ts_uid=5841229940; region=CN; puin=1332575979; pt2gguin=o01332575979; tgp_id=70602779; geoid=45; lcid=2052; tgp_env=online; tgp_user_type=0; colorMode=1; ssr=0; colorMode=1; BGTheme=[object Object]; pgv_info=ssid=s2269171810; language=zh_CN; uin=o01332575979; tgp_ticket=E8EC0DAE4F8A0303E628F46966494B3DB8A1CD2E4D06BE4B0BFAC3684D8E571C397A5F371F7B92967D87B0D7E4DD7763F57823E8B8C716F3DDB9EA3AA0AD0618A010F6E8BE8238797D93B1AB587FC1076BFB942E75D0991964E1979D6CB83704A36D4FE1718531E455224ECBF1240D0CBE9B6806456372B05A9D513BA2029480; tgp_biz_ticket=010000000000000000B46F8ED817E964EFC335D40E3BB6D6BCA0E4D9A96AB7803E723CB67C9C75F745B6BE0B991C72D35A19CCE390BF3FA4A49B8D84D3F56CED2C8E8B343C05D2FA99; pkey=000163CEC8A90070AD28E1B5BAF470B74F737FC4B27530B92889335F621966F849F4E5FB010F9225E959571E194DDE5591E307A3644269FC3BC2009DD23E08C50C72150974679CDAEAC7D990176C64265E3B600AD7FEE4F8B0C5A8E47BB476A60A7532CB3C3C0A6253EF120089909BCFA70DB177F037030A; "
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
        res={}
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


class FindSummoner(QThread):
    def __init__(self):
        super().__init__()
        self.cookie = "pgv_pvid=7859335832; ts_uid=5841229940; region=CN; puin=1332575979; pt2gguin=o01332575979; " \
                      "tgp_id=70602779; geoid=45; lcid=2052; tgp_env=online; tgp_user_type=0; colorMode=1; ssr=0; " \
                      "colorMode=1; BGTheme=[object Object]; pgv_info=ssid=s2269171810; language=zh_CN; " \
                      "uin=o01332575979; " \
                      "tgp_ticket=E8EC0DAE4F8A0303E628F46966494B3DB8A1CD2E4D06BE4B0BFAC3684D8E571C397A5F371F7B92967D87B0D7E4DD7763F57823E8B8C716F3DDB9EA3AA0AD0618A010F6E8BE8238797D93B1AB587FC1076BFB942E75D0991964E1979D6CB83704A36D4FE1718531E455224ECBF1240D0CBE9B6806456372B05A9D513BA2029480; tgp_biz_ticket=010000000000000000B46F8ED817E964EFC335D40E3BB6D6BCA0E4D9A96AB7803E723CB67C9C75F745B6BE0B991C72D35A19CCE390BF3FA4A49B8D84D3F56CED2C8E8B343C05D2FA99; pkey=000163CEC8A90070AD28E1B5BAF470B74F737FC4B27530B92889335F621966F849F4E5FB010F9225E959571E194DDE5591E307A3644269FC3BC2009DD23E08C50C72150974679CDAEAC7D990176C64265E3B600AD7FEE4F8B0C5A8E47BB476A60A7532CB3C3C0A6253EF120089909BCFA70DB177F037030A; "
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Referer': 'https://www.wegame.com.cn/helper/lol/record/profile.html',
            'Cookie': self.cookie
        }
        self.region_information = [
            [1, '艾欧尼亚', "HN1"],
            [15, "暗影岛", "HN11"]
        ]
        self.openid = []

    def run(self):
        while True:
            pass

    def get_summoner(self):
        self.__get_openid(1, '艾欧尼亚')

    def __get_openid(self, names, region):
        region = self.__set_region(region)

        '''
        for name in names:
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
                    openid = i["openid"]
                    break
        '''

    def __get_info(self):
        pass

    def __set_region(self, region):
        for i in self.region_information:
            if region in i:
                region = i
                break
        if region not in self.region_information:
            raise Exception(f"大区不存在:{region}")
        else:
            return region[0]
