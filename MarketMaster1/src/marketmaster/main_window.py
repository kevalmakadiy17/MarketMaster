from textwrap import dedent

from marketmaster.graph_menu import GraphMenu
from marketmaster.resources import folder_icon_path
from marketmaster.resources import history_icon_path
from marketmaster.resources import left_arrow_icon_path
from marketmaster.resources import light_folder_icon_path
from marketmaster.resources import light_history_icon_path
from marketmaster.resources import light_left_arrow_icon_path
from marketmaster.resources import light_search_icon_path
from marketmaster.resources import light_settings_icon_path
from marketmaster.resources import search_icon_path
from marketmaster.resources import settings_icon_path
from marketmaster.settings_menu import SettingsMenu
from marketmaster.start_menu import StartMenu
from marketmaster.styles import dark_mode_stylesheet
from marketmaster.styles import light_mode_stylesheet
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


VERSION = "1.0.0"


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        qApp.aboutToQuit.connect(self.__on_quit)  # type: ignore # noqa: F821
        self.close_shortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+W"), self)
        self.close_shortcut.activated.connect(self.close)

    def init_ui(self) -> None:
        self.setWindowTitle("MarketMaster")
        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        settings = QtCore.QSettings()
        if settings.contains("dark_mode"):
            self.start_menu = StartMenu(self, bool(settings.value("dark_mode")))
        else:
            self.start_menu = StartMenu(self, dark_mode=True)
        self.central_widget.addWidget(self.start_menu)
        self.graph_menu: GraphMenu | None = None
        self.settings_menu: SettingsMenu | None = None
        self.central_widget.setCurrentWidget(self.start_menu)
        self.__load_settings_and_show_window()

    def show_graph_menu(self, symbol: str | None = None) -> None:
        if self.graph_menu is None:
            if symbol is None:
                raise ValueError(
                    "symbol must be provided when creating a new graph menu"
                )
            settings = QtCore.QSettings()
            if settings.contains("dark_mode"):
                self.graph_menu = GraphMenu(
                    symbol, self, bool(settings.value("dark_mode"))
                )
            else:
                self.graph_menu = GraphMenu(symbol, self, dark_mode=True)
            self.central_widget.addWidget(self.graph_menu)
        self.central_widget.setCurrentWidget(self.graph_menu)

    def show_settings_menu(self) -> None:
        if self.settings_menu is None:
            settings = QtCore.QSettings()
            if settings.contains("dark_mode"):
                self.settings_menu = SettingsMenu(
                    self, bool(settings.value("dark_mode"))
                )
            else:
                self.settings_menu = SettingsMenu(self, dark_mode=True)
            self.central_widget.addWidget(self.settings_menu)
        self.central_widget.setCurrentWidget(self.settings_menu)

    def show_about_dialog(self) -> None:
        msg = QtWidgets.QMessageBox()
        msg.setText(
            dedent(
                f"""
                <h1>MarketMaster</h1>

                <p>v{VERSION}</p>

                <p>Icons from lucide.dev</p>
                """
            )
        )
        msg.exec()

    def __load_settings_and_show_window(self) -> None:
        """Reads the settings from the device's configuration files."""
        settings = QtCore.QSettings()
        if not settings.contains("main_window/geometry"):
            self.showMaximized()
        else:
            geometry_bytes: QtCore.QByteArray = settings.value("main_window/geometry")
            if geometry_bytes.isEmpty():
                self.showMaximized()
            else:
                self.adjustSize()
                self.restoreGeometry(geometry_bytes)
                self.show()
        if settings.contains("dark_mode") and not settings.value("dark_mode"):
            self.light_mode()
        else:
            self.dark_mode()
        if settings.contains("font/family"):
            font_family: str = settings.value("font/family")
            font_size: int = settings.value("font/size")
            font_weight: int = settings.value("font/weight")
            font_is_italic: bool = bool(settings.value("font/italic"))
            font = QtGui.QFont(font_family, font_size, font_weight, font_is_italic)
            self.set_font(font)
        else:
            font = QtGui.QFont("Arial", 16, QtGui.QFont.Weight.Normal, False)
            self.set_font(font)

    def dark_mode(self) -> None:
        """Sets the app's color mode to dark colors.

        Does not change the settings.
        """
        self.setStyleSheet(dark_mode_stylesheet)
        if self.graph_menu is not None:
            self.graph_menu.settings_action.setIcon(
                QtGui.QIcon(light_settings_icon_path)
            )
            self.graph_menu.history_qmenu.setIcon(QtGui.QIcon(light_history_icon_path))
            self.graph_menu.bookmarks_qmenu.setIcon(QtGui.QIcon(light_folder_icon_path))
            self.graph_menu.info_panel.submit_symbol_button.setIcon(
                QtGui.QIcon(light_search_icon_path)
            )
            self.graph_menu.info_panel.load_bookmark_star()
        if self.settings_menu is not None:
            self.settings_menu.back_button.setIcon(
                QtGui.QIcon(light_left_arrow_icon_path)
            )

    def light_mode(self) -> None:
        """Sets the app's color mode to light colors.

        Does not change the settings.
        """
        self.setStyleSheet(light_mode_stylesheet)
        if self.graph_menu is not None:
            self.graph_menu.settings_action.setIcon(QtGui.QIcon(settings_icon_path))
            self.graph_menu.history_qmenu.setIcon(QtGui.QIcon(history_icon_path))
            self.graph_menu.bookmarks_qmenu.setIcon(QtGui.QIcon(folder_icon_path))
            self.graph_menu.info_panel.submit_symbol_button.setIcon(
                QtGui.QIcon(search_icon_path)
            )
            self.graph_menu.info_panel.load_bookmark_star()
        if self.settings_menu is not None:
            self.settings_menu.back_button.setIcon(QtGui.QIcon(left_arrow_icon_path))

    def __save_window_geometry(self):
        """Saves the window's size and location to the device's configuration files."""
        QtCore.QSettings().setValue("main_window/geometry", self.saveGeometry())

    def set_font(self, font: QtGui.QFont) -> None:
        """Sets the font for the entire app."""
        self.setFont(font)
        self.start_menu.set_font(font)
        if self.graph_menu is not None:
            self.graph_menu.set_font(font)
        if self.settings_menu is not None:
            self.settings_menu.set_font(font)

    def __on_quit(self) -> None:
        """Called when the application is about to quit.

        Other code may run for a short time after this method runs.
        """
        self.__save_window_geometry()
