import sys
from PySide6 import QtWidgets, QtCore, QtGui


class ControlPanel(QtWidgets.QWidget):
    # widget that is use to save image, capture image, draw rect etc.

    capture = QtCore.Signal(bool)  # sends signal when capture button is pressed
    drawRect = QtCore.Signal(bool) # sends signal when draw rect is pressed

    def __init__(self, *args, **kwargs):
        super(ControlPanel, self).__init__(*args, **kwargs)

        self.capturing = False
        self.drawingRect = False

        self.setLayout(QtWidgets.QVBoxLayout())

        self.capturedFrame = QtWidgets.QFrame(self)
        self.capturedFrame.setLayout(QtWidgets.QVBoxLayout())

        self.captured_img = QtWidgets.QLabel()
        self.captured_img.setScaledContents(True)
        self.setMinimumSize(300, 250)
        self.captured_img.setMaximumHeight(300)

        self.captured_img_dimensions = QtWidgets.QLabel()

        self.label_edit = QtWidgets.QLineEdit()
        self.saveImage = QtWidgets.QPushButton("Save Captured Image")

        self.capturedFrame.layout().addWidget(self.captured_img)
        self.capturedFrame.layout().addWidget(self.captured_img_dimensions)
        self.capturedFrame.layout().addWidget(self.label_edit)
        self.capturedFrame.layout().addWidget(self.saveImage)

        self.capturedFrame.hide()

        self.draw_rect = QtWidgets.QPushButton("Capture Frame")
        self.draw_rect.setDisabled(True)
        self.draw_rect.clicked.connect(self.draw)

        self.camera_capture = QtWidgets.QPushButton("Start Capture")
        self.camera_capture.clicked.connect(self.toggleVideoCapture)

        self.layout().addWidget(self.capturedFrame)
        self.layout().addWidget(self.draw_rect)
        self.layout().addWidget(self.camera_capture)

        self.layout().addStretch(1)

    def toggleVideoCapture(self):  # starts and stops video capture
        self.capturing = not self.capturing

        if self.capturing:
            self.draw_rect.setDisabled(False)
            self.camera_capture.setText("Stop Capturing")

        else:
            self.draw_rect.setDisabled(True)
            self.camera_capture.setText("Start Capturing")

        self.capture.emit(self.capturing)

    def draw(self):  # emits signal when draw button is pressed
        self.drawingRect = not self.drawingRect
        self.drawRect.emit(self.drawingRect)

    def resetDraw(self):
        self.drawingRect = False

    def setCapturedImage(self, img: QtGui.QPixmap):  # shows the captured image in the widget
        self.captured_img_dimensions.setText(f"{img.width()} X {img.height()}")
        self.captured_img.setPixmap(img)
        self.showCaptureOptions()
        self.resetDraw()

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