import datetime
import os
import time

import requests

from Lcu import LcuRequest

lol_path = 'F:\\英雄联盟-\\LeagueClient'

lcu = LcuRequest(lol_path)


def CheckProc(name):
    ps = os.popen("C:/WINDOWS/system32/tasklist.exe", "r")
    pp = ps.readlines()
    ps.close()
    for i in pp:
        if name in i:
            return True
    return False


hd = {
    "body": "666",
    #  "fromId": "4127708294",
    #  "fromSummonerId": 4127708294,
    # "isHistorical": False,
    #  "timestamp": (datetime.datetime.now() - datetime.timedelta(hours=8)).isoformat("T", "milliseconds") + "Z",
    "type": "chat"
}
# celebration
# ban

# print(lcu.getdata("/lol-chat/v1/conversations").text)

print(lcu.getdata("/liveclientdata/activeplayerabilities").text)

print(lcu.getdata("/liveclientdata/activeplayerabilities").text)
# print(lcu.getdata("/lol-chat/v1/conversations/c1~83988016ba64badcdc154a8f80b58c6ece051a2d/messages","post",{},hd).text)
# print(lcu.getdata('/lol-chat/v1/blocked-players').text)
