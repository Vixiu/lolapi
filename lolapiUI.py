# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lolapiUI.ui'
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
        Frame.resize(1052, 624)
        Frame.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.widget_1 = QtWidgets.QWidget(Frame)
        self.widget_1.setGeometry(QtCore.QRect(160, 50, 581, 481))
        self.widget_1.setStyleSheet("QWidget#Button_X {\n"
"            border-width:0px 0px 0px 0px; \n"
"   \n"
"}\n"
"QWidget#Button_min{\n"
"border-width:0px 0px 0px 0px; \n"
"}\n"
"QWidget#widget_1{\n"
"background-color:#f8f9fa;\n"
"border-radius:10px;\n"
"border: 5px, white;\n"
"margin: 5px;\n"
"}\n"
"QPushButton {\n"
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
"QRadioButton {\n"
"    spacing: 8px;\n"
"}\n"
"QGroupBox::title,\n"
"QAbstractItemView::item {\n"
"    spacing: 6px;\n"
"}\n"
"QCheckBox::indicator,\n"
"QGroupBox::indicator,\n"
"QAbstractItemView::indicator,\n"
"QRadioButton::indicator {\n"
"    height: 18px;\n"
"    width: 18px;\n"
"}\n"
"QCheckBox::indicator,\n"
"QGroupBox::indicator,\n"
"\n"
"QCheckBox::indicator:unchecked:disabled,\n"
"QGroupBox::indicator:unchecked:disabled,\n"
"\n"
"QCheckBox::indicator:checked,\n"
"QGroupBox::indicator:checked,\n"
"\n"
"QCheckBox::indicator:checked:disabled,\n"
"QGroupBox::indicator:checked:disabled,\n"
"\n"
"QCheckBox::indicator:indeterminate,\n"
"\n"
"QCheckBox::indicator:indeterminate:disabled,\n"
"\n"
"")
        self.widget_1.setObjectName("widget_1")
        self.dial = QtWidgets.QDial(self.widget_1)
        self.dial.setEnabled(False)
        self.dial.setGeometry(QtCore.QRect(530, 430, 41, 41))
        self.dial.setMouseTracking(False)
        self.dial.setAutoFillBackground(False)
        self.dial.setMaximum(100)
        self.dial.setSingleStep(5)
        self.dial.setProperty("value", 0)
        self.dial.setSliderPosition(0)
        self.dial.setWrapping(False)
        self.dial.setNotchTarget(8.7)
        self.dial.setNotchesVisible(False)
        self.dial.setObjectName("dial")
        self.Gongao = QtWidgets.QTextBrowser(self.widget_1)
        self.Gongao.setEnabled(False)
        self.Gongao.setGeometry(QtCore.QRect(240, 260, 321, 161))
        self.Gongao.setToolTipDuration(10000)
        self.Gongao.setObjectName("Gongao")
        self.label = QtWidgets.QLabel(self.widget_1)
        self.label.setGeometry(QtCore.QRect(40, 410, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(self.widget_1)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 220, 141, 111))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButton_6 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_4.addWidget(self.pushButton_6)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_4.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setToolTip("")
        self.pushButton_4.setToolTipDuration(10000)
        self.pushButton_4.setStatusTip("")
        self.pushButton_4.setWhatsThis("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_4.addWidget(self.pushButton_4)
        self.state = QtWidgets.QLabel(self.widget_1)
        self.state.setGeometry(QtCore.QRect(240, 440, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.state.setFont(font)
        self.state.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.state.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.state.setText("")
        self.state.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.state.setObjectName("state")
        self.layoutWidget1 = QtWidgets.QWidget(self.widget_1)
        self.layoutWidget1.setGeometry(QtCore.QRect(500, 4, 61, 41))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Button_min = QtWidgets.QPushButton(self.layoutWidget1)
        self.Button_min.setObjectName("Button_min")
        self.horizontalLayout.addWidget(self.Button_min)
        self.Button_X = QtWidgets.QPushButton(self.layoutWidget1)
        self.Button_X.setStyleSheet("")
        self.Button_X.setObjectName("Button_X")
        self.horizontalLayout.addWidget(self.Button_X)
        self.layoutWidget2 = QtWidgets.QWidget(self.widget_1)
        self.layoutWidget2.setGeometry(QtCore.QRect(120, 410, 82, 45))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton_2 = QtWidgets.QRadioButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setIconSize(QtCore.QSize(22, 16))
        self.radioButton_2.setChecked(True)
        self.radioButton_2.setAutoRepeat(False)
        self.radioButton_2.setAutoExclusive(True)
        self.radioButton_2.setAutoRepeatDelay(100)
        self.radioButton_2.setAutoRepeatInterval(10)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout.addWidget(self.radioButton_2)
        self.radioButton = QtWidgets.QRadioButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout.addWidget(self.radioButton)
        self.Start = QtWidgets.QPushButton(self.widget_1)
        self.Start.setEnabled(True)
        self.Start.setGeometry(QtCore.QRect(40, 350, 161, 51))
        self.Start.setObjectName("Start")
        self.line_2 = QtWidgets.QFrame(self.widget_1)
        self.line_2.setGeometry(QtCore.QRect(230, 240, 341, 5))
        self.line_2.setMaximumSize(QtCore.QSize(16777215, 5))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line = QtWidgets.QFrame(self.widget_1)
        self.line.setEnabled(True)
        self.line.setGeometry(QtCore.QRect(222, 10, 5, 460))
        self.line.setMaximumSize(QtCore.QSize(5, 16777215))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.layoutWidget3 = QtWidgets.QWidget(self.widget_1)
        self.layoutWidget3.setGeometry(QtCore.QRect(340, 60, 181, 101))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget3)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_2.addWidget(self.pushButton_5)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget3)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.herolist = QtWidgets.QComboBox(self.widget_1)
        self.herolist.setEnabled(False)
        self.herolist.setGeometry(QtCore.QRect(330, 30, 171, 20))
        self.herolist.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.herolist.setEditable(True)
        self.herolist.setCurrentText("")
        self.herolist.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.herolist.setMinimumContentsLength(12)
        self.herolist.setObjectName("herolist")
        self.label_3 = QtWidgets.QLabel(self.widget_1)
        self.label_3.setGeometry(QtCore.QRect(50, 30, 141, 141))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("D:/lol-api/lol/icon/图层 2.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.profile = QtWidgets.QLabel(self.widget_1)
        self.profile.setGeometry(QtCore.QRect(50, 30, 141, 141))
        self.profile.setText("")
        self.profile.setPixmap(QtGui.QPixmap("C:/Users/lnori/Desktop/4804.jpg"))
        self.profile.setScaledContents(True)
        self.profile.setObjectName("profile")
        self.name = QtWidgets.QLabel(self.widget_1)
        self.name.setGeometry(QtCore.QRect(10, 180, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.name.setFont(font)
        self.name.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.name.setAutoFillBackground(False)
        self.name.setTextFormat(QtCore.Qt.AutoText)
        self.name.setScaledContents(True)
        self.name.setAlignment(QtCore.Qt.AlignCenter)
        self.name.setObjectName("name")
        self.layoutWidget4 = QtWidgets.QWidget(self.widget_1)
        self.layoutWidget4.setGeometry(QtCore.QRect(250, 20, 91, 161))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkBox = QtWidgets.QCheckBox(self.layoutWidget4)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_3.addWidget(self.checkBox)
        self.xzdj = QtWidgets.QCheckBox(self.layoutWidget4)
        self.xzdj.setObjectName("xzdj")
        self.verticalLayout_3.addWidget(self.xzdj)
        self.zdjs = QtWidgets.QCheckBox(self.layoutWidget4)
        self.zdjs.setChecked(True)
        self.zdjs.setTristate(False)
        self.zdjs.setObjectName("zdjs")
        self.verticalLayout_3.addWidget(self.zdjs)
        self.checkBox_5 = QtWidgets.QCheckBox(self.layoutWidget4)
        self.checkBox_5.setEnabled(False)
        self.checkBox_5.setCheckable(True)
        self.checkBox_5.setChecked(True)
        self.checkBox_5.setAutoRepeat(False)
        self.checkBox_5.setObjectName("checkBox_5")
        self.verticalLayout_3.addWidget(self.checkBox_5)
        self.checkBox_4 = QtWidgets.QCheckBox(self.layoutWidget4)
        self.checkBox_4.setEnabled(False)
        self.checkBox_4.setMouseTracking(True)
        self.checkBox_4.setCheckable(True)
        self.checkBox_4.setChecked(True)
        self.checkBox_4.setObjectName("checkBox_4")
        self.verticalLayout_3.addWidget(self.checkBox_4)
        self.profile.raise_()
        self.dial.raise_()
        self.Gongao.raise_()
        self.label.raise_()
        self.layoutWidget.raise_()
        self.state.raise_()
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.Start.raise_()
        self.line_2.raise_()
        self.line.raise_()
        self.layoutWidget.raise_()
        self.herolist.raise_()
        self.label_3.raise_()
        self.name.raise_()
        self.layoutWidget.raise_()

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.Gongao.setToolTip(_translate("Frame", "ninn"))
        self.Gongao.setHtml(_translate("Frame", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label.setText(_translate("Frame", "启动方式："))
        self.pushButton_6.setText(_translate("Frame", "战绩查询"))
        self.pushButton_3.setText(_translate("Frame", "更改生涯背景"))
        self.pushButton_4.setText(_translate("Frame", "更改右侧状态"))
        self.Button_min.setText(_translate("Frame", "-"))
        self.Button_X.setText(_translate("Frame", "X"))
        self.radioButton_2.setText(_translate("Frame", "客户端"))
        self.radioButton.setText(_translate("Frame", "WeGame"))
        self.Start.setText(_translate("Frame", "开始游戏"))
        self.pushButton_5.setText(_translate("Frame", "创建房间"))
        self.pushButton.setText(_translate("Frame", "资源获取(皮肤原画,图标等)"))
        self.name.setText(_translate("Frame", "游戏名字"))
        self.checkBox.setText(_translate("Frame", "秒选英雄"))
        self.xzdj.setText(_translate("Frame", "寻找对局"))
        self.zdjs.setText(_translate("Frame", "自动接受"))
        self.checkBox_5.setText(_translate("Frame", "对局详情"))
        self.checkBox_4.setText(_translate("Frame", "一键天赋"))
