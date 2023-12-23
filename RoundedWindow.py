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
from PyQt5 import QtCore
# import qdarktheme

from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, \
    QGraphicsDropShadowEffect, QPushButton, QGridLayout, QSpacerItem, \
    QSizePolicy, QApplication, QMainWindow


class RoundedWindow(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.mPos = ''
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        '''
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(10)  # 范围
        effect.setOffset(0, 0)  # 横纵,偏移量
        effect.setColor(Qt.black)  # 颜色
        self.setGraphicsEffect(effect)
        '''

    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        """鼠标弹起事件"""
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mPos:
            self.move(self.mapToGlobal(event.pos() - self.mPos))
        event.accept()
