# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lolapi.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.setEnabled(True)
        Frame.resize(586, 447)
        Frame.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.Start = QtWidgets.QPushButton(Frame)
        self.Start.setEnabled(True)
        self.Start.setGeometry(QtCore.QRect(20, 340, 151, 61))
        self.Start.setObjectName("Start")
        self.name = QtWidgets.QLabel(Frame)
        self.name.setGeometry(QtCore.QRect(30, 170, 131, 31))
        self.name.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.name.setAutoFillBackground(False)
        self.name.setTextFormat(QtCore.Qt.AutoText)
        self.name.setScaledContents(True)
        self.name.setAlignment(QtCore.Qt.AlignCenter)
        self.name.setObjectName("name")
        self.Gongao = QtWidgets.QTextBrowser(Frame)
        self.Gongao.setEnabled(False)
        self.Gongao.setGeometry(QtCore.QRect(210, 210, 331, 201))
        self.Gongao.setObjectName("Gongao")
        self.layoutWidget = QtWidgets.QWidget(Frame)
        self.layoutWidget.setGeometry(QtCore.QRect(220, 20, 180, 111))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.xzdj = QtWidgets.QCheckBox(self.layoutWidget)
        self.xzdj.setObjectName("xzdj")
        self.verticalLayout.addWidget(self.xzdj)
        self.zdjs = QtWidgets.QCheckBox(self.layoutWidget)
        self.zdjs.setObjectName("zdjs")
        self.verticalLayout.addWidget(self.zdjs)
        self.layoutWidget1 = QtWidgets.QWidget(Frame)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 410, 186, 31))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.radioButton = QtWidgets.QRadioButton(self.layoutWidget1)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.layoutWidget1)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout.addWidget(self.radioButton_2)
        self.layoutWidget2 = QtWidgets.QWidget(Frame)
        self.layoutWidget2.setGeometry(QtCore.QRect(400, 100, 141, 71))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget2)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_2.addWidget(self.pushButton_5)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget2)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.profile = QtWidgets.QLabel(Frame)
        self.profile.setGeometry(QtCore.QRect(40, 20, 120, 120))
        self.profile.setScaledContents(True)
        self.profile.setObjectName("profile")
        self.line = QtWidgets.QFrame(Frame)
        self.line.setGeometry(QtCore.QRect(160, 10, 51, 401))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(Frame)
        self.label_2.setGeometry(QtCore.QRect(40, 20, 120, 120))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("C:/Users/lnori/Desktop/lol-wangz/challenge-card-token-mask.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Frame)
        self.label_3.setEnabled(True)
        self.label_3.setGeometry(QtCore.QRect(8, 74, 181, 121))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("C:/Users/lnori/Desktop/lol-wangz/challenger.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.layoutWidget3 = QtWidgets.QWidget(Frame)
        self.layoutWidget3.setGeometry(QtCore.QRect(220, 130, 143, 71))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkBox_5 = QtWidgets.QCheckBox(self.layoutWidget3)
        self.checkBox_5.setEnabled(False)
        self.checkBox_5.setCheckable(True)
        self.checkBox_5.setChecked(True)
        self.checkBox_5.setAutoRepeat(False)
        self.checkBox_5.setObjectName("checkBox_5")
        self.verticalLayout_3.addWidget(self.checkBox_5)
        self.checkBox_4 = QtWidgets.QCheckBox(self.layoutWidget3)
        self.checkBox_4.setEnabled(False)
        self.checkBox_4.setMouseTracking(True)
        self.checkBox_4.setCheckable(True)
        self.checkBox_4.setChecked(True)
        self.checkBox_4.setObjectName("checkBox_4")
        self.verticalLayout_3.addWidget(self.checkBox_4)
        self.layoutWidget4 = QtWidgets.QWidget(Frame)
        self.layoutWidget4.setGeometry(QtCore.QRect(30, 200, 141, 121))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButton_6 = QtWidgets.QPushButton(self.layoutWidget4)
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_4.addWidget(self.pushButton_6)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget4)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_4.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget4)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_4.addWidget(self.pushButton_4)
        self.pushButton_2 = QtWidgets.QPushButton(Frame)
        self.pushButton_2.setGeometry(QtCore.QRect(420, 180, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.herolist = QtWidgets.QComboBox(Frame)
        self.herolist.setEnabled(True)
        self.herolist.setGeometry(QtCore.QRect(290, 20, 151, 20))
        self.herolist.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.herolist.setEditable(True)
        self.herolist.setCurrentText("")
        self.herolist.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.herolist.setMinimumContentsLength(12)
        self.herolist.setObjectName("herolist")
        self.checkBox = QtWidgets.QCheckBox(Frame)
        self.checkBox.setGeometry(QtCore.QRect(220, 20, 169, 16))
        self.checkBox.setObjectName("checkBox")
        self.heroedit = QtWidgets.QLineEdit(Frame)
        self.heroedit.setGeometry(QtCore.QRect(370, 60, 201, 20))
        self.heroedit.setObjectName("heroedit")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)
     #   Frame.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.Start.setText(_translate("Frame", "开始游戏"))
        self.name.setText(_translate("Frame", "游戏名字"))
        self.Gongao.setHtml(_translate("Frame",
                                       "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                       "p, li { white-space: pre-wrap; }\n"
                                       "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                       "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.xzdj.setText(_translate("Frame", "寻找对局"))
        self.zdjs.setText(_translate("Frame", "自动接受"))
        self.label.setText(_translate("Frame", "启动方式:"))
        self.radioButton.setText(_translate("Frame", "Wegame"))
        self.radioButton_2.setText(_translate("Frame", "客户端"))
        self.pushButton_5.setText(_translate("Frame", "创建房间"))
        self.pushButton.setText(_translate("Frame", "皮肤原画获取"))
        self.profile.setText(_translate("Frame", "头像"))
        self.checkBox_5.setText(_translate("Frame", "对局详情"))
        self.checkBox_4.setText(_translate("Frame", "一键天赋"))
        self.pushButton_6.setText(_translate("Frame", "战绩查询"))
        self.pushButton_3.setText(_translate("Frame", "更改生涯背景"))
        self.pushButton_4.setText(_translate("Frame", "更改状态"))
        self.pushButton_2.setText(_translate("Frame", "黑屏"))
        self.checkBox.setText(_translate("Frame", "秒选英雄"))
        # 这一行就是来设置窗口始终在顶端的。
