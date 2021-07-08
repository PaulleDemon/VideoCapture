import sys
from PySide6 import QtWidgets
from SplitterWidget import SplitterWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    win = SplitterWindow()
    win.setWindowTitle("Video Capture")

    with open("Theme.qss", 'r') as read:
        win.setStyleSheet(read.read())

    win.show()

    sys.exit(app.exec())

