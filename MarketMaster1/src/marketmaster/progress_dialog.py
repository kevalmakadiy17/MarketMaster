from PySide6 import QtCore
from PySide6 import QtWidgets


class ProgressDialog:
    def __enter__(self) -> None:
        self.__progress_dialog = QtWidgets.QProgressDialog("Loading...", "", 0, 0)
        self.__progress_dialog.setCancelButton(None)
        self.__progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        self.__progress_dialog.show()
        self.__progress_dialog.setValue(0)
        QtWidgets.QApplication.processEvents()

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.__progress_dialog.cancel()
