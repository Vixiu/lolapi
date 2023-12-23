import sys



import qdarktheme
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

app = QApplication(sys.argv)
# Apply the complete dark theme to your Qt App.
qdarktheme.setup_theme(theme= "light")

main_win = QMainWindow()
push_button = QPushButton("PyQtDarkTheme!!")
main_win.setCentralWidget(push_button)

main_win.show()

app.exec()