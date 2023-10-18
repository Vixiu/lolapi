import json

from requests import request

url = 'https://lol.qq.com/act/lbp/common/guides/guideschampion_position.js'

url1 = 'https://x1-6833.native.qq.com/x1/6833/1061021&3af49f?championid=666'

s = 'https://lol.sw.game.qq.com/lol/lwdcommact/a20211015billboard/a20211015api/fight?dtstatdate=20220908&callback=getRankFightCallback&ts=2771181'

# game_queue_config_id = ['440', '420']
# lane = ['top', 'mid', 'jungle', 'support', 'bottom']
# tier = ['0', '5', '6', '10', '20', '30', '40', '50', '80']
print(

    # ['https://x1-6833.native.qq.com/x1/6833/1061021&3af49f?championid=666&lane='+_+'&ijob=all' for _ in lane]
)

data = request('get', url).text
data = json.loads(data[data.index('{'):data.rindex('}') + 1])['list']
for _ in data:
    print(_, list(data[_].keys()))
