import time

from GetSummonerMatch import GetSummonerMatch
from Lcu import LcuRequest

lcu = LcuRequest()
# /lol-match-history/v1/products/lol/21e6f38d-4f11-5c48-856d-2de3a5fad6b7/matches?begIndex=0&endIndex=20
# f'/lol-collections/v1/inventories/51e24697-8247-5f11-8fc3-1fa6630bcd3b/champion-mastery'

# https://127.0.0.1:6914/lol-summoner/v1/summoners?name=%E5%8D%B7%E5%8D%B7%E6%AF%9B%E6%80%AA
# 单向的爱要戒掉
#/lol-ranked/v1/ranked-stats/
# c=lcu.getdata(f"/lol-match-history/v1/products/lol/{ppuid}/matches?begIndex=0&endIndex=20").json()

#d=lcu.getdata("/lol-ranked/v1/eos-notifications").text
#print(d)

math = GetSummonerMatch()
print(time.ctime())
math.get_match(['卷卷毛怪', '我家AD是麻瓜','我在拉扯o','lXB丶神情'])

math.wait()
print(time.ctime())