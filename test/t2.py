import time

from PyQt5.QtCore import QThread


class LcuThread(QThread):
    def __init__(self):
        super().__init__()
        print(1)

    def run(self) -> None:
        time.sleep(3)
        print(2)

    def st(self) -> None:
        print(3)
        self.start()


qt = LcuThread()

qt.st()
print('end')
while True:
    pass
qt.wait()
