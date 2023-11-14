import sys
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QRect
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 300, 200)

        self.button = QPushButton('展开/收缩窗口', self)
        self.button.clicked.connect(self.toggleWindow)

        self.windowExpanded = False

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def toggleWindow(self):
        startGeometry = self.geometry()
        endGeometry = QRect()

        if not self.windowExpanded:
            endGeometry = QRect(startGeometry.x(), startGeometry.y(), startGeometry.width(), startGeometry.height() + 200)
        else:
            endGeometry = QRect(startGeometry.x(), startGeometry.y(), startGeometry.width(), startGeometry.height() - 200)

        animation = QPropertyAnimation(self, b"geometry")
        animation.setDuration(500)
        animation.setEasingCurve(QEasingCurve.InOutQuart)
        animation.setStartValue(startGeometry)
        animation.setEndValue(endGeometry)
        animation.start()

        self.windowExpanded = not self.windowExpanded

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
