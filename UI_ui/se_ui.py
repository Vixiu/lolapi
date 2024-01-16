# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'se_ui.ui'
#
# Created by: PyQt5 UI_ui code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPropertyAnimation, Qt, QPoint
from PyQt5.QtGui import QIcon


class Ui_form(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.summoner = None
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | 0x80)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.detail.clicked.connect(self.detail_clicked)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowOpacity(0.9)
        self.summoner.adjustSize()
        self.animation = QPropertyAnimation(self.summoner, b'pos')
        self.animation.setDuration(100)

    def detail_clicked(self):
        self.total_number.setText("93900场")
        self.summoner.adjustSize()
        self.summoner.adjustSize()

    def pushButton_clicked(self):

        x = self.summoner.pos().x()
        if x == 0:
            end_pos = QPoint(-self.summoner.width() + self.pushButton.width() + 4, 0)
            self.animation.setEndValue(end_pos)
            self.pushButton.setIcon(QIcon("C:/Users/lnori/Desktop/right.png"))

        else:
            self.animation.setEndValue(QPoint(0, 0))
            self.pushButton.setIcon(QIcon("C:/Users/lnori/Desktop/left.png"))

        self.animation.start()

    def setupUi(self, form):

        self.summoner = QtWidgets.QWidget(form)
        self.summoner.setGeometry(QtCore.QRect(0, 0, 331, 100))
        self.summoner.setMaximumSize(QtCore.QSize(16777215, 100))
        self.summoner.setStyleSheet("QWidget#summoner{\n"
                                    "background-color:rgb(248, 249, 250);\n"
                                    "border: 1px solid rgb(179, 179, 179) ;\n"
                                    "border-style:solid;\n"
                                    "border-bottom-right-radius:10px;\n"
                                    "border-top-right-radius:10px;\n"
                                    "}")
        self.summoner.setObjectName("summoner")
        self.layoutWidget = QtWidgets.QWidget(self.summoner)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 321, 102))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.summoner)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(6, -1, -1, -1)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.recently = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.recently.setFont(font)
        self.recently.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.recently.setObjectName("recently")
        self.verticalLayout.addWidget(self.recently)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.total_number = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.total_number.setFont(font)
        self.total_number.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.total_number.setObjectName("total_number")
        self.horizontalLayout.addWidget(self.total_number)
        self.total_rate = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.total_rate.setFont(font)
        self.total_rate.setObjectName("total_rate")
        self.horizontalLayout.addWidget(self.total_rate)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.recently_worl = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.recently_worl.setFont(font)
        self.recently_worl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.recently_worl.setObjectName("recently_worl")
        self.horizontalLayout_2.addWidget(self.recently_worl)
        self.recently_rate = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.recently_rate.setFont(font)
        self.recently_rate.setObjectName("recently_rate")
        self.horizontalLayout_2.addWidget(self.recently_rate)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.hero_number = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.hero_number.setFont(font)
        self.hero_number.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.hero_number.setObjectName("hero_number")
        self.horizontalLayout_3.addWidget(self.hero_number)
        self.hero_rate = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.hero_rate.setFont(font)
        self.hero_rate.setObjectName("hero_rate")
        self.horizontalLayout_3.addWidget(self.hero_rate)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.rank = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.rank.setFont(font)
        self.rank.setAlignment(QtCore.Qt.AlignCenter)
        self.rank.setObjectName("rank")
        self.verticalLayout_3.addWidget(self.rank)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
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
        self.horizontalLayout_6.addWidget(self.detail)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.session_value_5 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.session_value_5.setFont(font)
        self.session_value_5.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.session_value_5.setObjectName("session_value_5")
        self.horizontalLayout_4.addWidget(self.session_value_5)
        self.hero_worl = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.hero_worl.setFont(font)
        self.hero_worl.setObjectName("hero_worl")
        self.horizontalLayout_4.addWidget(self.hero_worl)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setMaximumSize(QtCore.QSize(23, 80))
        self.pushButton.setStyleSheet("QPushButton {\n"
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
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/lnori/Desktop/left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(23, 70))
        self.pushButton.setAutoRepeatDelay(292)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_5.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(1, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "Form"))
        self.label_2.setText(_translate("form", "总 览:"))
        self.recently.setText(_translate("form", "近20场:"))
        self.label_3.setText(_translate("form", "英 雄:"))
        self.total_number.setText(_translate("form", "9999场"))
        self.total_rate.setText(_translate("form", "100%"))
        self.recently_worl.setText(_translate("form", "99胜99负"))
        self.recently_rate.setText(_translate("form", "100%"))
        self.hero_number.setText(_translate("form", "993场"))
        self.hero_rate.setText(_translate("form", "100%"))
        self.rank.setText(_translate("form", "青铜IV34"))
        self.detail.setText(_translate("form", "详情"))
        self.session_value_5.setText(_translate("form", "近期:"))
        self.hero_worl.setText(_translate("form", "99胜99负"))