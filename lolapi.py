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
        Frame.resize(717, 447)
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
        self.Gongao.setGeometry(QtCore.QRect(200, 240, 391, 161))
        self.Gongao.setObjectName("Gongao")
        self.layoutWidget = QtWidgets.QWidget(Frame)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 410, 186, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.radioButton = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout.addWidget(self.radioButton_2)
        self.layoutWidget1 = QtWidgets.QWidget(Frame)
        self.layoutWidget1.setGeometry(QtCore.QRect(460, 20, 160, 83))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_2.addWidget(self.pushButton_5)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
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
        self.label_3.setGeometry(QtCore.QRect(10, 50, 181, 121))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("C:/Users/lnori/Desktop/lol-wangz/challenger.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.layoutWidget2 = QtWidgets.QWidget(Frame)
        self.layoutWidget2.setGeometry(QtCore.QRect(200, 110, 143, 71))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkBox_5 = QtWidgets.QCheckBox(self.layoutWidget2)
        self.checkBox_5.setEnabled(False)
        self.checkBox_5.setCheckable(True)
        self.checkBox_5.setChecked(True)
        self.checkBox_5.setAutoRepeat(False)
        self.checkBox_5.setObjectName("checkBox_5")
        self.verticalLayout_3.addWidget(self.checkBox_5)
        self.checkBox_4 = QtWidgets.QCheckBox(self.layoutWidget2)
        self.checkBox_4.setEnabled(False)
        self.checkBox_4.setMouseTracking(True)
        self.checkBox_4.setCheckable(True)
        self.checkBox_4.setChecked(True)
        self.checkBox_4.setObjectName("checkBox_4")
        self.verticalLayout_3.addWidget(self.checkBox_4)
        self.layoutWidget3 = QtWidgets.QWidget(Frame)
        self.layoutWidget3.setGeometry(QtCore.QRect(30, 200, 141, 121))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButton_6 = QtWidgets.QPushButton(self.layoutWidget3)
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_4.addWidget(self.pushButton_6)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget3)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_4.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget3)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_4.addWidget(self.pushButton_4)
        self.checkBox = QtWidgets.QCheckBox(Frame)
        self.checkBox.setGeometry(QtCore.QRect(200, 20, 169, 16))
        self.checkBox.setObjectName("checkBox")
        self.zdjs = QtWidgets.QCheckBox(Frame)
        self.zdjs.setGeometry(QtCore.QRect(200, 80, 178, 16))
        self.zdjs.setObjectName("zdjs")
        self.xzdj = QtWidgets.QCheckBox(Frame)
        self.xzdj.setGeometry(QtCore.QRect(200, 50, 178, 16))
        self.xzdj.setObjectName("xzdj")
        self.herolist = QtWidgets.QComboBox(Frame)
        self.herolist.setEnabled(True)
        self.herolist.setGeometry(QtCore.QRect(270, 20, 178, 20))
        self.herolist.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.herolist.setEditable(True)
        self.herolist.setCurrentText("")
        self.herolist.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.herolist.setMinimumContentsLength(12)
        self.herolist.setObjectName("herolist")
        self.line_2 = QtWidgets.QFrame(Frame)
        self.line_2.setGeometry(QtCore.QRect(190, 210, 401, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.pushButton_7 = QtWidgets.QPushButton(Frame)
        self.pushButton_7.setGeometry(QtCore.QRect(430, 410, 75, 23))
        self.pushButton_7.setObjectName("pushButton_7")
        self.help = QtWidgets.QPushButton(Frame)
        self.help.setGeometry(QtCore.QRect(510, 410, 75, 23))
        self.help.setObjectName("help")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.Start.setText(_translate("Frame", "开始游戏"))
        self.name.setText(_translate("Frame", "游戏名字"))
        self.Gongao.setHtml(_translate("Frame", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label.setText(_translate("Frame", "启动方式:"))
        self.radioButton.setText(_translate("Frame", "Wegame"))
        self.radioButton_2.setText(_translate("Frame", "客户端"))
        self.pushButton_5.setText(_translate("Frame", "创建房间"))
        self.pushButton.setText(_translate("Frame", "资源获取(皮肤原画,图标等)"))
        self.pushButton_2.setText(_translate("Frame", "黑屏"))
        self.profile.setText(_translate("Frame", "头像"))
        self.checkBox_5.setText(_translate("Frame", "对局详情"))
        self.checkBox_4.setText(_translate("Frame", "一键天赋"))
        self.pushButton_6.setText(_translate("Frame", "战绩查询"))
        self.pushButton_3.setText(_translate("Frame", "更改生涯背景"))
        self.pushButton_4.setText(_translate("Frame", "更改状态"))
        self.checkBox.setText(_translate("Frame", "秒选英雄"))
        self.zdjs.setText(_translate("Frame", "自动接受"))
        self.xzdj.setText(_translate("Frame", "寻找对局"))
        self.pushButton_7.setText(_translate("Frame", "设置"))
        self.help.setText(_translate("Frame", "帮助"))
