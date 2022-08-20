import random
import sys
import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QCompleter
from pypinyin import lazy_pinyin
import Fuwen
import lolapi

from Lcu import LcuRequest, LcuThread


def add_text(_str):
    """
    :param _str: 内容
    :return:
    """
    ui.Gongao.append("<font color='{color}' size='4'>".format(color=randomcolor()) + _str + "<font>")


def set_text(_str, color):
    charlist = ['', '>', '>>', '>>>', '>>>>']
    ui.Gongao.setText(
        "<font color=" + color + " size='6'>" + _str + charlist[round(time.time()) % len(charlist)] + "<font>")


def randomcolor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color


def zdjs(state):
    if state == 0:
        qthread.acceptflag = False
        ui.Gongao.append("<font color='{color}'>".format(color=randomcolor()) + '自动接受>>>已关闭' + "<font>")
    else:
        qthread.acceptflag = True
        ui.Gongao.append("<font color='{color}'>".format(color=randomcolor()) + '自动接受>>>已开启' + "<font>")


def choosehero(state):
    if state == 0:
        qthread.herochoose = -1
        ui.Gongao.append("<font color='{color}'>".format(color=randomcolor()) + '秒抢>>>已关闭' + "<font>")
    else:
        qthread.herochoose = herolist[ui.herolist.currentText()]['id']
        ui.Gongao.append(
            "<font color='{color}'>".format(color=randomcolor()) + '秒抢>>>' + ui.herolist.currentText() + "<font>")


def scr(userlist):
    pixmapa = QPixmap(QImage.fromData(
        lcu.getdata('/lol-game-data/assets/v1/profile-icons/' + str(userlist['profileIconId']) + '.jpg').content))
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


def load():
    global herolist, userlist
    herolist = {}
    userlist = lcu.getdata('/lol-summoner/v1/current-summoner').json()
    # print(userlist)
    ui.name.setText(userlist['internalName'])
    ui.profile.setPixmap(scr(userlist))  # 圆形头像
    for i in lcu.getdata('/lol-champions/v1/owned-champions-minimal').json():
        herolist[i['name'] + ' - ' + i['title']] = {
            "squarePortraitPath": i['squarePortraitPath'],
            "id": i['id']
        }
    # print(herolist)
    ui.herolist.clear()
    ui.herolist.addItems(sorted(herolist.keys(), key=lambda x: lazy_pinyin(x)))  # 列表内添加英雄
    completer = QCompleter(herolist.keys())
    completer.setFilterMode(Qt.MatchContains)
    ui.herolist.setCompleter(completer)
    # ui.herolist.completer('')
    add_text('用户信息获取完毕!')


def shero(sate):
    if qthread.herochoose > -1:
        qthread.herochoose = herolist[sate]['id']
        ui.Gongao.append("<font color='{color}'>".format(color=randomcolor()) + '秒抢>>>' + sate + "<font>")
    ui.profile.setPixmap(scr(userlist))


def test(i):
    for j in herolist:
        if herolist[j]['id'] == i:
            uis.hero_avatar.setPixmap(QPixmap(QImage.fromData(lcu.getdata(herolist[j]['squarePortraitPath']).content)))
            uis.hero_name.setText(j)





herolist = {}
userlist = {}

lolpath = 'F:\\1\\英雄联盟-\\LeagueClient'

lcu = LcuRequest(lolpath)
qthread = LcuThread(lcu)
qthread.start()

# userlist = lcu.getdata('/lol-summoner/v1/current-summoner').json()
# query='/lol-lobby/v2/lobby/matchmaking/search'   #寻找对局
# query='/lol-matchmaking/v1/ready-check/accept' #接受
# /lol-summoner/v1/current-summoner 状态
# /lol-summoner/v1/summoners/4118336138 名字

app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = lolapi.Ui_Frame()
ui.setupUi(MainWindow)

MainWindow.show()

##fuwenmain = QDialog()
fuwenmain = QMainWindow()
uis = Fuwen.Ui_FuWen()
uis.setupUi(fuwenmain)
# fuwenmain.show()
# Frame.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint) 置顶
###############################################################
ui.herolist.highlighted[str].connect(
    lambda s: ui.profile.setPixmap(QPixmap(QImage.fromData(lcu.getdata(herolist[s]['squarePortraitPath']).content))))
ui.zdjs.stateChanged.connect(lambda s: zdjs(s))
ui.herolist.activated[str].connect(lambda s: shero(s))

ui.checkBox.stateChanged.connect(lambda s: choosehero(s))

# ui.herolist.editTextChanged.connect(lambda s:print(s))

ui.herolist.currentIndexChanged.connect(lambda s: print(s))

###############################################################
qthread.add_text.connect(add_text)
qthread.set_text.connect(set_text)
qthread.test.connect(test)
qthread.gameLoad.connect(load)  # 载入
qthread.window_enable.connect(lambda b: MainWindow.setEnabled(b))
###############################################################
app.exec_()  # 开始
qthread.stop = False  # 线程退出
