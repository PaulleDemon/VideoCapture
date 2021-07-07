from PySide6 import QtWidgets, QtCore
from VideoCaptureWidget import CaptureDisplayWidget
from ControlPanel import ControlPanel


class SplitterWindow(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(SplitterWindow, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QVBoxLayout())

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        self.video = CaptureDisplayWidget()
        self.control_panel = ControlPanel()
        self.control_panel.capture.connect(self.switchCapturing)
        self.control_panel.setMaximumWidth(600)

        splitter.addWidget(self.video)
        splitter.addWidget(self.control_panel)

        self.layout().addWidget(splitter)

    def switchCapturing(self, capture: bool):

        if capture:
            self.video.start()

        else:
            self.video.stop()

    def closeEvent(self, event) -> None:
        print("destroying...")
        self.video.stop()
        super(SplitterWindow, self).closeEvent(event)