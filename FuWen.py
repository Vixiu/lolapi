import asyncio

from concurrent.futures import ThreadPoolExecutor as Executor
import copy
import aiohttp
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPainterPath, QIcon
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGraphicsDropShadowEffect, QWidget, QFrame
from gevent.resolver import blocking

from FuWenUI import Ui_FuWen
from Lcu import LcuRequest
from PyQt5 import QtCore, QtGui, QtWidgets
from Widget import RoundedWindow
import data_rc
from info_data import Info


class FuWen(RoundedWindow, Ui_FuWen):
    def __init__(self, lcu: LcuRequest):
        super(FuWen, self).__init__()
        self.hero_id = None
        self.rune_data = Info().rune_id
        self.tier = None
        self.hero = None
        self.hero_title = None

        self.lcu = lcu
        self.setupUi(self)
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)  # 范围
        effect.setOffset(0, 0)  # 横纵,偏移量
        effect.setColor(Qt.black)  # 颜色
        self.widget_bottom.setGraphicsEffect(effect)

        self.rune_id = {}
        # 符文数据 图标,id
        self.hero_data = {}

        # 英雄数据 符文,位置, 等
        self.zh_ch = {
            'top': '上单',
            'mid': '中单',
            'jungle': '打野',
            'support': '辅助',
            'bottom': '下路',
            'ARAM': '大乱斗',
            '420': '召唤师峡谷--单排/双排',
            '430': '召唤师峡谷--匹配模式',
            '440': '召唤师峡谷--灵活排位',
            '450': '嚎哭深渊--极地大乱斗',
            '900': '召唤师峡谷--无限火力',
            '318': '召唤师峡谷--无限乱斗',
            '830': '召唤师峡谷--人机入门',
            '840': '召唤师峡谷--人机新手',
            '850': '召唤师峡谷--人机一般',
            '1400': '召唤师峡谷--终极魔典',
            '-1': '召唤师峡谷--训练模式',
            'unranked': '暂无段位',
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

        self.vbox_rune = QVBoxLayout()
        self.vbox_rune.setContentsMargins(0, 0, 0, 0)
        # self.fuwenlist.setMaximumSize(430, 1250)  # ---
        self.fuwenlist.setLayout(self.vbox_rune)
        self.vbox_rune.setAlignment(Qt.AlignTop)
        self.vbox_rune.setSpacing(1)

        self.vbox_items = QVBoxLayout()
        self.vbox_items.setContentsMargins(6, 4, 0, 0)
        self.scrollAreaWidgetContents_3.setLayout(self.vbox_items)

        self.vbox_items.setAlignment(Qt.AlignTop)
        self.vbox_items.setSpacing(10)

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

        #   self.swith_tier_3.currentIndexChanged.connect(lambda: self.switch_tier(self.swith_tier_3.currentData(), self.ui_switch_lane.currentData()))
        # ui_home.herolist.activated[str].connect(lambda s: grab_hero(s))
        self.ui_switch_lane.activated.connect(lambda: self.switch_lane(self.ui_switch_lane.currentData()))
        self.swith_tier_3.activated.connect(
            lambda: self.switch_tier(self.swith_tier_3.currentData(), self.ui_switch_lane.currentData()))
        self.queues_info = {
            '430': '420',
            '420': '420',
            '440': '440',
            '450': '450',
            '1400': '420',
            '1200': '420',
            '1300': '420',
        }

    def initialize_hero_data(self):

        #  lane = ['top', 'mid', 'jungle', 'support', 'bottom']
        #  tier = ['challenger', 'grandmaster', 'master', 'diamond', 'platinum', 'gold', 'silver', 'bronze', 'iron']
        return {
            '420': {
                'items': {},
                'spell': {},
                'rune': {},
                'lane': [],
                'ranging': {
                    'top': {},
                    'mid': {},
                    'jungle': {},
                    'support': {},
                    'bottom': {},
                }
            },
            '450': {
                'items': {'ARAM': []},
                'spell': {'ARAM': {}},
                'rune': {'ARAM': []},
                'lane': ['ARAM'],
                'ranging': {
                    'ARAM': {}
                }
            },
            'tips': {
                'ally_tips': '',
                'enemy_tips': ''
            }
        }

    def switch_lane(self, lane):

        # 清楚布局
        for i in range(self.vbox_rune.count()):
            self.vbox_rune.itemAt(i).widget().deleteLater()
        for i in range(self.vbox_items.count()):
            self.vbox_items.itemAt(i).widget().deleteLater()
        # 增加天赋
        for rune in self.hero['rune'][lane]:
            self.add_rune(rune, f'{self.hero_title}-{self.zh_ch[lane]}')
        # 增加装备
        for items in self.hero['items'][lane]:
            self.add_items(items)
        self.label_13.setPixmap(QPixmap(f':spells/{self.hero["spell"][lane].get("spell1", ["54", "54"])[0]}.png'))
        self.label_15.setPixmap(QPixmap(f':spells/{self.hero["spell"][lane].get("spell1", ["54", "54"])[1]}.png'))
        self.label_21.setPixmap(QPixmap(f':spells/{self.hero["spell"][lane].get("spell2", ["54", "54"])[0]}.png'))
        self.label_22.setPixmap(QPixmap(f':spells/{self.hero["spell"][lane].get("spell2", ["54", "54"])[1]}.png'))

        self.swith_tier_3.clear()
        if self.hero['ranging'][lane]:
            print('swith_lane', self.tier)
            for tier in self.hero['ranging'][lane]:
                self.swith_tier_3.addItem(QIcon(QPixmap(f':tier/{tier}.png')), self.zh_ch[tier], tier)

            if self.tier not in self.hero['ranging'][lane]:
                self.switch_tier(list(self.hero['ranging'][lane].keys())[0], lane)
                self.swith_tier_3.setCurrentText(self.zh_ch[list(self.hero['ranging'][lane].keys())[0]])
            else:

                self.switch_tier(self.tier, lane)
                self.swith_tier_3.setCurrentText(self.zh_ch[self.tier])
        else:
            self.swith_tier_3.addItem(QIcon(QPixmap(f':tier/unranked.png')), '暂无段位', '暂无段位')
            self.hero_gradient.setText(' 暂无数据')
            self.hero_ranking.setText('')
            self.hero_win.setText('')

    def switch_tier(self, tier, lane):

        ranging = self.hero['ranging'][lane]
        self.hero_gradient.setText(f' 梯度:T{ranging[tier]["T"]}')
        self.hero_ranking.setText(f'排名:{ranging[tier]["No"]}')
        self.hero_win.setText(f'胜率:{ranging[tier]["win_rate"]}%')

    def set_hero(self, hero_id, hero_title, lane=None, queues=None, tier='silver'):
        self.hero_id = hero_id
        # 固定不变信息-头像 名字 路线
        print('set_hero', tier)
        self.tier = tier
        self.hero_title = hero_title
        queues = self.queues_info.get(queues, '420')
        #        self.lane_bast_ui.setText(f'推荐位置:{",".join(self.hero["lane"])}')
        self.hero = self.hero_data[hero_id][queues]
        self.hero_name.setText(hero_title)
        self.hero_avatar.setPixmap(QPixmap(f':hero/{hero_id}.png'))
        self.state.setText(self.zh_ch.get(queues, '未知'))
        #  self.ui_tips.setText(self.hero_data[hero_id]['tips'][])
        self.ui_switch_lane.clear()
        # 默认 有符文的路 为基
        for _ in self.hero['lane']:
            self.ui_switch_lane.addItem(QIcon(QPixmap(f':other/{_}.png')), self.zh_ch[_], _)

        for _ in set(self.hero['rune'].keys()) - set(self.hero['lane']):
            self.ui_switch_lane.addItem(QIcon(QPixmap(f':other/{_}-disabled.png')), self.zh_ch[_], _)

        if lane not in self.hero['rune']:
            if self.hero['lane']:
                lane = self.hero['lane'][0]
            else:
                lane = list(self.hero['rune'].keys())[0]
        self.ui_switch_lane.setCurrentText(self.zh_ch.get(lane))
        self.switch_lane(lane)

    def add_rune(self, rune_data, name):
        rune_widget = RuneWidget()
        rune_widget.shenglv.setText(f"<span style=\" color: #9a9a9a \">{rune_data['win_rate']}</span>")
        rune_widget.shiyonglv.setText(f"<span style=\" color: #9a9a9a \">{rune_data['show_rate']}</span>")
        rune_widget.f1.setPixmap(QPixmap(f':rune/{rune_data["rune"][0]}.png'))
        rune_widget.f2.setPixmap(QPixmap(f':rune/{rune_data["rune"][1]}.png'))
        rune_widget.f3.setPixmap(QPixmap(f':rune/{rune_data["rune"][2]}.png'))
        rune_widget.f4.setPixmap(QPixmap(f':rune/{rune_data["rune"][3]}.png'))
        rune_widget.f5.setPixmap(QPixmap(f':rune/{rune_data["rune"][4]}.png'))
        rune_widget.f6.setPixmap(QPixmap(f':rune/{rune_data["rune"][5]}.png'))
        rune_widget.f7.setPixmap(QPixmap(f':rune/{rune_data["rune"][6]}.png'))
        rune_widget.f8.setPixmap(QPixmap(f':rune/{rune_data["rune"][7]}.png'))
        rune_widget.f9.setPixmap(QPixmap(f':rune/{rune_data["rune"][8]}.png'))
        self.vbox_rune.addWidget(rune_widget)
        rune_widget.tijiao.setObjectName(str(rune_data['rune']))
        rune_widget.tijiao.clicked.connect(lambda: self.test(rune_widget.tijiao.objectName(), name))

    def add_items(self, items_data):
        items_widget = ItemsWidget()

        items_widget.label_7.setPixmap(QPixmap(f':items/{items_data["items"][0]}.png'))
        items_widget.label_6.setPixmap(QPixmap(f':items/{items_data["items"][1]}.png'))
        items_widget.label_5.setPixmap(QPixmap(f':items/{items_data["items"][2]}.png'))
        items_widget.label_4.setText(f"<span style=\" color: #9c8250  \">{items_data['win_rate']}</span>")
        items_widget.label_14.setText(f"<span style=\" color: #1dbaa9 \">{items_data['show_rate']}</span>")
        self.vbox_items.addWidget(items_widget)

    def clean_hero(self):
        pass

    def test(self, perk, title):

        perk = eval(perk)
        res = self.lcu.getdata('/lol-perks/v1/currentpage').json()
        res = res['id']
        self.lcu.getdata(f'/lol-perks/v1/pages/{res}', 'DELETE')
        res = self.lcu.getdata('/lol-perks/v1/pages', 'post', None, {
            "autoModifiedSelections": [],
            "current": True,
            "isActive": True,
            "isDeletable": True,
            "isEditable": True,
            "isValid": True,
            "lastModified": 0,
            "name": title,
            "order": 0,
            "primaryStyleId": self.rune_data[str(perk[1])]['id'],
            "selectedPerkIds": perk,
            "subStyleId": self.rune_data[str(perk[4])]['id']
        })


class GetData(QThread):
    data = QtCore.pyqtSignal(str, object)

    def __init__(self, info):
        super().__init__()
        self.info = info

    def run(self):
        #  loop = asyncio.get_event_loop()
        #        loop = asyncio.get_running_loop()
        # asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = []
        for _id in self.info:
            _ = loop.create_task(self.async_get(_id, self.info[_id]))
            _.add_done_callback(self.emit_data)
            task.append(_)
        loop.run_until_complete(asyncio.wait(task))

    async def async_get(self, _id, url):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64, ssl=False)) as session:
            async with await session.get(url, headers={'Referer': 'https://101.qq.com/'}) as resp:
                page_text = await resp.text()
        return _id, page_text

    def emit_data(self, info):
        _id, data = info.result()
        self.data.emit(_id, data)


class RuneWidget(QWidget):
    def __init__(self):
        super(RuneWidget, self).__init__()
        self.fll = self
        self.fll.setEnabled(True)
        self.fll.setGeometry(QtCore.QRect(250, 180, 390, 90))
        self.fll.setMinimumSize(QtCore.QSize(390, 90))
        self.fll.setMaximumSize(QtCore.QSize(390, 90))
        self.fll.setAutoFillBackground(False)

        self.fll.setObjectName("fll")
        self.f1 = QtWidgets.QLabel(self.fll)
        self.f1.setGeometry(QtCore.QRect(0, 10, 70, 70))
        self.f1.setMaximumSize(QtCore.QSize(70, 70))
        self.f1.setText("")
        self.f1.setPixmap(QtGui.QPixmap("D:/lol-api/2/8214.png"))
        self.f1.setScaledContents(True)
        self.f1.setObjectName("f1")
        self.layoutWidget_6 = QtWidgets.QWidget(self.fll)
        self.layoutWidget_6.setGeometry(QtCore.QRect(70, 20, 141, 51))
        self.layoutWidget_6.setObjectName("layoutWidget_6")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.layoutWidget_6)
        self.horizontalLayout_17.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.f2 = QtWidgets.QLabel(self.layoutWidget_6)
        self.f2.setMaximumSize(QtCore.QSize(42, 42))
        self.f2.setText("")
        self.f2.setPixmap(QtGui.QPixmap("D:/lol-api/2/8105.png"))
        self.f2.setScaledContents(True)
        self.f2.setObjectName("f2")
        self.horizontalLayout_17.addWidget(self.f2)
        self.f3 = QtWidgets.QLabel(self.layoutWidget_6)
        self.f3.setMinimumSize(QtCore.QSize(0, 0))
        self.f3.setMaximumSize(QtCore.QSize(42, 42))
        self.f3.setText("")
        self.f3.setPixmap(QtGui.QPixmap("D:/lol-api/2/8135.png"))
        self.f3.setScaledContents(True)
        self.f3.setObjectName("f3")
        self.horizontalLayout_17.addWidget(self.f3)
        self.f4 = QtWidgets.QLabel(self.layoutWidget_6)
        self.f4.setMaximumSize(QtCore.QSize(42, 42))
        self.f4.setText("")
        self.f4.setPixmap(QtGui.QPixmap("D:/lol-api/2/8136.png"))
        self.f4.setScaledContents(True)
        self.f4.setObjectName("f4")
        self.horizontalLayout_17.addWidget(self.f4)
        self.horizontalLayoutWidget_12 = QtWidgets.QWidget(self.fll)
        self.horizontalLayoutWidget_12.setGeometry(QtCore.QRect(210, 0, 81, 51))
        self.horizontalLayoutWidget_12.setObjectName("horizontalLayoutWidget_12")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_12)
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.f6 = QtWidgets.QLabel(self.horizontalLayoutWidget_12)
        self.f6.setMaximumSize(QtCore.QSize(35, 35))
        self.f6.setText("")
        self.f6.setPixmap(QtGui.QPixmap("D:/lol-api/2/8014.png"))
        self.f6.setScaledContents(True)
        self.f6.setObjectName("f6")
        self.horizontalLayout_18.addWidget(self.f6)
        self.f5 = QtWidgets.QLabel(self.horizontalLayoutWidget_12)
        self.f5.setMaximumSize(QtCore.QSize(35, 35))
        self.f5.setText("")
        self.f5.setPixmap(QtGui.QPixmap("D:/lol-api/2/8009.png"))
        self.f5.setScaledContents(True)
        self.f5.setObjectName("f5")
        self.horizontalLayout_18.addWidget(self.f5)
        self.horizontalLayoutWidget_13 = QtWidgets.QWidget(self.fll)
        self.horizontalLayoutWidget_13.setGeometry(QtCore.QRect(210, 40, 81, 41))
        self.horizontalLayoutWidget_13.setObjectName("horizontalLayoutWidget_13")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_13)
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.f8 = QtWidgets.QLabel(self.horizontalLayoutWidget_13)
        self.f8.setMinimumSize(QtCore.QSize(27, 30))
        self.f8.setMaximumSize(QtCore.QSize(30, 30))
        self.f8.setText("")
        self.f8.setPixmap(QtGui.QPixmap("D:/lol-api/2/5001.png"))
        self.f8.setScaledContents(True)
        self.f8.setObjectName("f8")
        self.horizontalLayout_4.addWidget(self.f8)
        self.f7 = QtWidgets.QLabel(self.horizontalLayoutWidget_13)
        self.f7.setMinimumSize(QtCore.QSize(27, 30))
        self.f7.setMaximumSize(QtCore.QSize(30, 30))
        self.f7.setText("")
        self.f7.setPixmap(QtGui.QPixmap("D:/lol-api/2/5002.png"))
        self.f7.setScaledContents(True)
        self.f7.setObjectName("f7")
        self.horizontalLayout_4.addWidget(self.f7)
        self.f9 = QtWidgets.QLabel(self.horizontalLayoutWidget_13)
        self.f9.setMaximumSize(QtCore.QSize(30, 30))
        self.f9.setText("")
        self.f9.setPixmap(QtGui.QPixmap("D:/lol-api/2/5003.png"))
        self.f9.setScaledContents(True)
        self.f9.setObjectName("f9")
        self.horizontalLayout_4.addWidget(self.f9)
        self.line_4 = QtWidgets.QFrame(self.fll)
        self.line_4.setGeometry(QtCore.QRect(290, 10, 5, 65))
        self.line_4.setMaximumSize(QtCore.QSize(5, 16777215))
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setObjectName("line_4")
        self.line = QtWidgets.QFrame(self.fll)
        self.line.setGeometry(QtCore.QRect(20, 85, 350, 3))
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.tijiao = QtWidgets.QPushButton(self.fll)
        self.tijiao.setGeometry(QtCore.QRect(300, 45, 81, 31))
        self.tijiao.setMouseTracking(False)
        self.tijiao.setStyleSheet("QPushButton {\n"
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
                                  "}\n"
                                  "QDialogButtonBox QPushButton {\n"
                                  "    min-width: 65px;\n"
                                  "}")
        self.tijiao.setObjectName("tijiao")
        self.tijiao.setText('使用')
        self.widget = QtWidgets.QWidget(self.fll)
        self.widget.setGeometry(QtCore.QRect(290, 0, 102, 41))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.shiyonglv = QtWidgets.QLabel(self.widget)
        self.shiyonglv.setMinimumSize(QtCore.QSize(100, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.shiyonglv.setFont(font)
        self.shiyonglv.setAlignment(QtCore.Qt.AlignCenter)
        self.shiyonglv.setObjectName("shiyonglv")
        self.verticalLayout.addWidget(self.shiyonglv)
        self.shenglv = QtWidgets.QLabel(self.widget)
        self.shenglv.setMinimumSize(QtCore.QSize(100, 25))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.shenglv.setFont(font)
        self.shenglv.setAlignment(QtCore.Qt.AlignCenter)
        self.shenglv.setObjectName("shenglv")
        self.verticalLayout.addWidget(self.shenglv)


class ItemsWidget(QWidget):
    def __init__(self):
        super(ItemsWidget, self).__init__()
        self.widget = self
        self.widget.setGeometry(QtCore.QRect(100, 100, 240, 40))
        self.widget.setMinimumSize(QtCore.QSize(230, 40))
        self.widget.setMaximumSize(QtCore.QSize(240, 40))
        self.widget.setObjectName("widget")
        self.layoutWidget_2 = QtWidgets.QWidget(self.widget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(150, 0, 91, 41))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_14 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_6.addWidget(self.label_14)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.layoutWidget_3 = QtWidgets.QWidget(self.widget)
        self.layoutWidget_3.setGeometry(QtCore.QRect(0, 0, 131, 42))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_7.setMaximumSize(QtCore.QSize(40, 40))

        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_5.setMaximumSize(QtCore.QSize(40, 40))

        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget_3)
        self.label_6.setMaximumSize(QtCore.QSize(40, 40))

        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setGeometry(QtCore.QRect(193, 5, 3, 30))
        self.line.setLineWidth(1)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
