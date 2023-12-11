import json
import os
import random
import sys
import time
from datetime import date, timedelta

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QApplication, QCompleter, QGraphicsDropShadowEffect, QSystemTrayIcon, QAction, QMenu, QMessageBox
from pypinyin import lazy_pinyin
import subprocess
import lolapiUI
from GameInfo import Info

from Lcu import LcuRequest, LcuThread
from RoundedWindow import RoundedWindow
from Summoner import SummonerUIRect

from setting import Ui_Dialog as uf


def set_state(_str):
    ui_home.state.setText(f"{_str}")
    ui_home.dial.setValue(ui_home.dial.value() + 5)


def auto_accept(state):
    if state == 0:
        qthread.accept_flag = False
    else:
        qthread.accept_flag = True


def choose_hero(state):
    if state == 0:
        ui_home.herolist.setEnabled(False)

    else:
        ui_home.herolist.setEnabled(True)
        qthread.hero_choose = ui_home.herolist.currentData()


def grab_hero():
    qthread.hero_choose = ui_home.herolist.currentData()


def load_user_data():
    global user
    user = lcu.getdata('/lol-summoner/v1/current-summoner').json()
    print(lcu.getdata('/lol-summoner/v1/current-summoner').text)
    ui_home.name.setText(user['internalName'])
    ui_home.profile.setPixmap(QPixmap(QImage.fromData(
        lcu.getdata('/lol-game-data/assets/v1/profile-icons/' + str(user['profileIconId']) + '.jpg').content)))


def summoner_init(data: dict):
    """
    :param data: {ppuid:floor}
    :return:
    """
    global summoner
    summoner = {}
    for ppuid, floor in data.items():
        summoner[ppuid] = {"UI": summoner_rect.bind_ui(floor)}
    summoner_rect.start()


def set_summoner_info(ppuid: str, data: dict):
    summoner[ppuid].update(data)
    wins = data["wins"]
    lost = data["lost"]
    summoner[ppuid]["UI"].recently.setText(f'近{wins + lost}场:')
    summoner[ppuid]["UI"].recently_worl.setText(f'{wins}胜{lost}负{wins / (wins + lost) * 100:.0f}%')
    summoner[ppuid]["UI"].recently_state.setText(f'{data["state"]}')
    summoner[ppuid]["UI"].rank.setText(f'{data["tier"]}')
    summoner[ppuid]["UI"].auto_size()
    summoner[ppuid]["UI"].show()


def set_summoner_hero(ppuid, hero_id: int):
    if 'hero_collections' in summoner[ppuid]:
        hero_no = summoner[ppuid]['hero_collections'].get(hero_id, {'championPoints_no': '无'})[
            'championPoints_no']
        hero_proficiency = summoner[ppuid]['hero_collections'].get(hero_id, {'championPoints': '0'})[
            'championPoints']
        hero_worl = summoner[ppuid]['hero_worl'].get(hero_id, {})
        wins = hero_worl.get("wins", 0)
        lost = hero_worl.get("lost", 0)
        # hero_worl = hero_worl if (wins + lost) == 0 else False

        hero_worl = f'{wins}胜{lost}负{wins / (wins + lost) * 100:.0f}%' if hero_worl else '无记录'

        summoner[ppuid]["UI"].hero_no.setText(f"{hero_no}")
        summoner[ppuid]["UI"].hero_proficiency.setText(f"{hero_proficiency}")
        summoner[ppuid]["UI"].hero_worl.setText(f"{hero_worl}")
        summoner[ppuid]["UI"].auto_size()


def set_summoner_hide():
    summoner_rect.init()


def ui_init():
    ui_home.name.setText("召唤师")
    ui_home.profile.clear()


def create_tray_icon():
    menu = QMenu()
    tray_icon = QSystemTrayIcon(main_window)
    tray_icon.setIcon(QIcon(r"C:\Users\lnori\Desktop\q.png"))

    ARestore = QAction('显示界面', main_window)
    ARestore.triggered.connect(lambda: main_window.showNormal())

    AQuit = QAction('退出', main_window)
    AQuit.triggered.connect(lambda: QCoreApplication.instance().quit())

    AMatch = QAction('战绩查询', main_window)
    AMatch.triggered.connect(lambda: QMessageBox.critical(main_window, ':(', '暂未实现'))
    AToolbox = QAction('工具箱', main_window)
    AToolbox.triggered.connect(lambda: QMessageBox.critical(main_window, ':(', '暂未实现'))
    # 先添加的在上面
    menu.addAction(ARestore)
    menu.addAction(AMatch)
    menu.addAction(AToolbox)
    menu.addAction(AQuit)
    tray_icon.setContextMenu(menu)
    tray_icon.show()


#
def start_game(mode):
    # app_arguments = ["--arg1", "value1", "--arg2", "value2"]
    mf_m.show()
    mf_m.setModal(True)
  #  mf_m.setModal(True)
 #   mf_m.activateWindow()
 #   QMessageBox.about(main_window, ':(', '没有找到路径,请手动启动吧！')


# subprocess.Popen(r"C:\Users\lnori\Desktop\nuitka.exe")


def start():
    ##########################################################
    global hero
    hero = Info().hero_id
    ui_home.dial.setWrapping(True)  # 设置转盘转完一圈后没有间隙
    main_window.setWindowTitle(' LOLHlp')
    create_tray_icon()
    ui_init()
    '''
    ui_home.herolist.clear()
    for k, v in sorted({hero[k]['title']: k for k in hero}.items(), key=lambda x: lazy_pinyin(x)):
        ui_home.herolist.addItem(k, v)
    completer = QCompleter(sorted([hero[k]['title'] for k in hero], key=lambda x: lazy_pinyin(x)))
    completer.setFilterMode(Qt.MatchContains)
    ui_home.herolist.setCompleter(completer)
    '''
    ##########################################################
    effect = QGraphicsDropShadowEffect()
    effect.setBlurRadius(10)  # 范围
    effect.setOffset(0, 0)  # 横纵,偏移量
    effect.setColor(Qt.black)  # 颜色
    ui_home.widget_1.setGraphicsEffect(effect)
    ##########################################################
    ui_home.match_query.clicked.connect(ui_init)
    ui_home.Button_X.clicked.connect(lambda: main_window.hide())
    ui_home.start.clicked.connect(start_game)
    #  ui_home.herolist.highlighted[str].connect(
    #     lambda s: ui_home.profile.setPixmap(hero[hero_name_id[s]]['icon']))
    #    ui_home.zdjs.stateChanged.connect(lambda s: auto_accept(s))
    #    ui_home.herolist.currentTextChanged.connect(lambda: grab_hero())
    #    ui_home.checkBox.stateChanged.connect(lambda s: choose_hero(s))

    # ui_home.hero.editTextChanged.connect(lambda s:print(s))
    # ui_home.herolist.currentIndexChanged.connect(lambda s: print(s))
    # ui_home.help.clicked.connect(test1)
    # ui_home.pushButton_7.clicked.connect(test2)
    ############################################################

    qthread.set_text.connect(set_state)
    qthread.load_user_data.connect(load_user_data)  # 载入
    qthread.window_enable.connect(lambda b: main_window.setEnabled(b))
    ##########################################################
    qthread.summoner_info.connect(set_summoner_info)
    qthread.summoner_hero.connect(set_summoner_hero)
    qthread.summoner_hide.connect(set_summoner_hide)
    qthread.summoner_init.connect(summoner_init)
    ###############################################################
    qthread.start()
    main_window.show()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QDialog
    app = QApplication(sys.argv)
    hero = {}
    user = {}
    summoner = {}

    lcu = LcuRequest()
    qthread = LcuThread(lcu)
    summoner_rect = SummonerUIRect()
    ui_home = lolapiUI.Ui_Frame()


    ''' 
    #UI美化,最后会用到
    
    
    
    
    Frame.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) 置顶

    '''
    main_window = RoundedWindow()
    ui_home.setupUi(main_window)
    # test
    mh = uf()
    mf_m = QDialog(main_window)
    mh.setupUi(mf_m)
    ui_home.widget_1.show()

    start()
    app.exec_()  # 开始
