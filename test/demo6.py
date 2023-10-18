#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019年4月19日
@author: Irony
@site: https://pyqt.site , https://github.com/PyQt5
@email: 892768447@qq.com
@file: FramelessDialog
@description: 无边框圆角对话框
"""
from time import sleep

import qdarktheme
from PyQt5.QtGui import QPixmap

from Widget import RoundedWindow

try:
    from PyQt5.QtCore import Qt, QSize, QTimer
    from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, \
        QGraphicsDropShadowEffect, QPushButton, QGridLayout, QSpacerItem, \
        QSizePolicy, QApplication, QMainWindow
except ImportError:
    from PySide2.QtCore import Qt, QSize, QTimer
    from PySide2.QtWidgets import QDialog, QVBoxLayout, QWidget, \
        QGraphicsDropShadowEffect, QPushButton, QGridLayout, QSpacerItem, \
        QSizePolicy, QApplication



class Dialog(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()
        self.setObjectName('Custom_Dialog')
        self.resize(450, 600)
        ui = Ui_FuWen()
        wg = QWidget()
        ui.setupUi(wg)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(wg)

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet(qdarktheme.load_stylesheet("light"))

        # 添加阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(5)  # 范围
        effect.setOffset(0, 0)  # 横纵,偏移量
        effect.setColor(Qt.black)  # 颜色
        self.setGraphicsEffect(effect)
        self.show()

    def initUi(self):
        # 在widget中添加ui
        layout = QGridLayout(self.widget)
    #  layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 0)
    #  layout.addWidget(QPushButton('r', self, clicked=self.accept, objectName='closeButton'), 0, 1)
    #   layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum,QSizePolicy.Expanding), 1, 0)


from FuWenUI import Ui_FuWen

if __name__ == '__main__':
    import sys
    import data_rc
    app = QApplication(sys.argv)
    main_window = RoundedWindow()
    ui_home = Ui_FuWen()
    ui_home.setupUi(main_window)
    main_window.show()
    import os

    '''
                 for root, dirs, files in os.walk(r'C:\Users\lnori\Desktop\test\tier-promotion-to-challenger'):
                     ls = files

                 for path in ls:

                     self.ssss.emit(QPixmap(rf'C:\Users\lnori\Desktop\test\tier-promotion-to-challenger\{path}'))
                     time.sleep(0.04)
         '''




    #


    # ui_home.Gongao.append("<font color='#eb6213' size='4'>" + '9999' + "<font>")

    sys.exit(app.exec_())
