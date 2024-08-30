from marketmaster.resources import left_arrow_icon_path
from marketmaster.resources import light_left_arrow_icon_path
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class SettingsMenu(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow, dark_mode: bool = False):
        super().__init__(main_window)
        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout(self)

        self.back_button = QtWidgets.QPushButton()
        if dark_mode:
            self.back_button.setIcon(QtGui.QIcon(light_left_arrow_icon_path))
        else:
            self.back_button.setIcon(QtGui.QIcon(left_arrow_icon_path))
        self.back_button.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        self.back_button.clicked.connect(self.main_window.show_graph_menu)
        self.layout.addWidget(self.back_button)
        self.title_label = QtWidgets.QLabel("<h1>Settings</h1>")
        self.layout.addWidget(self.title_label, alignment=QtCore.Qt.AlignCenter)

        self.layout.addStretch()

        self.color_mode_checkbox = QtWidgets.QCheckBox("dark mode")
        self.color_mode_checkbox.setChecked(dark_mode)
        self.color_mode_checkbox.stateChanged.connect(self.__change_color_mode)
        self.layout.addWidget(self.color_mode_checkbox, alignment=QtCore.Qt.AlignCenter)

        self.layout.addSpacing(30)

        self.font_button = QtWidgets.QPushButton("font")
        self.layout.addWidget(self.font_button, alignment=QtCore.Qt.AlignCenter)
        self.font_button.clicked.connect(self.__set_app_font)

        self.layout.addSpacing(30)

        self.reset_settings_button = QtWidgets.QPushButton("reset settings")
        self.layout.addWidget(
            self.reset_settings_button, alignment=QtCore.Qt.AlignCenter
        )
        self.reset_settings_button.clicked.connect(self.__reset_settings)

        self.layout.addStretch()

        self.set_font(main_window.font())

    def __change_color_mode(self) -> None:
        if self.color_mode_checkbox.isChecked():
            QtCore.QSettings().setValue("dark_mode", 1)
            # QSettings cannot correctly save booleans.
            self.main_window.dark_mode()
        else:
            QtCore.QSettings().setValue("dark_mode", 0)
            self.main_window.light_mode()

    def set_font(self, font: QtGui.QFont) -> None:
        """Sets the font for this widget and all its children."""
        self.setFont(font)
        self.title_label.setFont(font)
        self.color_mode_checkbox.setFont(font)
        self.font_button.setFont(font)
        self.reset_settings_button.setFont(font)

    def __set_app_font(self) -> None:
        """Sets the font for the entire app and saves settings."""
        font: QtGui.QFont = self.main_window.font()
        ok, font = QtWidgets.QFontDialog.getFont(font)
        if ok:
            self.main_window.set_font(font)
            family: str = font.family()
            size: int = font.pointSize()
            weight = int(font.weight())
            is_italic: bool = font.italic()
            settings = QtCore.QSettings()
            settings.setValue("font/family", family)
            settings.setValue("font/size", size)
            settings.setValue("font/weight", weight)
            settings.setValue("font/italic", int(is_italic))
            # QSettings cannot correctly save booleans.

    def __reset_settings(self) -> None:
        """Resets all settings except bookmarks to default values."""
        settings = QtCore.QSettings()
        if settings.contains("bookmarks"):
            bookmarks = settings.value("bookmarks")
            settings.clear()
            settings.setValue("bookmarks", bookmarks)
        else:
            settings.clear()
        self.main_window.dark_mode()
        self.main_window.set_font(QtGui.QFont("Arial", 16))
        self.color_mode_checkbox.setChecked(True)
