import sys
from PySide6 import QtWidgets, QtCore, QtGui


class ControlPanel(QtWidgets.QWidget):

    capture = QtCore.Signal(bool)
    drawRect = QtCore.Signal(bool)

    def __init__(self, *args, **kwargs):
        super(ControlPanel, self).__init__(*args, **kwargs)

        self.capturing = False
        self.drawingRect = False

        self.setLayout(QtWidgets.QVBoxLayout())

        self.capturedFrame = QtWidgets.QFrame(self)
        self.capturedFrame.setLayout(QtWidgets.QVBoxLayout())

        self.captured_img = QtWidgets.QLabel()
        self.setMinimumSize(250, 100)
        self.captured_img.setMaximumHeight(300)
        self.label_edit = QtWidgets.QLineEdit()
        self.saveImage = QtWidgets.QPushButton("Save Captured Image")

        self.capturedFrame.layout().addWidget(self.captured_img)
        self.capturedFrame.layout().addWidget(self.label_edit)
        self.capturedFrame.layout().addWidget(self.saveImage)

        self.capturedFrame.hide()

        self.draw_rect = QtWidgets.QPushButton("Capture Frame")
        self.draw_rect.setDisabled(True)
        self.draw_rect.clicked.connect(self.drawRect)

        self.camera_capture = QtWidgets.QPushButton("Start Capture")
        self.camera_capture.clicked.connect(self.changeCapture)

        self.layout().addWidget(self.capturedFrame)
        self.layout().addWidget(self.draw_rect)
        self.layout().addWidget(self.camera_capture)

        self.layout().addStretch(1)

    def changeCapture(self):
        self.capturing = not self.capturing

        if self.capturing:
            self.draw_rect.setDisabled(False)
            self.camera_capture.setText("Stop Capturing")

        else:
            self.draw_rect.setDisabled(True)
            self.camera_capture.setText("Start Capturing")

        self.capture.emit(self.capturing)

    def draw(self):
        self.drawingRect = not self.drawingRect
        self.drawRect.emit(self.drawingRect)

    def updateCapturedImage(self, img: QtGui.QPixmap):
        self.captured_img.setPixmap(img)

    def showCaptureOptions(self):
        self.capturedFrame.show()

    def hideCaptureOptions(self):
        self.capturedFrame.hide()

    def saveLabel(self):
        pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    win = ControlPanel()
    win.show()

    sys.exit(app.exec())