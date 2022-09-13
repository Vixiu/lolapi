import asyncio
import json, random, sys

import aiohttp
import qdarktheme
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QCompleter
from pypinyin import lazy_pinyin

import lolapi

from FuWen import FuWen, GetData

from Lcu import LcuRequest, LcuThread


def add_text(_str):
    """
    :param _str: 内容
    :return:
    """
    ui_home.Gongao.append("<font color='{color}' size='4'>".format(color=randomcolor()) + _str + "<font>")


def set_state(_str, color='#000000'):
    ui_home.state.setText("<font color='{color}' size='4'>".format(color=color) + _str + "<font>")
    _ = ui_home.dial.value()
    if _ >= 100:
        _ = -10
    ui_home.dial.setValue(_ + 5)


def randomcolor():
    color_arr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += color_arr[random.randint(0, 14)]
    return "#" + color


def auto_accept(state):
    if state == 0:
        qthread.accept_flag = False
        ui_home.Gongao.append("<font color='{color}'>".format(color=randomcolor()) + '自动接受>>>已关闭' + "<font>")
    else:
        qthread.accept_flag = True
        ui_home.Gongao.append("<font color='{color}'>".format(color=randomcolor()) + '自动接受>>>已开启' + "<font>")


def choose_hero(state):
    if state == 0:
        qthread.choice_flag = False
        ui_home.Gongao.append("<font color='{color}'>".format(color=randomcolor()) + '秒抢>>>已关闭' + "<font>")
    else:

        qthread.hero_choose = hero_name_id[ui_home.herolist.currentText()]
        ui_home.Gongao.append(
            "<font color='{color}'>".format(color=randomcolor()) + '秒抢>>>' + ui_home.herolist.currentText() + "<font>")


def grab_hero(sate):
    if qthread.hero_choose > -1:
        qthread.hero_choose = hero[sate]['id']
        ui_home.Gongao.append("<font color='{color}'>".format(color=randomcolor()) + '秒抢>>>' + sate + "<font>")
    ui_home.profile.setPixmap(avatar_round(user))


def avatar_round(_user):
    pixmapa = QPixmap(QImage.fromData(
        lcu.getdata('/lol-game-data/assets/v1/profile-icons/' + str(_user['profileIconId']) + '.jpg').content))
    pixmap = QPixmap(360, 360)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)  # 一个是平滑，一个是缩放保持比例
    path = QPainterPath()
    path.addEllipse(0, 0, 360, 360)  # 绘制椭圆
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, 360, 360, pixmapa)
    painter.end()
    return pixmap


def load_data():
    global user, hero, hero_name_id
    # 获取用户信息
    user = lcu.getdata('/lol-summoner/v1/current-summoner').json()
    # 设置用户头像 名字
    ui_home.name.setText(user['internalName'])
    ui_home.profile.setPixmap(avatar_round(user))  # 圆形头像
    # 获取英雄信息
    # /lol-champions/v1/owned-champions-minimal

    for i in lcu.getdata('/lol-game-data/assets/v1/champion-summary.json').json()[1:]:
        hero[str(i['id'])] = {
            "squarePortraitPath": i['squarePortraitPath'],
            'name': i['name'],
        }
        hero_name_id[i['name']] = str(i['id'])
    # 下拉列表内添加数据，并键入提示
    ui_home.herolist.clear()
    ui_home.herolist.addItems(sorted(hero_name_id.keys(), key=lambda x: lazy_pinyin(x)))  # 列表内添加英雄
    completer = QCompleter(hero_name_id.keys())
    completer.setFilterMode(Qt.MatchContains)
    ui_home.herolist.setCompleter(completer)
    # 加载符文数据
    perk_id = {}
    for _ in lcu.getdata('/lol-perks/v1/perks').json():
        _ = dict(_)
        perk_id[str(_['id'])] = {
            'iconPath': _['iconPath']
        }

    for _ in lcu.getdata('/lol-perks/v1/styles').json():
        for j in _['slots']:
            for k in j['perks']:
                fw.rune_data[str(k)] = {
                    'id': _['id'],
                    'defaultSubStyle': _['defaultSubStyle']

                }
    # 得到要处理的 图标数据 网络数据json-----------------------
    for _ in hero:
        fw.hero_data[_] = fw.initialize_hero_data()
    data = {
        '符文-图标': {
            'lcu': lcu,
            'data': {_: perk_id[_].get('iconPath') for _ in fw.rune_data},
            'faction': save_rune_icon
        },
        '英雄-符文': {
            'lcu': None,
            'data': {_: f'https://lol.qq.com/act/lbp/common/guides/champDetail/champDetail_{_}.js' for _ in hero},
            'faction': save_hero_rune
        },
        '英雄-头像': {
            'lcu': lcu,
            'data': {_: hero[_].get('squarePortraitPath') for _ in hero},
            'faction': save_hero_icon
        },
        '英雄-排名': {
            "lcu": None,
            'data': {f'{_}-{lane}-{tier[1]}': f'https://x1-6833.native.qq.com/x1/6833/1061021&3af49f?championid=666&lane={lane}&ijob=all&gamequeueconfigid={_}&tier={tier[0]}' for _ in ['440', '420']
                     for lane in ['top', 'mid', 'jungle', 'support', 'bottom'] for tier in
                     [('0', 'challenger'), ('5', 'grandmaster'), ('6', 'master'), ('10', 'diamond'), ('20', 'platinum'), ('30', 'gold'), ('40', 'silver'), ('50', 'bronze'), ('80', 'iron'), ]},
            'faction': save_hero_ranking
        },
        '英雄-位置': {
            "lcu": None,
            'data': {'-': 'https://lol.qq.com/act/lbp/common/guides/guideschampion_position.js'},
            'faction': save_hero_lane
        }
    }

    # 多线程处理,后续可能改为多进程处理

    for _ in data:
        a = GetData(data[_]['data'], _, data[_]['lcu'])
        a.start()
        a.data.connect(data[_]['faction'])
        a.add_text.connect(add_text)
        a.set_sata.connect(set_state)
        qthread.loading_thread.append(a)
    qthread.wake()


def set_hero(hero_id, lane, queues):
    if hero_id != fw.hero_id:
        print(hero_id, lane, queues)
        fw.set_hero(hero_id, hero[hero_id]['name'], hero[hero_id]['squarePortraitPath'], queues, lane)


def set_show(bl):
    if bl:
        fw.show()
    else:
        fw.hide()


def start():
    main_window = QMainWindow()
    ui_home.setupUi(main_window)
    main_window.show()
    ##########################################################
    ui_home.herolist.highlighted[str].connect(
        lambda s: ui_home.profile.setPixmap(hero[hero_name_id[s]]['icon']))
    ui_home.zdjs.stateChanged.connect(lambda s: auto_accept(s))
    ui_home.herolist.activated[str].connect(lambda s: grab_hero(s))

    ui_home.checkBox.stateChanged.connect(lambda s: choose_hero(s))

    # ui_home.hero.editTextChanged.connect(lambda s:print(s))
    #  ui_home.herolist.currentIndexChanged.connect(lambda s: print(s))

    ui_home.help.clicked.connect(test1)
    # ui_home.pushButton_7.clicked.connect(test2)
    ###############################################################
    qthread.start()
    qthread.set_fuwen_hero.connect(set_hero)
    qthread.add_text.connect(add_text)
    qthread.set_text.connect(set_state)
    qthread.gameLoad.connect(load_data)  # 载入
    qthread.set_fuwen_show.connect(set_show)
    qthread.window_enable.connect(lambda b: main_window.setEnabled(b))
    ###############################################################


def test1():
    key = '72'
    # key = random.choice(list(hero.keys()))
    # print(fw.hero_data[key])
    print(hero[key]['name'], key)
    fw.set_hero(key, hero[key]['name'], hero[key]['squarePortraitPath'], '440')


def save_hero_rune(hero_id, data):
    """
    :param hero_id: 英雄id
    :param data:

    :return:
    """
    # 根据官网,符文数据共五组，每组里取前俩个
    data = json.loads(data[data.index('{'):data.rindex('}') + 1])
    rune_data = {}
    for lane in data['list']['championLane']:
        if 'perkdetail' not in data['list']['championLane'][lane]:
            continue
        perk_detail = json.loads(data['list']['championLane'][lane]['perkdetail'])
        _ls = []
        for i in ['1', '2', '3', '4', '5']:
            for j in ['1', '2']:
                if i not in perk_detail or j not in perk_detail[i]:
                    continue
                _ = {}
                win_rate = str(perk_detail[i][j]['winrate']).ljust(4, '0')
                show_rate = str(perk_detail[i][j]['showrate']).ljust(4, '0')
                _['rune'] = perk_detail[i][j]['perk'].split('&')
                _['win_rate'] = f'胜率:{win_rate[0:2]}.{win_rate[2:]}%'
                _['show_rate'] = f'使用率:{show_rate[0:2]}.{show_rate[2:]}%'
                _ls.append(_)
        rune_data[lane] = _ls

    fw.hero_data[hero_id]['rune_data'] = rune_data

    '''
    fw.hero_data[hero_id] = {
        # 'best_lane': [] if data['list']['championFight'] is None else [zh_ch[lane] for lane in data['list']['championFight'].keys()],
        'rune_data': rune_data
    }
    '''
    set_state(f'加载英雄-符文-->{hero[hero_id]["name"]}')


def save_hero_lane(_, data):
    data = json.loads(data[data.index('{'):data.rindex('}') + 1])['list']
    for _ in data:
        fw.hero_data[_]['best_lane'] = list(data[_].keys())


def save_hero_ranking(ids, data):
    data = json.loads(data)
    ids = ids.split('-')

    for _ in json.loads(data['data']['result'])['championdetails'].split('#'):
        _ = _.split('_', 6)[0:6]
        hero_id = _.pop(1)
        if ids[1] in fw.hero_data[hero_id]['ranging'][ids[0]]:
            fw.hero_data[hero_id]['ranging'][ids[0]][ids[1]][ids[2]] = _
        else:

            fw.hero_data[hero_id]['ranging'][ids[0]][ids[1]] = {ids[2]: _}

    set_state(f'加载英雄-排名-->{ids[1]}')


def save_hero_icon(hero_id, data):
    hero[hero_id]['icon'] = data
    set_state(f'加载英雄-图标-->{hero[hero_id]["name"]}')


def save_rune_icon(perk_id, data):
    """

    :param perk_id: 符文id
    :param data: 图片数据(QPixmap)
    :return:
    """
    fw.rune_data[perk_id]['icon'] = data
    set_state(f'加载符文-图标-->{perk_id}')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    hero = {}
    user = {}
    hero_name_id = {}

    LOL_PATH = 'F:\\1\\英雄联盟-\\LeagueClient'
    lcu = LcuRequest(LOL_PATH)
    qthread = LcuThread(lcu)
    ui_home = lolapi.Ui_Frame()
    fw = FuWen(lcu)
    hero_select = ''

    ########Ui暂时性适配##################
    # Frame.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) 置顶
    ###########后续直接移入py文件###################

    app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    start()  # 初始化数据
    app.exec_()  # 开始
    qthread.stop = False  # 线程退出
