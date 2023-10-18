from Lcu import LcuRequest

lcu = LcuRequest()

LobbyConfig = {
    'customGameLobby': {
        'configuration': {
            'gameMode': 'CHERRY',
            'gameMutator': '',
            'gameServerRegion': '',
            'mapId': 30,
            'mutators': {'id': 1},
            'spectatorPolicy': 'AllAllowed',
            'teamSize': 10,
            "maxLobbySize": 5,
            "maxTeamSize": 5,
        },
        'lobbyName': 'PRACTICETOOL',
        'lobbyPassword': ''
    },
    'isCustom': False,
    "queueId": 1700,

}
'''
res = lcu.getdata('/lol-lobby/v2/lobby/', 'post', data=LobbyConfig)
bot = {"championId": 16, "botDifficulty": "MEDIUM", "teamId": "200"}
res=lcu.getdata( '/lol-lobby/v1/lobby/custom/bots','POST', data=bot)
#res = lcu.getdata('/lol-lobby/v2/lobby/', 'get')
print(res.text)
'''
id=30
res = lcu.getdata('/lol-store/v1/catalog', 'get')

print(res.text)