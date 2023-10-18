from Lcu import LcuRequest
#Qt.WindowTransparentForInput
lcu = LcuRequest('F:\\英雄联盟-\\LeagueClient')

res = lcu.getdata(f'/lol-chat/v1/conversations').json()

print(res)