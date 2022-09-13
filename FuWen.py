import asyncio

import aiohttp
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPainterPath
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout
from FuWenUI import Ui_FuWen
from Lcu import LcuRequest
from PyQt5 import QtCore, QtGui, QtWidgets
from requests import request


class FuWen(QMainWindow, Ui_FuWen):
    def __init__(self, lcu: LcuRequest):

        super(FuWen, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.lcu = lcu
        self.setupUi(self)

        self.rune_data = {}
        # 符文数据 图标,id
        self.hero_data = {}
        # 英雄数据 符文,位置, 等
        self.zh_ch = {
            'top': '上单',
            'mid': '中单',
            'jungle': '打野',
            'support': '辅助',
            'bottom': '下路',
        }

        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.fuwenlist.setMaximumSize(430, 950)  # ---
        self.fuwenlist.setLayout(self.vbox)
        self.vbox.setAlignment(Qt.AlignTop)
        # self.vbox.setSpacing(2)
        self.button_list = []

        self.show()
        self.hero_id = ''
        self.tier = ''  # 待删除
        # ui_home.herolist.activated[str].connect(lambda s: grab_hero(s))
        self.switch_location.activated.connect(lambda: self.switch(self.switch_location.currentData()))
        self.queues = ''
        self.queues_info = {
            '430': '420',
            '420': '420',
            '440': '440',
            '450': '450',
            '1400': '420',
            '1200': '420',
            '1300': '420',
        }

    #  self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    def initialize_hero_data(self):

        #  lane = ['top', 'mid', 'jungle', 'support', 'bottom']
        #  tier = ['challenger', 'grandmaster', 'master', 'diamond', 'platinum', 'gold', 'silver', 'bronze', 'iron']

        return {
            'rune_data': 'None',
            'best_lane': [],
            'rank': 'None',
            'ranging': {
                '450': {},
                '420': {},
                '440': {}
            }
        }

    def switch(self, lane):
        # 清楚布局

        for i in range(self.vbox.count()):
            self.vbox.itemAt(i).widget().deleteLater()

        for i in self.hero_data[self.hero_id]['rune_data'][lane]:
            self.add_rune(i, f'{self.hero_name.text()}-{self.zh_ch[lane]}')
        if lane in self.hero_data[self.hero_id]['ranging'][self.queues]:
            if self.tier not in self.hero_data[self.hero_id]['ranging'][self.queues][lane]:
                self.tier = list(self.hero_data[self.hero_id]['ranging'][self.queues][lane].keys())[0]
            self.hero_gradient.setText('梯度:T' + self.hero_data[self.hero_id]['ranging'][self.queues][lane][self.tier][1])
            self.hero_ranking.setText('排名:' + self.hero_data[self.hero_id]['ranging'][self.queues][lane][self.tier][0])
            self.hero_win.setText('胜率:' + format(float(self.hero_data[self.hero_id]['ranging'][self.queues][lane][self.tier][2]), '.2%'))
        else:
            self.hero_gradient.setText('暂无数据')
            self.hero_ranking.setText('')
            self.hero_win.setText('')

    def set_hero(self, hero_id, hero_name, hero_icon, queues='420', lane=None, tier='gold'):

        self.hero_id = hero_id
        self.queues = self.queues_info.get(queues, '420')

        self.tier = tier
        if lane not in self.hero_data[hero_id]['best_lane']:
            lane = list(self.hero_data[self.hero_id]['rune_data'].keys())[0]

        best_lane = '推荐位置:'
        for _ in self.hero_data[hero_id]['best_lane']:
            best_lane = best_lane + self.zh_ch[_] + ' '
        self.lane_bast_ui.setText(best_lane)
        self.hero_name.setText(hero_name)
        # self.hero_avatar.setPixmap(QPixmap(QImage.fromData(self.lcu.getdata(hero['squarePortraitPath']).content)))  # 方形头像
        self.hero_avatar.setPixmap(self.round_scr(hero_icon))  # 圆形头像
        self.switch_location.clear()

        for _ in self.hero_data[self.hero_id]['rune_data']:
            self.switch_location.addItem(self.zh_ch[_], _)
        self.switch_location.setCurrentText(self.zh_ch[lane])
        self.switch(lane)

    def add_rune(self, rune_data, name):

        fll = QtWidgets.QFrame()
        fll.setEnabled(True)
        fll.setGeometry(QtCore.QRect(130, 180, 430, 90))
        fll.setMinimumSize(QtCore.QSize(430, 90))
        fll.setMaximumSize(QtCore.QSize(430, 90))
        fll.setStyleSheet("")
        fll.setFrameShape(QtWidgets.QFrame.StyledPanel)
        fll.setFrameShadow(QtWidgets.QFrame.Plain)
        fll.setLineWidth(10)
        fll.setMidLineWidth(0)
        fll.setObjectName("fll")
        tijiao = QtWidgets.QPushButton(fll)
        tijiao.setGeometry(QtCore.QRect(330, 50, 91, 31))
        tijiao.setMouseTracking(False)
        tijiao.setObjectName("tijiao")
        verticalLayoutWidget_7 = QtWidgets.QWidget(fll)
        verticalLayoutWidget_7.setGeometry(QtCore.QRect(320, 0, 111, 51))
        verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
        verticalLayout_7 = QtWidgets.QVBoxLayout(verticalLayoutWidget_7)
        verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        verticalLayout_7.setSpacing(0)
        verticalLayout_7.setObjectName("verticalLayout_7")
        shenglv = QtWidgets.QLabel(verticalLayoutWidget_7)
        shenglv.setAlignment(QtCore.Qt.AlignCenter)
        shenglv.setObjectName("shenglv")
        verticalLayout_7.addWidget(shenglv)
        shiyonglv = QtWidgets.QLabel(verticalLayoutWidget_7)
        font = QtGui.QFont()
        font.setPointSize(10)
        shiyonglv.setFont(font)
        shiyonglv.setAlignment(QtCore.Qt.AlignCenter)
        shiyonglv.setObjectName("shiyonglv")
        verticalLayout_7.addWidget(shiyonglv)
        f1 = QtWidgets.QLabel(fll)
        f1.setGeometry(QtCore.QRect(0, 0, 81, 91))
        f1.setText("")

        f1.setScaledContents(True)
        f1.setObjectName("f1")
        layoutWidget_5 = QtWidgets.QWidget(fll)
        layoutWidget_5.setGeometry(QtCore.QRect(70, 10, 161, 71))
        layoutWidget_5.setObjectName("layoutWidget_5")
        horizontalLayout_16 = QtWidgets.QHBoxLayout(layoutWidget_5)
        horizontalLayout_16.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        horizontalLayout_16.setSpacing(0)
        horizontalLayout_16.setObjectName("horizontalLayout_16")
        f3 = QtWidgets.QLabel(layoutWidget_5)
        f3.setMinimumSize(QtCore.QSize(0, 0))
        f3.setMaximumSize(QtCore.QSize(50, 50))
        f3.setText("")

        f3.setScaledContents(True)
        f3.setObjectName("f3")
        horizontalLayout_16.addWidget(f3)
        f2 = QtWidgets.QLabel(layoutWidget_5)
        f2.setMaximumSize(QtCore.QSize(50, 50))
        f2.setText("")
        f2.setScaledContents(True)
        f2.setObjectName("f2")
        horizontalLayout_16.addWidget(f2)
        f4 = QtWidgets.QLabel(layoutWidget_5)
        f4.setMaximumSize(QtCore.QSize(50, 50))
        f4.setText("")
        f4.setScaledContents(True)
        f4.setObjectName("f4")
        horizontalLayout_16.addWidget(f4)
        horizontalLayoutWidget_10 = QtWidgets.QWidget(fll)
        horizontalLayoutWidget_10.setGeometry(QtCore.QRect(230, 10, 91, 42))
        horizontalLayoutWidget_10.setObjectName("horizontalLayoutWidget_10")
        horizontalLayout_15 = QtWidgets.QHBoxLayout(horizontalLayoutWidget_10)
        horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        horizontalLayout_15.setObjectName("horizontalLayout_15")
        f6 = QtWidgets.QLabel(horizontalLayoutWidget_10)
        f6.setMaximumSize(QtCore.QSize(40, 40))
        f6.setText("")

        f6.setScaledContents(True)
        f6.setObjectName("f6")
        horizontalLayout_15.addWidget(f6)
        f5 = QtWidgets.QLabel(horizontalLayoutWidget_10)
        f5.setMaximumSize(QtCore.QSize(40, 40))
        f5.setText("")

        f5.setScaledContents(True)
        f5.setObjectName("f5")
        horizontalLayout_15.addWidget(f5)
        horizontalLayoutWidget_11 = QtWidgets.QWidget(fll)
        horizontalLayoutWidget_11.setGeometry(QtCore.QRect(230, 50, 92, 32))
        horizontalLayoutWidget_11.setObjectName("horizontalLayoutWidget_11")
        horizontalLayout = QtWidgets.QHBoxLayout(horizontalLayoutWidget_11)
        horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        horizontalLayout.setSpacing(0)
        horizontalLayout.setObjectName("horizontalLayout")
        f8 = QtWidgets.QLabel(horizontalLayoutWidget_11)
        f8.setMaximumSize(QtCore.QSize(30, 30))
        f8.setText("")

        f8.setScaledContents(True)
        f8.setObjectName("f8")
        horizontalLayout.addWidget(f8)
        f7 = QtWidgets.QLabel(horizontalLayoutWidget_11)
        f7.setMaximumSize(QtCore.QSize(30, 30))
        f7.setText("")

        f7.setScaledContents(True)
        f7.setObjectName("f7")
        horizontalLayout.addWidget(f7)
        f9 = QtWidgets.QLabel(horizontalLayoutWidget_11)
        f9.setMaximumSize(QtCore.QSize(30, 30))
        f9.setText("")
        f9.setScaledContents(True)
        f9.setObjectName("f9")
        horizontalLayout.addWidget(f9)
        line = QtWidgets.QFrame(fll)
        line.setGeometry(QtCore.QRect(315, 0, 21, 91))
        line.setFrameShape(QtWidgets.QFrame.VLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setObjectName("line")
        tijiao.setText('使用')
        shenglv.setText(rune_data['win_rate'])
        shiyonglv.setText(rune_data['show_rate'])

        f1.setPixmap(self.rune_data[rune_data['rune'][0]]['icon'])
        f2.setPixmap(self.rune_data[rune_data['rune'][1]]['icon'])
        f3.setPixmap(self.rune_data[rune_data['rune'][2]]['icon'])
        f4.setPixmap(self.rune_data[rune_data['rune'][3]]['icon'])
        f5.setPixmap(self.rune_data[rune_data['rune'][4]]['icon'])
        f6.setPixmap(self.rune_data[rune_data['rune'][5]]['icon'])
        f7.setPixmap(self.rune_data[rune_data['rune'][6]]['icon'])
        f8.setPixmap(self.rune_data[rune_data['rune'][7]]['icon'])
        f9.setPixmap(self.rune_data[rune_data['rune'][8]]['icon'])

        self.vbox.addWidget(fll)
        # self.vbox.insertWidget(0,fll)
        tijiao.setObjectName(str(rune_data['rune']))

        tijiao.clicked.connect(lambda: self.test(tijiao.objectName(), name))

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

    def round_scr(self, path):
        pixmapa = QPixmap(QImage.fromData(self.lcu.getdata(path).content))
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


class GetData(QThread):
    data = QtCore.pyqtSignal(str, object)
    add_text = QtCore.pyqtSignal(str)
    set_sata = QtCore.pyqtSignal(str)

    def __init__(self, info, text, lcu):
        super().__init__()
        self.text = text
        self.lcu = lcu
        self.info = info

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        task = []
        if self.lcu is None:
            for _id in self.info:
                _ = loop.create_task(self.async_get(_id, self.info[_id]))
                task.append(_)
            # self.data.emit(_id, request('get', self.info[_id]).text)

        else:
            for _id in self.info:
                _ = loop.create_task(self.async_lcu(_id, self.info[_id]))
                task.append(_)
            #    self.data.emit(_id, QPixmap(QImage.fromData(self.lcu.getdata(self.info[_id]).content)))
        for _ in task:
            _.add_done_callback(self.emit_data)
        loop.run_until_complete(asyncio.wait(task))



    async def async_get(self, _id, url):
        async with aiohttp.ClientSession() as session:
            async with await session.get(url) as resp:
                page_text = await resp.text()
                return _id, page_text

    async def async_lcu(self, _id, url):
        return _id, QPixmap(QImage.fromData(self.lcu.getdata(url).content))

    def emit_data(self, info):
        _id, data = info.result()
        self.data.emit(_id, data)
