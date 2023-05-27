from Lcu import LcuRequest


def test(perk, title):
    res = lcu.getdata('/lol-perks/v1/currentpage').json()
    res = res.get('id', 0)
    lcu.getdata(f'/lol-perks/v1/pages/{res}', 'DELETE')
    res = lcu.getdata('/lol-perks/v1/pages', 'post', None, {
        "autoModifiedSelections": [],
        "current": True,
        "isActive": True,
        "isDeletable": True,
        "isEditable": True,
        "isValid": True,
        "lastModified": 0,
        "name": title,
        "order": 0,
        "primaryStyleId": rune_data[perk['zhuxi'][0]]['primaryStyleId'],
        "selectedPerkIds": perk['zhuxi'] + perk['fuxi'],
        "subStyleId": rune_data[perk['fuxi'][0]]['primaryStyleId']
    })
    print(res.text)


if __name__ == '__main__':
    lcu = LcuRequest()
    print(lcu.pw, lcu.port)
    rune_data = {}
    for _ in lcu.getdata('/lol-perks/v1/styles').json():
        for j in _['slots']:
            for k in j['perks']:
                rune_data[k] = {
                    'primaryStyleId': _['id'],
                }
    gang = {
        "zhuxi": [
            8437,
            8463,
            8444,
            8451

        ],
        "fuxi": [
            8139,
            8134,
            5005,
            5008,
            5001

        ],
    }
    test(gang, '--打刚--')
    input()
