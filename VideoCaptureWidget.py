import cv2
from PySide6 import QtWidgets, QtCore, QtGui


class CaptureDisplayWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(CaptureDisplayWidget, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QVBoxLayout())

        # self.img_label = QtWidgets.QLabel()
        self.img_label = DrawLabel()
        self.img_label.startDraw()
        self.img_label.setText("Click capture to display")
        self.img_label.setScaledContents(True)
        
        self.layout().addWidget(self.img_label)
        self.capture = None

    def updateImage(self, img):
        self.img_label.setPixmap(QtGui.QPixmap.fromImage(img))

    def start(self):
        self.capture = Capture()
        self.capture.frameChanged.connect(self.updateImage)
        self.capture.start()

    def stop(self):

        if self.capture:
            self.capture.stop()
            self.capture.quit()
            self.capture = None


class Capture(QtCore.QThread):

    frameChanged = QtCore.Signal(QtGui.QImage)
        
    def run(self) -> None:
        self.cap = cv2.VideoCapture(0)
        
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


class DrawLabel(QtWidgets.QLabel):
    drawingComplete = QtCore.Signal()

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

    def stopDraw(self):
        self.draw = False
        self._drawingRect = QtCore.QRectF()

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
