import json

import urllib3
from requests import request

urllib3.disable_warnings()


def getName_newApi(name, region, cookie):
    region_information = {
        "艾欧尼亚": 1,
        "暗影岛": 15,
    }

    if region not in region_information:
        return "大区不存在:" + region
    else:
        region = region_information[region]
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Referer': 'https://www.wegame.com.cn/helper/lol/record/profile.html',
        'Cookie': cookie}
    lastname = {name}
    uuid = ""
    res = request('post',
                  "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/SearchPlayer",
                  #/GetBattleList
                  headers=headers,
                  data=json.dumps({
                      "nickname": name, "from_src": "lol_helper"
                  }),
                  verify=False
                  ).json()

 #   print(res)

    for i in list(res["players"]):
        if i["area"] == region:
            uuid = i["openid"]
            break
  #  print(uuid)
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
    #print(res)
    # print(len(list(res['snapshots'])))
    for i in list(res['snapshots']):
        if i["player_name"] != '':
            lastname.add(i["player_name"])
    return lastname


def getName_oldApi(name, region, cookie):
    pass


def get_(names):
    qqs = []
    for i in names:
        res = request("get",
                      "https://zy.xywlapi.cc/lolname?name=" + i,
                      verify=False
                      ).json()

        print(res)
    return qqs


'''
    res1 = request("get",
                   "https://zy.xywlapi.cc/qqcx?qq=779330785",
                   verify=False
                   )

'''

wgcookie = "pgv_pvid=1595395908; ts_uid=1211749850; PTTuserFirstTime=1656201600000; weekloop=0-27-28-29; " \
           "isHostDate=19188; puin=3036346407; pt2gguin=o03036346407; uin=o03036346407; tgp_id=250478907; geoid=45; " \
           "lcid=2052; tgp_env=online; tgp_user_type=0; colorMode=1; " \
           "pkey" \
           "=000162D117F500707E577507233AD202CC049E39295A101FD29F43265C1B079FE309F9327386689C2848D6F8B5C929DAB5AD73308DF52482F2BEF86E2E766B137EBAF7CD6890994E17808CCD09A823F6F05F30CE587267E8B73C2F4BF0E925B38FE64ABDB20C3A94DFDD1F0F7AF8AFB18AE50D798EEC6870; tgp_ticket=0E24D067BC54B031A1699F1A4D3D74DA1480ED7DA7FCF4FCDC5E95E76B2575FDE7FF8B4EE4C33A1166FBEAC758D1403C012A5BB5B5C93CB92B7E3508787131142D10AB762A71ADD8EA05A141A73128285F52B497E066EF454CFFBD1437CF5EA060EB273D2F852E1FA9A59B7D5031D5A587352ED0967832E301E966C6DC525CC0; ssr=0; colorMode=1; BGTheme=[object Object]; pgv_info=ssid=s1355991640; language=zh_CN; tgp_biz_ticket=010000000000000000E96CB543F284C2EA146DA547EFFB7187CFC26403A96A8CB1B79BD63591412CC5088E282302D30679ECDD47D92567D3BBD9880519AABD2E34A8D863A8CBC481EE; region=CN; ts_last=www.wegame.com.cn/helper/lol/search/index.html "

print("曾有ID:", getName_newApi("94逍遥", "暗影岛", wgcookie))
#print("曾有ID:", getName_newApi("他与她和她的猫", "暗影岛", wgcookie))

# print(get_(get_lol_lastname("结婚了有外遇", "艾欧尼亚", wgcookie)))
# i = 'fdj13'
#L5012827086932396361","offset":0,"limit":40,"