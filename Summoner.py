import asyncio
import json
import time

from functools import wraps

import aiohttp
import pygetwindow
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from win32api import Sleep
from SummonerUI import Ui_form

from functools import wraps

from asyncio.proactor_events import _ProactorBasePipeTransport
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, Qt, QPoint
from PyQt5.QtGui import QIcon

'''
def silence_event_loop_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RuntimeError as e:
            if str(e) != 'Event loop is closed':
                raise

    return wrapper


_ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)

目前 aiohttp 存在bug ,代码正常运行出结果,但是到最后会报错：
Exception ignored in: <function _ProactorBasePipeTransport.__del__ at XXXXXXXX>
...

RuntimeError: Event loop is closed
Bug 原因:
1.https://github.com/aio-libs/aiohttp/issues/4324
2.https://github.com/aio-libs/aiohttp/issues/1925

目前解决找到的解决办法:
方案1
使用:loop.run_until_complete(main()),启动异步
方案2
async with await session.get() as resp: 
    await resp.text()
await asyncio.sleep(1)   在这里加入延迟
方案3
上面的装饰器

'''


class GetSummonerMatch(QThread):
    summoner_data = QtCore.pyqtSignal(str, dict)

    def __init__(self, max_match=20):
        super().__init__()
        #    self.wegame_cookie = ""
        self.ppuid = []
        self.region = None
        self.max_match = max_match - 1
        self.tier_zh = {
            'unranked': '无段位',
            'none': '无段位',
            'emerald': '流光翡翠',
            'iron': '坚韧黑铁',
            'bronze': '英勇黄铜',
            'silver': '不屈白银',
            'gold': '荣耀黄金',
            'platinum': '华贵铂金',
            'diamond': '璀璨钻石',
            'master': '超凡大师',
            'grandmaster': '傲世宗师',
            'challenger': '最强王者',
        }
        self.headers = None
        self.port = None
        self.loop = None

    def get_match(self, ppuid, port, headers, region=None):
        self.port = port
        self.headers = headers
        self.ppuid = ppuid
        self.region = region
        self.start()

    def count_consecutive_elements(self, lst):
        if len(lst) < 2:
            return ''
        count_num = 1
        first = lst[0]
        if first == lst[1]:
            for bl in lst[1:]:
                if first == bl:
                    count_num += 1
                else:
                    break
            return f"{count_num}连{'胜' if first else '败'}中" if count_num > 1 else ''
        else:
            first = not first
            count_num = 0
            for bl in lst[1:]:
                if first == bl:
                    count_num += 1
                else:
                    break
            return f"{count_num}连{'胜' if first else '败'}中断" if count_num > 2 else ''

    async def get_data(self, url, session):
        async with await session.get(f"https://127.0.0.1:{self.port}{url}", headers=self.headers) as resp:
            data = json.loads(await resp.text())
        return data

    async def get_lol_match(self, ppuid):

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, ssl=False)) as session:
            tier = self.get_data(f"/lol-ranked/v1/ranked-stats/{ppuid}", session)
            masteries = self.get_data(f"/lol-collections/v1/inventories/{ppuid}/champion-mastery", session)
            games = self.get_data(f"/lol-match-history/v1/products/lol/{ppuid}/matches?begIndex=0&endIndex="f"{self.max_match}", session)
            tier, games, masteries = await asyncio.gather(tier, games, masteries)

        tier = tier['highestCurrentSeasonReachedTierSR']
        games = games['games']['games']
        wins = []
        hero_worl = {}
        for game in games:
            participants = game['participants'][0]
            if not participants['championId'] in hero_worl:
                hero_worl[participants['championId']] = {
                    'wins': 0,
                    'lost': 0
                }
            if participants['stats']['win']:
                hero_worl[participants['championId']]['wins'] += 1
                wins.append(True)
            else:
                hero_worl[participants['championId']]['lost'] += 1
                wins.append(False)
        hero_collections = {}
        sorted_masteries = sorted(masteries, key=lambda x: x["championPoints"], reverse=True)
        for i, mastery in enumerate(sorted_masteries):
            hero_collections[mastery['championId']] = {
                'championPoints': mastery['championPoints'],
                'championPoints_no': i + 1
            }
        self.summoner_data.emit(ppuid, {
            "wins": wins.count(True),
            "lost": wins.count(False),
            #   "wins_rate":
            "state": self.count_consecutive_elements(wins),
            'hero_collections': hero_collections,
            'tier': self.tier_zh.get(tier.lower(), str(tier)),
            'hero_worl': hero_worl
        })

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = []
        for ppuid in self.ppuid:
            print(ppuid)
            task.append(loop.create_task(self.get_lol_match(ppuid)))
        loop.run_until_complete(asyncio.wait(task))

    def set_max_match(self, count):
        self.max_match = count - 1


class SummonerUIRect(QThread):
    def __init__(self):
        super().__init__()
        self.widows = []
        self.bind_widows = {}

    def run(self):
        width = 100
        offset = 120
        while True:
            windows = pygetwindow.getAllWindows()
            for window in windows:
                if "League of Legends" == window.title:
                    print(f"窗口标题：{window.title}, 位置：{window.topleft}, 大小：{window.size}")
                    for floor, ui in self.bind_widows.items():
                        # ui.moveto(window.topleft.x + 293, window.topleft.y + 120 + floor * width)
                        ui.move(window.topleft.x + 293, window.topleft.y + offset + floor * width)
                    if window.isMinimized:
                        print(f"窗口 '{window.title}' 已最小化")
                    if not window.isActive:
                        print(f"窗口 '{window.title}' 被遮挡")
                    break
            break

    def init(self):
        if self.isRunning():
            self.quit()
        for ui in self.bind_widows.values():
            if ui.isVisible():
                ui.hide()
            self.widows.append(ui)
        self.bind_widows = {}

    # Ui_form
    def bind_ui(self, floor: int) -> Ui_form:
        if floor in self.bind_widows:
            return self.bind_widows[floor]
        if not self.widows:
            self.widows.append(Ui_form())
        self.bind_widows[floor] = self.widows.pop()

        return self.bind_widows[floor]


class SummonerUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.summoner = None
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() | 0x80)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        self.shrink.clicked.connect(self.shrink_clicked)
        self.detail.clicked.connect(self.detail_clicked)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowOpacity(0.9)
        self.animation = QPropertyAnimation(self.summoner, b'pos')
        self.animation.setDuration(100)

    def detail_clicked(self):
        self.auto_size()

    def auto_size(self) -> None:
        self.summoner.adjustSize()
        self.summoner.adjustSize()
        self.adjustSize()

    def shrink_clicked(self):

        x = self.summoner.pos().x()
        if x == 0:
            end_pos = QPoint(-self.summoner.width() + self.shrink.width() + 15, 0)
            self.animation.setEndValue(end_pos)
            self.shrink.setIcon(QIcon("C:/Users/lnori/Desktop/right.png"))

        else:
            self.animation.setEndValue(QPoint(0, 0))
            self.shrink.setIcon(QIcon("C:/Users/lnori/Desktop/left.png"))

        self.animation.start()

    def moveto(self, x, y):
        self.move(x, y)

    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(771, 100)
        form.setMaximumSize(QtCore.QSize(16777215, 100333))
        form.setStyleSheet("")
        self.summoner = QtWidgets.QWidget(form)
        self.summoner.setGeometry(QtCore.QRect(0, 0, 481, 100))
        self.summoner.setMinimumSize(QtCore.QSize(0, 100))
        self.summoner.setMaximumSize(QtCore.QSize(59999, 100))
        self.summoner.setStyleSheet("QWidget#summoner{\n"
                                    "background-color:rgb(248, 249, 250);\n"
                                    "border: 1px solid rgb(179, 179, 179) ;\n"
                                    "border-style:solid;\n"
                                    "border-bottom-right-radius:10px;\n"
                                    "border-top-right-radius:10px;\n"
                                    "}")
        self.summoner.setObjectName("summoner")
        self.layoutWidget = QtWidgets.QWidget(self.summoner)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 451, 101))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.summoner)
        self.horizontalLayout_4.setContentsMargins(10, 10, 8, 8)
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 6, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.recently = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.recently.setFont(font)
        self.recently.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.recently.setObjectName("recently")
        self.horizontalLayout.addWidget(self.recently)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(8)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.recently_worl = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.recently_worl.setFont(font)
        self.recently_worl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.recently_worl.setObjectName("recently_worl")
        self.horizontalLayout_6.addWidget(self.recently_worl)
        self.recently_state = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.recently_state.setFont(font)
        self.recently_state.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.recently_state.setObjectName("recently_state")
        self.horizontalLayout_6.addWidget(self.recently_state)
        self.horizontalLayout.addLayout(self.horizontalLayout_6)
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.detail = QtWidgets.QPushButton(self.layoutWidget)
        self.detail.setMaximumSize(QtCore.QSize(80, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.detail.setFont(font)
        self.detail.setStyleSheet("\n"
                                  "QPushButton {\n"
                                  "\n"
                                  "    color: #0081db;\n"
                                  "    border: 1px solid #dadce0;\n"
                                  "    padding: 4px 8px;\n"
                                  "    border-radius: 4px;\n"
                                  "}\n"
                                  "QPushButton:!window {\n"
                                  "    background: transparent;\n"
                                  "}\n"
                                  "QPushButton:flat,\n"
                                  "QPushButton:default {\n"
                                  "    border: none;\n"
                                  "    padding: 5px 9px;\n"
                                  "}\n"
                                  "QPushButton:default {\n"
                                  "    color: #f8f9fa;\n"
                                  "    background: #0081db;\n"
                                  "}\n"
                                  "QPushButton:hover,\n"
                                  "QPushButton:flat:hover {\n"
                                  "    background: rgba(181.000, 202.000, 244.000, 0.333);\n"
                                  "}\n"
                                  "QPushButton:pressed,\n"
                                  "QPushButton:flat:pressed,\n"
                                  "QPushButton:checked:pressed,\n"
                                  "QPushButton:flat:checked:pressed {\n"
                                  "    background: rgba(181.000, 202.000, 244.000, 0.933);\n"
                                  "}\n"
                                  "QPushButton:checked,\n"
                                  "QPushButton:flat:checked {\n"
                                  "    background: rgba(181.000, 202.000, 244.000, 0.733);\n"
                                  "}\n"
                                  "QPushButton:default:hover {\n"
                                  "    background: #3781ea;\n"
                                  "}\n"
                                  "QPushButton:default:pressed {\n"
                                  "    background: #6ca1f0;\n"
                                  "}\n"
                                  "QPushButton:default:disabled {\n"
                                  "    background: #dadce0;\n"
                                  "}")
        self.detail.setObjectName("detail")
        self.horizontalLayout.addWidget(self.detail)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.hero_proficiency = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.hero_proficiency.setFont(font)
        self.hero_proficiency.setObjectName("hero_proficiency")
        self.horizontalLayout_2.addWidget(self.hero_proficiency)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setMaximumSize(QtCore.QSize(232, 16777215))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_5.addWidget(self.label_2)
        self.hero_no = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.hero_no.setFont(font)
        self.hero_no.setObjectName("hero_no")
        self.horizontalLayout_5.addWidget(self.hero_no)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_5)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(8)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.session_value_5 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.session_value_5.setFont(font)
        self.session_value_5.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.session_value_5.setObjectName("session_value_5")
        self.horizontalLayout_3.addWidget(self.session_value_5)
        self.hero_worl = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.hero_worl.setFont(font)
        self.hero_worl.setObjectName("hero_worl")
        self.horizontalLayout_3.addWidget(self.hero_worl)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.rank = QtWidgets.QLabel(self.layoutWidget)
        self.rank.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.rank.setFont(font)
        self.rank.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft)
        self.rank.setObjectName("rank")
        self.horizontalLayout_3.addWidget(self.rank)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.shrink = QtWidgets.QPushButton(self.layoutWidget)
        self.shrink.setMaximumSize(QtCore.QSize(23, 70))
        self.shrink.setStyleSheet("QPushButton {\n"
                                  "\n"
                                  "    color: #0081db;\n"
                                  "    border: 0px ;\n"
                                  "    border-radius: 4px;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:!window {\n"
                                  "    background: transparent;\n"
                                  "}\n"
                                  "\n"
                                  "QPushButton:default {\n"
                                  "    color: #f8f9fa;\n"
                                  "    background: #0081db;\n"
                                  "}\n"
                                  "QPushButton:hover,\n"
                                  "QPushButton:flat:hover {\n"
                                  "    background: rgba(181.000, 202.000, 244.000, 0.333);\n"
                                  "}\n"
                                  "QPushButton:pressed,\n"
                                  "QPushButton:flat:pressed,\n"
                                  "QPushButton:checked:pressed,\n"
                                  "QPushButton:flat:checked:pressed {\n"
                                  "    background: rgba(181.000, 202.000, 244.000, 0.933);\n"
                                  "}\n"
                                  "QPushButton:checked,\n"
                                  "QPushButton:flat:checked {\n"
                                  "    background: rgba(181.000, 202.000, 244.000, 0.733);\n"
                                  "}\n"
                                  "QPushButton:default:hover {\n"
                                  "    background: #3781ea;\n"
                                  "}\n"
                                  "QPushButton:default:pressed {\n"
                                  "    background: #6ca1f0;\n"
                                  "}\n"
                                  "QPushButton:default:disabled {\n"
                                  "    background: #dadce0;\n"
                                  "}")
        self.shrink.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/lnori/Desktop/left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.shrink.setIcon(icon)
        self.shrink.setIconSize(QtCore.QSize(23, 70))
        self.shrink.setAutoRepeatDelay(292)
        self.shrink.setObjectName("shrink")
        self.horizontalLayout_4.addWidget(self.shrink)
        spacerItem3 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "Form"))
        self.recently.setText(_translate("form", "近20场:"))
        self.recently_worl.setText(_translate("form", "99胜99负"))
        self.recently_state.setText(_translate("form", "1123"))
        self.detail.setText(_translate("form", "详情"))
        self.label_3.setText(_translate("form", "成就点:"))
        self.hero_proficiency.setText(_translate("form", "0"))
        self.label_2.setText(_translate("form", " No."))
        self.hero_no.setText(_translate("form", "0"))
        self.session_value_5.setText(_translate("form", "近 期:"))
        self.hero_worl.setText(_translate("form", "无记录"))
        self.rank.setText(_translate("form", "荣耀黄金"))
