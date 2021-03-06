import cv2
from PySide6 import QtWidgets, QtCore, QtGui


class VideoCaptureDisplayWidget(QtWidgets.QWidget):

    # Displays image frame by frame

    capturedImage = QtCore.Signal(QtGui.QImage)  # emits the captured image
    cameraFailed = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(VideoCaptureDisplayWidget, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QVBoxLayout())

        self.img_label = DrawLabel()
        self.img_label.drawingComplete.connect(self.extractImageFromRect)
        self.img_label.setText("Click capture to display")
        self.img_label.setScaledContents(True)
        
        self.layout().addWidget(self.img_label)
        self.capture = None
        self.cameraDevice = 0

    def updateImage(self, img): # changes the current frame
        self.img_label.setPixmap(QtGui.QPixmap.fromImage(img))

    def start(self):
        self.img_label.setText("")
        self.capture = Capture(self.cameraDevice)
        self.capture.frameChanged.connect(self.updateImage)
        self.capture.cameraFailed.connect(self.cameraUnsuccessful)
        self.capture.start()

    def cameraUnsuccessful(self):
        self.stop()
        self.cameraFailed.emit()
        self.img_label.clear()
        self.img_label.setText("Camera Failed")

    def stop(self):

        if self.capture:
            self.capture.stop()
            self.capture.quit()
            self.capture = None

    def drawRect(self):  # enables draw rect
        self.img_label.startDraw()

    def stopDrawing(self):  # stops drawing
        self.img_label.stopDraw()

    def extractImageFromRect(self):  # emits the image inside the drawn rect
        pixmap = self.img_label.pixmap()

        image = pixmap.copy(self.img_label.drawingRect().toRect()).toImage()
        self.capturedImage.emit(image)
        self.img_label.stopDraw()

    def setCameraDevice(self, index):
        self.cameraDevice = index


class Capture(QtCore.QThread): # capture video frame by frame

    frameChanged = QtCore.Signal(QtGui.QImage)  # emits new image
    cameraFailed = QtCore.Signal() # emits when the camera was unsuccessful

    def __init__(self, cameraDevice=0, *args, **kwargs):
        super(Capture, self).__init__(*args, **kwargs)
        self.cameraDevice = cameraDevice

    def run(self) -> None:
        self.cap = cv2.VideoCapture(self.cameraDevice)

        if not self.cap.isOpened():
            self.cameraFailed.emit()
            return

        while not self.isInterruptionRequested():

            ret, frame = self.cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QtGui.QImage(rgbImage.data, w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
                pix = convertToQtFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                self.frameChanged.emit(pix)

        self.cap.release()

    def stop(self):
        self.requestInterruption()
        self.wait()


class DrawLabel(QtWidgets.QLabel):  # Enables user to draw over the image

    drawingComplete = QtCore.Signal()  # emits when mouse released when drawing

    def __init__(self, *args, **kwargs):
        super(DrawLabel, self).__init__(*args, **kwargs)
        self.draw = False
        self._isdrawing = False
        self._drawingRect = QtCore.QRectF()

        self.penColor = QtGui.QColor("#06c42c")
        self._penWidth = 2

    def setPenWidth(self, penwidth: float):
        self._penWidth = penwidth

    def setPenColor(self, color):
        self.penColor = QtGui.QColor(color)

    def startDraw(self):
        self.draw = True
        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

    def stopDraw(self):
        self.draw = False
        self._drawingRect = QtCore.QRectF()
        self.setCursor(QtGui.QCursor())

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:

        if self.draw:
            pos = event.pos()
            self._isdrawing = True
            self._drawingRect.setRect(pos.x(), pos.y(), pos.x(), pos.y())

        else:
            super(DrawLabel, self).mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:

        if self._isdrawing:
            self._drawingRect.setBottomRight(event.pos())

        else:
            super(DrawLabel, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:

        if self._isdrawing:
            self._drawingRect.setBottomRight(event.pos())
            self._isdrawing = False
            self.drawingComplete.emit()

        else:
            super(DrawLabel, self).mouseReleaseEvent(event)

    def drawingRect(self):
        return self._drawingRect

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        super(DrawLabel, self).paintEvent(event)

        if self.draw:
            painter = QtGui.QPainter(self)
            painter.setPen(self.penColor)
            painter.pen().setWidthF(self._penWidth)
            painter.drawRect(self.drawingRect())
            self.update()
