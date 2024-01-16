from 弃用.GetSE import FindLolQP

find = FindLolQP()

info = find.get_info([''], '暗影岛')
print(str(info).replace("'", '').replace('{', '').replace('}', '}'))
