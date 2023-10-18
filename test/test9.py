from Lcu import LcuRequest

lcu = LcuRequest()
'''
for i in range(10):
    lcu.getdata('/lol-lobby/v1/lobby/custom/switch-teams','post',None ,{'team': 'two'})
    lcu.getdata('/lol-lobby/v1/lobby/custom/switch-teams', 'post', None, {'team': 'one'})
'''
id = 'ap~05b167a6b3310e8f0345616c584e9679d3fb8066'
url = f'/lol-chat/v1/conversations/{id}/messages'

rp = lcu.getdata('/lol-chat/v1/conversations')

lcu.getdata(url, 'post', None, {'team': 'one'})
print(lcu.pw)
