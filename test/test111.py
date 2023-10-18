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

        self.show()
        self.switch_location.activated.connect(lambda: self.switch(self.switch_location.currentData()))

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
