import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget


class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 创建一个主窗口
        self.setWindowTitle('自动调整主窗口大小')

        # 创建一个包含标签的部件
        widget = QWidget(self)
        layout = QVBoxLayout(widget)

        label = QLabel('一些文本内容', self)
        layout.addWidget(label)

        # 设置主窗口的中央部件
        self.setCentralWidget(widget)

        # 调整主窗口大小以适应内容
        self.adjustSize()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
