import sys

from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication


class GifButton(QWidget):
    def __init__(self):
        super(GifButton, self).__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 创建一个 QPushButton
        self.gif_button = QPushButton(self)
        self.gif_button.setFixedSize(100, 50)  # 设置按钮大小

        # 创建一个 QMovie 并设置要播放的 GIF 文件路径
        self.movie =  QMovie(r"C:\Users\lnori\Desktop\a9825517750145ce88cf60bd3b1a540f.gif")

        # 将 QMovie 设置给 QPushButton
        self.gif_button.movie = self.movie

        # 连接 QMovie 的帧变化信号到自定义的槽函数
        self.movie.frameChanged.connect(self.update_button_style)

        # 连接按钮的 clicked 信号到自定义的槽函数
        self.gif_button.clicked.connect(self.on_button_clicked)

        layout.addWidget(self.gif_button)

        self.setLayout(layout)
        self.setWindowTitle('GIF Button')
        self.setGeometry(300, 300, 150, 100)

    def on_button_clicked(self):
        # 在按钮点击时开始播放 GIF
        self.movie.start()

    def update_button_style(self):
        # 手动更新按钮的样式，以显示当前帧的图像
        self.gif_button.setStyleSheet(
            f"QPushButton {{background-image: url({self.movie.currentPixmap().toImage().cacheKey()});}}"
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gif_button = GifButton()
    gif_button.show()
    sys.exit(app.exec_())
