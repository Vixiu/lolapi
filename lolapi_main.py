import json
import random
import sys
import time
from threading import Thread

import qdarkstyle
import qdarktheme
import qtmodern
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QCompleter
from pypinyin import lazy_pinyin
from requests import request
from win32api import Sleep
from qt_material import apply_stylesheet, list_themes
import lolapi
# from Fuwendemo import FuWen
from FuWen import FuWen, GetData

from Lcu import LcuRequest, LcuThread


def add_text(_str):
    """
    :param _str: 内容
    :return:
    """
    ui_home.Gongao.append("<font color='{color}' size='4'>".format(color=randomcolor()) + _str + "<font>")


def set_text(_str, color):
    ui_home.state.setText(_str)
    _ = ui_home.dial.value()
    if _ > 98:
        _ = 0

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
        qthread.hero_choose = hero[ui_home.herolist.currentText()]['id']
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
    user = lcu.getdata('/lol-summoner/v1/current-summoner').json()
    ui_home.name.setText(user['internalName'])
    ui_home.profile.setPixmap(avatar_round(user))  # 圆形头像

    for i in lcu.getdata('/lol-champions/v1/owned-champions-minimal').json():
        hero[str(i['id'])] = {
            "squarePortraitPath": i['squarePortraitPath'],
            'name': i['title'],
            'title': i['name']
        }
        hero_name_id[f"{i['name']}-{i['title']}"] = str(i['id'])

    ui_home.herolist.clear()

    ui_home.herolist.addItems(sorted(hero_name_id.keys(), key=lambda x: lazy_pinyin(x)))  # 列表内添加英雄

    completer = QCompleter(hero_name_id.keys())
    completer.setFilterMode(Qt.MatchContains)
    ui_home.herolist.setCompleter(completer)

    # ui_home.hero.completer('')
    load_hero_data()

    add_text('初始化完毕!')


def set_hero(name):
    if (name != fw.hero['name']) and (name != ''):
        print(name)
        fw.set_hero(hero[name])


def start():
    main_window = QMainWindow()
    ui_home.setupUi(main_window)
    main_window.show()
    ###############################################################
    ui_home.herolist.highlighted[str].connect(
        lambda s: ui_home.profile.setPixmap(
            QPixmap(QImage.fromData(lcu.getdata(hero[hero_name_id[s]]['squarePortraitPath']).content))))
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
    qthread.set_text.connect(set_text)
    qthread.gameLoad.connect(load_data)  # 载入
    qthread.window_enable.connect(lambda b: main_window.setEnabled(b))
    ###############################################################


def load_hero_data():
    global qthread_ls
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

    for _ in fw.rune_data:
        a = GetData(perk_id[_]['iconPath'], _, lcu)
        a.data.connect(save_rune_icon)
        a.start()
        qthread_ls.append(a)

    for _ in hero:
        a = GetData(f'https://lol.qq.com/act/lbp/common/guides/champDetail/champDetail_{_}.js', _)
        a.data.connect(save_hero_rune)
        a.start()
        qthread_ls.append(a)


def test1():
    key = random.choice(list(hero.keys()))
    fw.set_hero(key, hero[key]['name'], hero[key]['squarePortraitPath'])


def save_hero_rune(hero_id, data):
    """

    :param hero_id: 英雄id
    :param data: {
    rune_data:
       top:[{rune:[],win_rate:00.00%,show_rate:00.00%},]
    ,
    best_lane:['top',,,,]
    }
    :return:
    """
    # 根据官网,符文数据共五组，每组里取前俩个
    lane_ch = {
        'top': '上单',
        'mid': '中单',
        'jungle': '打野',
        'support': '辅助',
        'bottom': '下路',
    }
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
        rune_data[lane_ch[lane]] = _ls
    fw.hero_data[hero_id] = {
        # 'best_lane': [] if data['list']['championFight'] is None else [lane_ch[lane] for lane in data['list']['championFight'].keys()],
        'rune_data': rune_data
    }
    set_text(f'正在读取符文-->{hero_id}', 1)


def save_hero_lane(_, data):
    data = json.loads(data[data.index('{'):data.rindex('}') + 1])


def save_rune_icon(perk_id, data):
    """

    :param perk_id: 符文id
    :param data: 图片数据(QPixmap)
    :return:
    """
    fw.rune_data[perk_id]['icon'] = data


# Frame.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) 置顶
app = QApplication(sys.argv)
hero = {}
user = {}
hero_name_id = {}

LOL_PATH = 'F:\\1\\英雄联盟-\\LeagueClient'
lcu = LcuRequest(LOL_PATH)
qthread = LcuThread(lcu)
ui_home = lolapi.Ui_Frame()
qthread_ls = []
fw = FuWen(lcu)
hero_select = ''

########Ui暂时性适配##################


###########后续直接移入py文件###################


app.setStyleSheet(qdarktheme.load_stylesheet("light"))
start()  # 开始

app.exec_()  # 开始
qthread.stop = False  # 线程退出
