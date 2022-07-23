# https://101.qq.com/#/hero-detail?heroid=350&tab=overview&lane=all&datatype=5v5&hero2_id=115
import json

import urllib3
from requests import request
urllib3.disable_warnings()

res = request("get", "https://101.qq.com/#/hero-detail?heroid=350&tab=overview&lane=all&datatype=5v5&hero2_id=115", verify=False )
print(res.text)
