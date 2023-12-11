import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QDialog, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Main Window')

        self.central_widget = QLabel('This is the main window')
        self.setCentralWidget(self.central_widget)

        self.button = QPushButton('Open Dialog', self)
        self.button.clicked.connect(self.open_dialog)

    def open_dialog(self):
        dialog = Dialog()
        dialog.exec_()


class Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Dialog')

        self.label = QLabel('This is a dialog')
        self.button = QPushButton('Close Dialog', self)
        self.button.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
