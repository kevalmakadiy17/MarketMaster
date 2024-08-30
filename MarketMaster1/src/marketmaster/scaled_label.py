from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class ScaledLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        QtWidgets.QLabel.__init__(self, *args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        self.setMinimumSize(QtCore.QSize(100, 100))
        self.__pixmap: QtGui.QPixmap = self.pixmap()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.setPixmap(self.__pixmap)

    def setPixmap(self, pixmap: QtGui.QPixmap) -> None:
        self.__pixmap = pixmap
        QtWidgets.QLabel.setPixmap(
            self,
            self.__pixmap.scaled(self.frameSize(), QtCore.Qt.KeepAspectRatio),
        )
