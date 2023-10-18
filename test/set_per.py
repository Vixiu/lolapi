import json
from base64 import b64encode
from psutil import process_iter
from urllib3 import disable_warnings
from requests import request


class LcuRequest:
    disable_warnings()

    def __init__(self):
        self.is_process = False
        self.lcu_args = self.get_lcu_args()
        self.port, self.pw = self.lcu_args.get('app-port', '0000'), self.lcu_args.get("remoting-auth-token", 'None')
        self.url = 'https://127.0.0.1:' + self.port
        self.headers = {
            "User-Agent": "LeagueOfLegendsClient",
            'Authorization': 'Basic ' + b64encode(('riot' + ':' + self.pw).encode()).decode(),

        }

    def get_lcu_args(self):

        return {
            line[2:].split('=', 1)[0]: line[2:].split('=', 1)[1]
            for line in self.find_lcu_cmdline()
            if '=' in line
        }

    def getdata(self, path, method='get', headers=None, data=None):
        """
        :param path:路径
        :param method:方式,默认get
        :param headers:参数
        :param data:内容body
        :return:数据
        """
        if headers is None:
            headers = {}
        headers.update(self.headers)
        return request(method, self.url + path, headers=self.headers, data=json.dumps(data), verify=False)

    def find_lcu_cmdline(self):
        for prs in process_iter():
            if prs.name() in ['LeagueClientUx', 'LeagueClientUx.exe']:
                self.is_process = True
                return prs.cmdline()
        self.is_process = False
        return []

    def reset(self):
        self.__init__()


def test(perk, title):
    res = lcu.getdata('/lol-perks/v1/currentpage').json()
    res = res.get('id', 0)
    lcu.getdata(f'/lol-perks/v1/pages/{res}', 'DELETE')
    lcu.getdata('/lol-perks/v1/pages', 'post', None, {
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


def out_perks():
    res = lcu.getdata('/lol-perks/v1/styles').json()
    for _ in res:
        print('\t', '######', _['defaultPageName'], '######')
        for j in _['slots'][:4]:
            for k in j['perks']:
                print(rune_data[k]['name'], k, '\t', end='')
            print()
    print('\t', '######', '通用', '######')
    for k in res[0]['slots'][4:]:
        for _ in k['perks']:
            print(rune_data[_]['name'], _, '\t', end='')
        print()


if __name__ == '__main__':

    lcu = LcuRequest()
    rune_data = {}
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
    try:
        for _ in lcu.getdata('/lol-perks/v1/styles').json():
            for j in _['slots']:
                for k in j['perks']:
                    rune_data[k] = {
                        'primaryStyleId': _['id'],
                    }
        for _ in lcu.getdata('/lol-perks/v1/perks').json():
            rune_data.get(_['id'], {})['name'] = _['name']
    except:
        print('运行失败:(,或许客户端没有打开')
        input()
        exit()
    while True:
        print('请输入开头数字,并按回车:')
        print('1:一键心之钢天赋')
        print('2:自定义天赋')
        print('输入其他任意字符 -退出')
        print('Ps:客户端只要打开就可以使用,在大厅内可在 藏品->符文 查看效果, (不能点天赋的小号也可用) By:青烟')
        it = input()
        if it == '2':
            out_perks()
            print('说明:主系4个+副系2个+通用3个,共9个,中间用逗号隔开')
            print('示例: 8437,8463,8444,8451,8139,8134,5005,5008,5001')
            print('请输入:')

            perks = input()
            try:
                perks = perks.replace('，', ',').split(',')
                test({
                    'zhuxi': [int(i) for i in perks[:4]],
                    'fuxi': [int(i) for i in perks[4:]]
                },
                    '--自定义--'
                )
                print('完成,请自行检查')
            except:
                print('输入错误')
        elif it == '1':
            test(gang, '--打钢--')
            print('心之钢天赋 配置完成 ！')
        else:
            break
        print()
