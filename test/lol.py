import json

import requests
from urllib3 import disable_warnings

disable_warnings()

b = "eyJraWQiOiJzMSIsImFsZyI6IlJTNTEyIn0.eyJzY3AiOiJMT0wiLCJzdWIiOiIxNWI2YTI5Ni1iMWI0LTU3YzQtODdkYS0xODI0Mzc5ZGRlMzciLCJwcm9kdWN0IjoiTE9MIiwicGFydGlkIjoiMTMzMjU3NTk3OSIsImxpZCI6bnVsbCwiY25hbWUiOiJsY3UiLCJoYmMiOiJuYW4iLCJhY3RpZCI6MjkzNTA5NjUwOSwiaXNzIjoiaHR0cHM6XC9cL3Nlc3Npb24tandrcy0xMjUzMjk4MTg1LmNvcy5hcC1zaGFuZ2hhaS5teXFjbG91ZC5jb20iLCJyaWQiOiJaMS1VcENtUVZpRSIsInJmYSI6MTY5MDQ3NDc4OSwic2lkIjoiNzQ4YTAyOWQtMmJiNS00MmY4LWExNDUtZTViMWJmNDFiZTM3IiwiYnlwYXNzIjpmYWxzZSwiZmVkZXJhdGVkX2lkZW50aXR5X3Byb3ZpZGVycyI6W10sInJlZyI6IkhOMTEiLCJkYXQiOnsiciI6IkhOMTEiLCJ1IjoyOTM1MDk2NTA5fSwicmZvIjozNDgsImV4cCI6MTY5MDQ3NTA0MSwiaWF0IjoxNjkwNDc0NDQxLCJqdGkiOiJhYzdhZDZhMi0yMzJkLTQzMDUtOTMwMi0xZTRmOTFkNDE3NDkiLCJjaWQiOiJsc3MiLCJzaXQiOjE2OTA0NzM3OTB9.jt_-D0K1mhknJQaFKk73fCswRE6tn2xvIZ45FI-BDTCJ3t92utbUN73KAD12M-FExZe3sYRm2Rf6mGTrMKzS7Zi2XIN9-aoYD3jI5EdAIkdV19kTFlVd7CIyAqPS7Jenw5JyiJ4x56g-aGY7A2ycQXihC5E-2b-nnRm6yVb-Y_YBAX-D4tSZj2ZTcvnTWCnkC_1c63ZQ6VbvKIgMoKpYydjH6cIUCRIPjTCPTRE4E_-Kl9YNN_SvyvWZyCe6fQe6yfgTTXt6fe2zFEv2_TEGvvfRNXXNSnT7AkPUuJluilwN3qCRJ-OIqJPP48el5veEbCrQbEk81v0ub3-JB_7mUA"
url = "https://hn11-cloud-sgp.lol.qq.com:21019/marketing-preferences/public/partition/sfm2023/player/15b6a296-b1b4-57c4-87da-1824379dde37"
hd = {
    "Content-type": "application/json",
    "Host": "hn11-cloud-sgp.lol.qq.com:21019",
    "user-agent": "LeagueOfLegendsClient/13.14.520.6878 (rcp-be-lol-challenges)",
    "Authorization": f"Bearer {b}"}
n = 19
data1 = {
    "progress": str(n)
}
data2 = {
    "numNodesUnlocked": str(n+1),
}
data3={
    "loadout_active_e": "3",
    "loadout_active_q": "2",
    "loadout_active_r": "1",
    "loadout_active_w": "1",
}
res = requests.request(method='post', url=url, headers=hd, data=json.dumps(data1), verify=False)
print(res.text)
res = requests.request(method='post', url=url, headers=hd, data=json.dumps(data2), verify=False)
print(res.text)
