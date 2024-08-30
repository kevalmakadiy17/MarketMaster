from textwrap import dedent
from typing import Callable

import pandas as pd
from marketmaster.common import round_
from marketmaster.resources import blue_star_icon_path
from marketmaster.resources import light_search_icon_path
from marketmaster.resources import light_star_icon_path
from marketmaster.resources import search_icon_path
from marketmaster.resources import star_icon_path
from marketmaster.symbol_line_edit import SymbolLineEdit
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class InfoPanel(QtWidgets.QWidget):
    """The left panel of the main window.

    Constructing an instance of this class will not automatically show the info panel.
    The ``show_info_panel`` method must be called to show the info panel.
    """

    def __init__(
        self,
        symbol: str,
        symbol_to_name: dict[str, str],
        show_graph_and_info_panel: Callable,
        graph_menu,
        main_window: QtWidgets.QMainWindow,
    ):
        super().__init__()
        self.SYMBOL_TO_NAME: dict[str, str] = symbol_to_name
        self.show_graph_and_info_panel = show_graph_and_info_panel
        self.main_window = main_window
        self.graph_menu = graph_menu
        self.layout = QtWidgets.QVBoxLayout(self)
        settings = QtCore.QSettings()
        top_row_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(top_row_layout)
        top_row_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.symbol_line_edit = SymbolLineEdit()
        top_row_layout.addWidget(self.symbol_line_edit)
        self.symbol_line_edit.returnPressed.connect(self.show_graph_and_info_panel)
        self.symbol_line_edit.returnPressed.connect(self.__load_and_show_table)
        self.symbol_line_edit.setText(symbol)
        self.bookmarks: list[tuple[str, QtGui.QAction]] = self.__load_bookmarks()
        self.bookmark_action = QtGui.QAction(self)
        self.symbol_line_edit.addAction(
            self.bookmark_action, QtWidgets.QLineEdit.TrailingPosition
        )
        self.bookmark_action.triggered.connect(self.__toggle_bookmark)
        self.original_key_press_event = self.symbol_line_edit.keyPressEvent
        self.symbol_line_edit.keyPressEvent = self.__key_press_event
        self.submit_symbol_button = QtWidgets.QPushButton()
        top_row_layout.addWidget(self.submit_symbol_button)
        if settings.contains("dark_mode") and not settings.value("dark_mode"):
            self.submit_symbol_button.setIcon(QtGui.QIcon(search_icon_path))
            self.bookmark_action.setIcon(QtGui.QIcon(star_icon_path))
        else:
            self.submit_symbol_button.setIcon(QtGui.QIcon(light_search_icon_path))
            self.bookmark_action.setIcon(QtGui.QIcon(light_star_icon_path))
        self.submit_symbol_button.clicked.connect(self.show_graph_and_info_panel)
        self.submit_symbol_button.clicked.connect(self.__load_and_show_table)
        self.invalid_input_label = QtWidgets.QLabel("Invalid symbol")
        self.invalid_input_label.setStyleSheet("color: red; font-size: 20px;")
        self.invalid_input_label.setVisible(False)
        self.layout.addWidget(self.invalid_input_label)
        days_hbox_layout = QtWidgets.QHBoxLayout()
        self.layout.addLayout(days_hbox_layout)
        self.days_label = QtWidgets.QLabel("days to predict:")
        self.days_label.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum
        )
        days_hbox_layout.addWidget(self.days_label)
        self.prediction_days_spin_box = QtWidgets.QSpinBox(self)
        days_hbox_layout.addWidget(self.prediction_days_spin_box)
        self.prediction_days_spin_box.setSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
        )
        self.prediction_days_spin_box.setRange(1, 365)
        self.prediction_days_spin_box.setValue(5)
        self.prediction_days_spin_box.lineEdit().returnPressed.connect(
            self.show_graph_and_info_panel
        )
        self.layout.addSpacing(30)

        self.label = QtWidgets.QLabel("Loading...")
        self.layout.addWidget(self.label)
        self.table = QtWidgets.QTableWidget()
        self.layout.addWidget(self.table)
        self.table.setColumnCount(2)
        self.table.setRowCount(5)
        self.table.setHorizontalHeaderLabels(["", ""])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.table.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents
        )
        self.table.setItem(0, 0, QtWidgets.QTableWidgetItem("high"))
        self.table.setItem(1, 0, QtWidgets.QTableWidgetItem("low"))
        self.table.setItem(2, 0, QtWidgets.QTableWidgetItem("close"))
        self.table.setItem(3, 0, QtWidgets.QTableWidgetItem("adj close"))
        self.table.setItem(4, 0, QtWidgets.QTableWidgetItem("volume"))
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(
            """
            QTableView {
                font-size: 20px;
                margin-top: 25px;
                border: none;
            }
            """
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )

    def __key_press_event(self, event: QtGui.QKeyEvent) -> None:
        """Handles the key press event for the symbol line edit.

        If the key is the down arrow, the focus is set to the table.
        """
        if (
            event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter)
            and self.symbol_line_edit.has_valid_input()
        ):
            self.bookmark_action.setVisible(True)
            self.invalid_input_label.setVisible(False)
            # self.table.setFocus()
        elif len(event.text()) > 0 and not event.text().isalpha():
            self.bookmark_action.setVisible(False)
            self.invalid_input_label.setVisible(True)
        self.original_key_press_event(event)

    def show_info_panel(self, symbol: str, todays_symbol_data: pd.DataFrame) -> None:
        """Loads and shows the info panel for the given symbol."""
        self.load_bookmark_star(symbol)
        self.symbol = symbol
        self.data = todays_symbol_data
        self.__load_and_show_table()

    def load_bookmark_star(self, symbol: str | None = None) -> None:
        """Sets the correct bookmark star icon.

        If the symbol is not given, it will be retrieved from the symbol line edit.
        """
        if symbol is None:
            symbol = self.symbol_line_edit.text()
        settings = QtCore.QSettings()
        if symbol in tuple(s[0] for s in self.bookmarks):
            self.bookmark_action.setIcon(QtGui.QIcon(blue_star_icon_path))
        elif settings.contains("dark_mode") and not settings.value("dark_mode"):
            self.bookmark_action.setIcon(QtGui.QIcon(star_icon_path))
        else:
            self.bookmark_action.setIcon(QtGui.QIcon(light_star_icon_path))

    def __load_and_show_table(self) -> None:
        """Loads the table data and displays it.

        Depends on the ``self.symbol`` and ``self.data`` attributes.
        """
        self.label.setText(
            dedent(
                f"""\
                <h2 style="font-size: 24px">
                    {self.SYMBOL_TO_NAME[self.symbol]}
                </h2>
                """
            )
        )
        self.table.setItem(0, 1, QtWidgets.QTableWidgetItem(round_(self.data["High"])))
        self.table.setItem(1, 1, QtWidgets.QTableWidgetItem(round_(self.data["Low"])))
        self.table.setItem(2, 1, QtWidgets.QTableWidgetItem(round_(self.data["Close"])))
        self.table.setItem(
            3, 1, QtWidgets.QTableWidgetItem(round_(self.data["Adj Close"]))
        )
        self.table.setItem(
            4, 1, QtWidgets.QTableWidgetItem(round_(self.data["Volume"]))
        )

    def is_valid_symbol(self) -> bool:
        if not self.symbol_line_edit.has_valid_input():
            self.symbol_line_edit.setStyleSheet("border: 1px solid red;")
            return False
        self.symbol_line_edit.setStyleSheet("")
        return True

    def set_font(self, font: QtGui.QFont) -> None:
        """Sets the font for this widget and all its children."""
        self.setFont(font)
        self.days_label.setFont(font)
        self.symbol_line_edit.setFont(font)
        self.prediction_days_spin_box.setFont(font)
        self.label.setFont(font)
        self.table.setFont(font)

    def __toggle_bookmark(self) -> None:
        """Toggles the bookmark for the current symbol."""
        if not self.is_valid_symbol():
            return
        symbol: str = self.symbol_line_edit.text()
        settings = QtCore.QSettings()
        s_bookmarks: list[str] = [s[0] for s in self.bookmarks]
        if symbol in s_bookmarks:
            i = s_bookmarks.index(symbol)
            if settings.contains("dark_mode") and not settings.value("dark_mode"):
                self.bookmark_action.setIcon(QtGui.QIcon(star_icon_path))
            else:
                self.bookmark_action.setIcon(QtGui.QIcon(light_star_icon_path))
            self.graph_menu.bookmarks_qmenu.removeAction(self.bookmarks[i][1])
            del s_bookmarks[i]
            del self.bookmarks[i]
            if len(self.bookmarks) == 0:
                self.graph_menu.bookmarks_qmenu.menuAction().setVisible(False)
        else:
            new_action = self.__create_bookmark_action(symbol)
            self.graph_menu.bookmarks_qmenu.addAction(new_action)
            self.bookmarks.append((symbol, new_action))
            s_bookmarks.append(symbol)
            if len(self.bookmarks) > 0:
                self.graph_menu.bookmarks_qmenu.menuAction().setVisible(True)
            self.bookmark_action.setIcon(QtGui.QIcon(blue_star_icon_path))
        settings.setValue("bookmarks", ",".join(s_bookmarks))

    def __load_bookmarks(self) -> list[tuple[str, QtGui.QAction]]:
        """Loads the symbol bookmarks from the config files."""
        settings = QtCore.QSettings()
        if settings.contains("bookmarks"):
            s_bookmarks = settings.value("bookmarks").split(",")
            s_bookmarks = list(
                dict.fromkeys(s_bookmarks)
            )  # stable-ly remove duplicates
            bookmarks = []
            for symbol in s_bookmarks:
                if symbol not in self.symbol_line_edit.valid_symbols:
                    continue
                new_action = self.__create_bookmark_action(symbol)
                self.graph_menu.bookmarks_qmenu.addAction(new_action)
                bookmarks.append((symbol, new_action))
            if bookmarks:
                self.graph_menu.bookmarks_qmenu.menuAction().setVisible(True)
            return bookmarks
        return []

    def __create_bookmark_action(self, symbol: str) -> QtGui.QAction:
        """Creates the bookmark action."""
        new_action = QtGui.QAction(symbol, self)
        new_action.triggered.connect(
            lambda self=self, symbol=symbol: self.graph_menu.show_graph_and_info_panel(
                symbol
            )
        )
        return new_action
