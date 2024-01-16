import win32gui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint

from PyQt5 import QtCore, QtGui, QtWidgets

from lolapiUI import Ui_Frame
from setting import Ui_Dialog


class InvisibleWidget(QWidget):
    def __init__(self):
        super().__init__()
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


class InvisibleDialog(QDialog):
    def __init__(self, windows):
        super().__init__(windows)
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


class MainWindow(InvisibleWidget, Ui_Frame):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class Toolbox(InvisibleDialog, Ui_Dialog):
    def __init__(self, windows):
        super().__init__(windows)
        self.setupUi(self)


class SummonerUI:
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
        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.Minimum)
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


class MatchDialog(QDialog, SummonerUI):
    instances = []  # 存储所有实例的引用
    timer: QTimer = None  # 共享的定时器

    def __init__(self, windows=None):
        super().__init__(windows)
        self.setupUi(self)
        self.X = 0  # 相对偏移
        self.Y = 0  # 相对偏移
        # 无边框标题设置
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() | 0x80)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # 按钮事件
        self.shrink.clicked.connect(self.shrink_clicked)
        self.detail.clicked.connect(self.detail_clicked)
        self.__class__.instances.append(self)
        if self.__class__.timer is None:
            # 如果定时器不存在，创建一个新的定时器
            self.__class__.timer = QTimer(self)
            self.__class__.timer.timeout.connect(self.follow_window)
            self.__class__.timer.start(10)  # 设置定时器间隔为1秒
        # 收缩动画
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowOpacity(0.9)
        self.animation = QPropertyAnimation(self.summoner, b'pos')
        self.animation.setDuration(100)

    def set_offset(self, x, y):
        self.X, self.Y = x, y

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

    @staticmethod
    def follow_window():
        hwnd = win32gui.FindWindow(None, 'League of Legends')
        if hwnd:
            rect = win32gui.GetWindowRect(hwnd)
            for instance in MatchDialog.instances:
                #    print(rect, id(hwnd))
                instance.move(rect[0] + instance.X, rect[1] + instance.Y)
