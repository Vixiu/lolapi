import json
import random
import sys
from datetime import date, timedelta

import win32gui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QCompleter, QGraphicsDropShadowEffect
from pypinyin import lazy_pinyin

import lolapiUI

from Lcu import LcuRequest, LcuThread
from Widget import RoundedWindow
from info_data import Info
from se_ui import Ui_Form


def add_text(text):
    """
    :param text: 内容
    :return:
    """
    ui_home.Gongao.append("<font color='{color}' size='4'>".format(color=randomcolor()) + text + "<font>")


def set_state(_str, color='#000000'):
    ui_home.state.setText("<font color='{color}' size='4'>".format(color=color) + _str + "<font>")
    _ = ui_home.dial.value()
    if _ >= 100:
        _ = -25
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
        ui_home.herolist.setEnabled(False)
        ui_home.Gongao.append("<font color='{color}'>".format(color=randomcolor()) + '秒抢>>>已关闭' + "<font>")
    else:
        ui_home.herolist.setEnabled(True)
        qthread.hero_choose = ui_home.herolist.currentData()
        ui_home.Gongao.append("<font color='{color}'>".format(
            color=randomcolor()) + '秒抢>>>' + ui_home.herolist.currentText() + "<font>")


def grab_hero():
    qthread.hero_choose = ui_home.herolist.currentData()
    ui_home.Gongao.append(
        "<font color='{color}'>".format(color=randomcolor()) + '秒抢>>>' + ui_home.herolist.currentText() + "<font>")


def load_user_data():
    global user
    print(1)
    user = lcu.getdata('/lol-summoner/v1/current-summoner').json()
    ui_home.name.setText(user['internalName'])
    ui_home.profile.setPixmap(QPixmap(QImage.fromData(
        lcu.getdata('/lol-game-data/assets/v1/profile-icons/' + str(user['profileIconId']) + '.jpg').content)))


def set_summoner_info(floor, info):
    summoner_floor = {
        0: summoner_1,
        1: summoner_2,
        2: summoner_3,
        3: summoner_4,
        4: summoner_5,
        5: summoner_1,
        6: summoner_2,
        7: summoner_3,
        8: summoner_4,
        9: summoner_5

    }
    tier = {
        0: "王者",
        1: "钻石",
        2: "铂金",
        3: "黄金",
        4: "白银",
        5: "青铜",
        6: "大师",
        7: "宗师",
        8: "黑铁"
    }
    queue = {
        0: "I",
        1: "II",
        2: "III",
        3: "IV",
        4: "V",

    }
    global summoner
    summoner_floor[floor].show()
    summoner_floor[floor].total_sessions.setText(f'{info["battle_count"]["total_games"]}场')
    summoner_floor[floor].total_rate.setText(
        f'{int(info["battle_count"]["total_wins"] / info["battle_count"]["total_games"] * 100)}%')
    if info["season_list"][0]["tier"] == 255:
        summoner_floor[floor].total_rank.setText("无段位")
    else:
        summoner_floor[floor].total_rank.setText(
            f'{tier[info["season_list"][0]["tier"]]}'
            f'{"" if info["season_list"][0]["tier"] in [0, 6, 7] else queue[info["season_list"][0]["queue"]]}'
            f'{info["season_list"][0]["win_point"]}')
    summoner_floor[floor].recently_worl.setText(f'{info["record_count"]["wins"]}胜{info["record_count"]["lost"]}负')
    summoner_floor[floor].recently_rate.setText(
        f'{int(info["record_count"]["wins"] / (info["record_count"]["wins"] + info["record_count"]["lost"]) * 100)}%'
    )

    summoner[floor] = {
        "near_record": info['near_record'],
        "champion_list": info["champion_list"]
    }
    summoner_floor[floor].show()


def set_summoner_hero(floor, hero_id):
    try:
        summoner_floor = {
            0: summoner_1,
            1: summoner_2,
            2: summoner_3,
            3: summoner_4,
            4: summoner_5,
            5: summoner_1,
            6: summoner_2,
            7: summoner_3,
            8: summoner_4,
            9: summoner_5

        }

        global summoner
        #####
        if floor in summoner:
            total = summoner[floor]["champion_list"].get(hero_id, {}).get("total", 0)
            wins = summoner[floor]["champion_list"].get(hero_id, {}).get("wins", 0)
            if total == 0:
                summoner_floor[floor].hero_sessions.setText(f"暂无场次")
                summoner_floor[floor].hero_rate.setText("")

            else:
                summoner_floor[floor].hero_sessions.setText(f'{total}场')
                summoner_floor[floor].hero_rate.setText(
                    f"{int(wins / total * 100)}%"
                )
            if hero_id in summoner[floor].get("near_record", {}):
                summoner_floor[floor].hero_worl.setText(
                    f'{summoner[floor]["near_record"][hero_id]["wins"]}胜'
                    f'{summoner[floor]["near_record"][hero_id]["lost"]}负'
                )
            else:
                summoner_floor[floor].hero_worl.setText("无记录")
    except Exception as e:
        raise print(e)


def set_summoner_rect():
    width = 101
    rect = win32gui.GetWindowRect(win32gui.FindWindow(None, 'League of Legends'))
    s1_x = int(rect[0] + 0.1725 * (rect[2] - rect[0]))
    s1_y = int(rect[1] + 0.1311 * (rect[3] - rect[1]))
    # print(s1_x, s1_y)
    summoner_1.move(s1_x, s1_y)
    summoner_2.move(s1_x, s1_y + width)
    summoner_3.move(s1_x, s1_y + 2 * width)
    summoner_4.move(s1_x, s1_y + 3 * width)
    summoner_5.move(s1_x, s1_y + 4 * width)


def set_summoner_show():
    global summoner
    summoner = {}
    summoner_1.hide()
    summoner_2.hide()
    summoner_3.hide()
    summoner_4.hide()
    summoner_5.hide()


def start():
    ##########################################################
    global hero
    hero = Info().hero_id
    ui_home.herolist.clear()
    for k, v in sorted({hero[k]['title']: k for k in hero}.items(), key=lambda x: lazy_pinyin(x)):
        ui_home.herolist.addItem(k, v)
    completer = QCompleter(sorted([hero[k]['title'] for k in hero], key=lambda x: lazy_pinyin(x)))
    completer.setFilterMode(Qt.MatchContains)
    ui_home.herolist.setCompleter(completer)


    ##########################################################
    effect = QGraphicsDropShadowEffect()
    effect.setBlurRadius(10)  # 范围
    effect.setOffset(0, 0)  # 横纵,偏移量
    effect.setColor(Qt.black)  # 颜色
    ui_home.widget_1.setGraphicsEffect(effect)
    ##########################################################
    #  ui_home.herolist.highlighted[str].connect(
    #     lambda s: ui_home.profile.setPixmap(hero[hero_name_id[s]]['icon']))
    ui_home.zdjs.stateChanged.connect(lambda s: auto_accept(s))
    ui_home.herolist.currentTextChanged.connect(lambda: grab_hero())
    ui_home.checkBox.stateChanged.connect(lambda s: choose_hero(s))

    # ui_home.hero.editTextChanged.connect(lambda s:print(s))
    # ui_home.herolist.currentIndexChanged.connect(lambda s: print(s))
    # ui_home.help.clicked.connect(test1)
    # ui_home.pushButton_7.clicked.connect(test2)
    ############################################################

    qthread.add_text.connect(add_text)
    qthread.set_text.connect(set_state)
    qthread.load_user_data.connect(load_user_data)  # 载入
    qthread.window_enable.connect(lambda b: main_window.setEnabled(b))
    qthread.summoner_info.connect(set_summoner_info)
    qthread.summoner_hero.connect(set_summoner_hero)
    qthread.summoner_rect.connect(set_summoner_rect)
    qthread.summoner_show.connect(set_summoner_show)
    ###############################################################

    qthread.start()
    main_window.show()
    '''
    summoner_1.show()
    summoner_2.show()
    summoner_3.show()
    summoner_4.show()
    summoner_5.show()
    '''



if __name__ == '__main__':

    hero = {}
    user = {}
    app = QApplication(sys.argv)
    lcu = LcuRequest()
    qthread = LcuThread(lcu)
    ui_home = lolapiUI.Ui_Frame()
    summoner = {}
    '''
    #UI美化,最后会用到
    Frame.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) 置顶

    '''
    main_window = RoundedWindow()
    ui_home.setupUi(main_window)

    #############

    summoner_1 = Ui_Form()
    summoner_2 = Ui_Form()
    summoner_3 = Ui_Form()
    summoner_4 = Ui_Form()
    summoner_5 = Ui_Form()

    #############
    start()
    app.exec_()  # 开始
