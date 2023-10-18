from lol_find import FindLolQP
# print(team_info['myTeam'][-1]['championId'] )

find = FindLolQP()

info = find.get_info(['优雅永不过时'], '暗影岛')
print(info)