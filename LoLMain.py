import asyncio
import json
import os
import random
import sys
import time

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QApplication, QCompleter, QGraphicsDropShadowEffect, QSystemTrayIcon, QAction, QMenu, QMessageBox
from pypinyin import lazy_pinyin
import subprocess

from GameInfo import Info

from Lcu import lcu
from LoLMainQThread import LcuThread
from Summoner import SummonerUIRect

from UI import Toolbox, MainWindow


def set_state(_str):
    MainUI.state.setText(f"{_str}")
    MainUI.dial.setValue(MainUI.dial.value() + 5)


def load_data():
    global user, hero
    user = lcu.getdata('/lol-summoner/v1/current-summoner').json()
    print(lcu.getdata('/lol-summoner/v1/current-summoner').text)
    MainUI.name.setText(user['internalName'])
    MainUI.profile.setPixmap(QPixmap(QImage.fromData(lcu.getdata('/lol-game-data/assets/v1/profile-icons/' + str(user['profileIconId']) + '.jpg').content)))
    if not hero:
        hero = Info().hero_id
        set_hero_list()


def set_hero_list():
    ToolboxUI.grab_hero.clear()
    completer = QCompleter(sorted([hero[k]['title'] for k in hero], key=lambda x: lazy_pinyin(x)))
    completer.setFilterMode(Qt.MatchContains)
    for k, v in sorted({hero[k]['title']: k for k in hero}.items(), key=lambda x: lazy_pinyin(x)):
        ToolboxUI.grab_hero.addItem(k, v)
        ToolboxUI.ban_hero_1.addItem(k, v)
        ToolboxUI.ban_hero_2.addItem(k, v)
        ToolboxUI.ban_hero_3.addItem(k, v)
    ToolboxUI.grab_hero.setCompleter(completer)
    ToolboxUI.ban_hero_1.setCompleter(completer)
    ToolboxUI.ban_hero_2.setCompleter(completer)
    ToolboxUI.ban_hero_3.setCompleter(completer)


def summoner_init(data: dict):
    """
    :param data: {ppuid:floor}
    :return:
    """
    global summoner
    summoner = {}
    for ppuid, floor in data.items():
        summoner[ppuid] = {"UI_ui": summoner_rect.bind_ui(floor)}


def set_summoner_info(ppuid: str, data: dict):

    summoner[ppuid].update(data)
    wins = data["wins"]
    lost = data["lost"]
    summoner[ppuid]["UI_ui"].recently.setText(f'近{wins + lost}场:')
    summoner[ppuid]["UI_ui"].recently_worl.setText(f'{wins}胜{lost}负{wins / (wins + lost) * 100:.0f}%')
    summoner[ppuid]["UI_ui"].recently_state.setText(f'{data["state"]}')
    summoner[ppuid]["UI_ui"].rank.setText(f'{data["tier"]}')
    summoner[ppuid]["UI_ui"].auto_size()
    summoner[ppuid]["UI_ui"].show()


def set_summoner_hero(ppuid, hero_id: int):
    if ppuid in summoner and 'hero_collections' in summoner[ppuid]:
        hero_no = summoner[ppuid]['hero_collections'].get(hero_id, {'championPoints_no': '无'})[
            'championPoints_no']
        hero_proficiency = summoner[ppuid]['hero_collections'].get(hero_id, {'championPoints': '0'})[
            'championPoints']
        hero_worl = summoner[ppuid]['hero_worl'].get(hero_id, {})
        wins = hero_worl.get("wins", 0)
        lost = hero_worl.get("lost", 0)
        # hero_worl = hero_worl if (wins + lost) == 0 else False

        hero_worl = f'{wins}胜{lost}负{wins / (wins + lost) * 100:.0f}%' if hero_worl else '无记录'

        summoner[ppuid]["UI_ui"].hero_no.setText(f"{hero_no}")
        summoner[ppuid]["UI_ui"].hero_proficiency.setText(f"{hero_proficiency}")
        summoner[ppuid]["UI_ui"].hero_worl.setText(f"{hero_worl}")
        summoner[ppuid]["UI_ui"].auto_size()


def set_summoner_hide():
    summoner_rect.close()


def ui_init():
    MainUI.name.setText("召唤师")
    MainUI.profile.clear()


def create_tray_icon():
    menu = QMenu()
    tray_icon = QSystemTrayIcon(MainUI)
    tray_icon.setIcon(QIcon(r"C:\Users\lnori\Desktop\q.png"))

    ARestore = QAction('显示界面', MainUI)
    ARestore.triggered.connect(lambda: MainUI.show())

    AQuit = QAction('退出', MainUI)
    AQuit.triggered.connect(lambda: QCoreApplication.instance().quit())

    AMatchQuery = QAction('战绩查询', MainUI)
    AMatchQuery.triggered.connect(lambda: QMessageBox.critical(MainUI, ':(', '暂未实现'))

    AToolbox = QAction('工具箱', MainUI)
    AToolbox.triggered.connect(lambda: QMessageBox.critical(MainUI, ':(', '暂未实现'))

    AMathDetails = QAction('对局详情', MainUI)
    AMathDetails.triggered.connect(lambda: QMessageBox.critical(MainUI, ':(', '暂未实现'))
    # 先添加的在上面
    menu.addAction(ARestore)
    menu.addAction(AMatchQuery)
    menu.addAction(AMathDetails)
    menu.addAction(AToolbox)
    menu.addAction(AQuit)
    tray_icon.setContextMenu(menu)
    tray_icon.show()


#
def start_game(mode):
    # app_arguments = ["--arg1", "value1", "--arg2", "value2"]
    MainUI.widget_2.show()


#  mf_m.setModal(True)


#  mf_m.setModal(True)
#   mf_m.activateWindow()
#   QMessageBox.about(main_window, ':(', '没有找到路径,请手动启动吧！')


# subprocess.Popen(r"C:\Users\lnori\Desktop\nuitka.exe")

def match_query():
    MainUI.widget_1.hide()
    MainUI.widget_1.show()


def hide_widows(widows=None):
    toolbox_visible = ToolboxUI.isVisible()
    main_visible = MainUI.isVisible()
    main_widget_visible = MainUI.widget_1.isVisible()
    if widows == 'MainUI':
        if toolbox_visible:
            MainUI.widget_1.hide()
        else:
            MainUI.hide()
    elif widows == "ToolboxUI":
        ToolboxUI.hide()

    print('主窗口', MainUI.isVisible(), MainUI.widget_1.isVisible())


def set_accept(flag):
    qthread.control_auto_accept = flag


def set_summoner_show(flag: bool):
    qthread.summoner_ishow = flag
    ToolboxUI.team_show_my.setEnabled(flag)
    ToolboxUI.team_count.setEnabled(flag)


def set_summoner_my_show(flag):
    qthread.summoner_my_ishow = flag


def set_summoner_max_match(count):
    qthread.summoner_match.set_max_match(count)


def set_grab(flag):
    ToolboxUI.grab_hero.setEnabled(flag)
    if flag:
        print(ToolboxUI.grab_hero.currentData())
        qthread.hero_choose = ToolboxUI.grab_hero.currentData()
    else:
        qthread.hero_choose = -1


def set_grab_hero():
    # qthread.hero_choose = ToolboxUI.grab_hero.currentData()
    print(ToolboxUI.grab_hero.currentData())


def start():
    ##########################################################

    MainUI.dial.setWrapping(True)  # 设置转盘转完一圈后没有间隙
    MainUI.setWindowTitle(' LOLHlp')
    create_tray_icon()
    ui_init()
    ##########################################################
    effect = QGraphicsDropShadowEffect()
    effect.setBlurRadius(10)  # 范围
    effect.setOffset(0, 0)  # 横纵,偏移量
    effect.setColor(Qt.black)  # 颜色
    MainUI.widget_1.setGraphicsEffect(effect)
    ##########################################################
    MainUI.Button_X.clicked.connect(lambda: hide_widows('MainUI'))
    MainUI.setting.clicked.connect(lambda: ToolboxUI.show())
    ###########################################################
    #
    ToolboxUI.close_button.clicked.connect(lambda: hide_widows('ToolboxUI'))
    ToolboxUI.radio_accept_on.toggled.connect(lambda: set_accept(ToolboxUI.radio_accept_on.isChecked()))
    ToolboxUI.radio_team_on.toggled.connect(lambda: set_summoner_show(ToolboxUI.radio_team_on.isChecked()))
    ToolboxUI.team_show_my.toggled.connect(lambda: set_summoner_my_show(ToolboxUI.team_show_my.isChecked()))
    ToolboxUI.team_count.textEdited.connect(lambda: set_summoner_max_match(int(ToolboxUI.team_count.text())))
    ToolboxUI.radio_grab_on.toggled.connect(lambda: set_grab(ToolboxUI.radio_grab_on.isChecked()))
    ToolboxUI.grab_hero.currentIndexChanged.connect(set_grab_hero)

    ############################################################

    qthread.set_sata.connect(set_state)
    qthread.load_user_data.connect(load_data)  # 载入
    qthread.window_enable.connect(lambda b: MainUI.setEnabled(b))
    ##########################################################
    qthread.summoner_info.connect(set_summoner_info)
    qthread.summoner_hero.connect(set_summoner_hero)
    qthread.summoner_hide.connect(set_summoner_hide)
    qthread.summoner_init.connect(summoner_init)
    ###############################################################
    qthread.start()
    MainUI.show()
    from win32api import Sleep
    Sleep(7)


async def ft(data):
    await asyncio.sleep(3)
    print(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    local_setting = {}  # 软件配置
    hero = {}  # 英雄信息
    user = {}  # 用户信息
    summoner = {}  # 队友信息
    qthread = LcuThread()
    summoner_rect = SummonerUIRect()

    MainUI = MainWindow()
    ToolboxUI = Toolbox(MainUI)
    MainUI.show()

    start()
    app.exec_()  # 开始
