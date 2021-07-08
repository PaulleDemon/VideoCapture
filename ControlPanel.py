import os.path
import sys
from PySide6 import QtWidgets, QtCore, QtGui
from pygrabber.PyGrabber import PyGrabber


class ControlPanel(QtWidgets.QWidget):
    # widget that is use to save image, capture image, draw rect etc.

    capture = QtCore.Signal(bool)  # sends signal when capture button is pressed
    drawRect = QtCore.Signal(bool)  # sends signal when draw rect is pressed
    cameraChanged = QtCore.Signal(int)

    def __init__(self, *args, **kwargs):
        super(ControlPanel, self).__init__(*args, **kwargs)

        self.capturing = False
        self.drawingRect = False
        self.capturedImage: QtGui.QImage = QtGui.QImage()

        self.setLayout(QtWidgets.QVBoxLayout())

        self.capturedFrame = QtWidgets.QFrame(self)
        self.capturedFrame.setLayout(QtWidgets.QVBoxLayout())

        self.captured_img_lbl = QtWidgets.QLabel()
        self.captured_img_lbl.setScaledContents(True)
        self.setMinimumSize(300, 250)
        self.captured_img_lbl.setMaximumHeight(300)

        self.captured_img_dimensions = QtWidgets.QLabel()

        self.error_lbl = QtWidgets.QLabel(objectName="ErrorLabel")
        self.error_lbl.setWordWrap(True)

        self.directory_edit = QtWidgets.QLineEdit()
        self.directory_edit.setPlaceholderText("Set output folder")

        self.save_as_lbl = QtWidgets.QLineEdit()
        self.save_as_lbl.setPlaceholderText("Set image name")

        self.saveImage = QtWidgets.QPushButton("Save Captured Image", clicked=self.save)

        self.capturedFrame.layout().addWidget(self.captured_img_lbl)
        self.capturedFrame.layout().addWidget(self.captured_img_dimensions)
        self.capturedFrame.layout().addWidget(self.error_lbl)
        self.capturedFrame.layout().addWidget(self.directory_edit)
        self.capturedFrame.layout().addWidget(self.save_as_lbl)
        self.capturedFrame.layout().addWidget(self.saveImage)

        self.capturedFrame.hide()

        self.camera_devices = QtWidgets.QComboBox()
        self.camera_devices.addItems(PyGrabber(None).get_video_devices())
        self.camera_devices.currentIndexChanged.connect(self.changeCameraDevice)

        self.draw_rect = QtWidgets.QPushButton("Capture Frame")
        self.draw_rect.setDisabled(True)
        self.draw_rect.clicked.connect(self.draw)

        self.camera_capture = QtWidgets.QPushButton("Start Capture")
        self.camera_capture.clicked.connect(self.toggleVideoCapture)

        self.layout().addWidget(self.capturedFrame)
        self.layout().addWidget(self.camera_devices)
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

    def resetCameraCapture(self):
        self.draw_rect.setDisabled(True)
        self.capturing = False
        self.camera_capture.setText("Start Capturing")

    def changeCameraDevice(self, index):
        self.resetCameraCapture()
        self.cameraChanged.emit(index)

    def resetDraw(self):
        self.drawingRect = False

    def setCapturedImage(self, img: QtGui.QPixmap):  # shows the captured image in the widget
        self.capturedImage = img
        self.captured_img_dimensions.setText(f"{img.width()} X {img.height()}")
        self.captured_img_lbl.setPixmap(img)
        self.showCaptureOptions()
        self.resetDraw()

    def showCaptureOptions(self):
        self.capturedFrame.show()

    def hideCaptureOptions(self):
        self.capturedFrame.hide()

    def save(self):

        directory = self.directory_edit.text()
        save_image = self.save_as_lbl.text()

        if not os.path.isdir(directory):
            self.error_lbl.setText("Enter a valid directory")
            return

        if not save_image:
            self.error_lbl.setText("Enter a file name")

        path = os.path.join(directory, save_image)

        saved = self.capturedImage.save(path)

        if saved:
            self.error_lbl.setText(f"Saved to successfully to {path}")

        else:
            self.error_lbl.setText(f"Save unsuccessful")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    win = ControlPanel()
    win.show()

    sys.exit(app.exec())
