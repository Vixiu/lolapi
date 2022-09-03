import json

from requests import request

hero_id = 133

res = request('get',
              f'https://lol.qq.com/act/lbp/common/guides/champDetail/champDetail_{str(hero_id)}.js').text
res = json.loads(res[res.index('{'):res.rindex('}') + 1])
# res = json.loads(res['list']['championLane']['support']['perkdetail'])['1']
res1 = res['list']
res = res['list']['championFight']
data = {}
if res is None:
    for i in res1['championLane']:
        if 'championid' in res1['championLane'][i]:
            data[i] = res1['championLane'][i]



else:
    for i in res.keys():
        res = res1['championLane'][i]
        data[i] = res
print(data.keys())





