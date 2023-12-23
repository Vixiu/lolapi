from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt
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


class MathDetails(QDialog):
    def __init__(self, windows):
        super().__init__(windows)
    #  self.setupUi(self)
