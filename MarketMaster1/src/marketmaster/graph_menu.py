from datetime import datetime
from datetime import timedelta

import FinanceDataReader as fdr
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from marketmaster.info_panel import InfoPanel
from marketmaster.progress_dialog import ProgressDialog
from marketmaster.resources import folder_icon_path
from marketmaster.resources import history_icon_path
from marketmaster.resources import light_folder_icon_path
from marketmaster.resources import light_history_icon_path
from marketmaster.resources import light_settings_icon_path
from marketmaster.resources import settings_icon_path
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

matplotlib.use("Qt5Agg")

plt.rcParams["figure.figsize"] = (14, 8)
plt.rcParams["font.size"] = 16
plt.rcParams["lines.linewidth"] = 2
plt.rcParams["axes.grid"] = True
plt.rcParams["axes.axisbelow"] = True


class GraphMenu(QtWidgets.QWidget):
    def __init__(
        self, symbol: str, main_window: QtWidgets.QMainWindow, dark_mode: bool = False
    ):
        super().__init__(main_window)
        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout(self)
        self.history_qmenu = QtWidgets.QMenu(self)
        self.bookmarks_qmenu = QtWidgets.QMenu(self)
        if dark_mode:
            self.settings_action = QtGui.QAction(
                QtGui.QIcon(light_settings_icon_path), "", self
            )
            self.history_qmenu.setIcon(QtGui.QIcon(light_history_icon_path))
            self.bookmarks_qmenu.setIcon(QtGui.QIcon(light_folder_icon_path))
        else:
            self.settings_action = QtGui.QAction(
                QtGui.QIcon(settings_icon_path), "", self
            )
            self.history_qmenu.setIcon(QtGui.QIcon(history_icon_path))
            self.bookmarks_qmenu.setIcon(QtGui.QIcon(folder_icon_path))
        main_window.menuBar().addAction(self.settings_action)
        self.main_window.menuBar().addMenu(self.bookmarks_qmenu)
        self.bookmarks_qmenu.menuAction().setVisible(False)
        self.settings_action.triggered.connect(main_window.show_settings_menu)

        self.history: list[tuple[str, QtGui.QAction]] = []

        self.splitter = QtWidgets.QSplitter()
        self.layout.addWidget(self.splitter)
        qApp.aboutToQuit.connect(self._save_splitter_state)  # type: ignore # noqa: F821

        symbol_to_name: dict[str, str] = (
            fdr.StockListing("S&P500").set_index("Symbol")["Name"].to_dict()
        )
        self.info_panel = InfoPanel(
            symbol, symbol_to_name, self.show_graph_and_info_panel, self, main_window
        )
        self.splitter.addWidget(self.info_panel)
        self.plot = MatplotlibWidget()
        self.splitter.addWidget(self.plot)
        settings = QtCore.QSettings()
        if settings.contains("splitter_state"):
            self.splitter.restoreState(settings.value("splitter_state"))

        self.show_graph_and_info_panel(symbol)
        self.set_font(main_window.font())

    def _save_splitter_state(self) -> None:
        QtCore.QSettings().setValue("splitter_state", self.splitter.saveState())

    def show_graph_and_info_panel(self, symbol: str | None = None) -> None:
        """Shows the table and graph for the given symbol.

        Depends on the info panel's symbol line edit and prediction days spin box.
        """
        if isinstance(symbol, bool):
            symbol = None
        if symbol is None:
            symbol = self.info_panel.symbol_line_edit.text()
        else:
            self.info_panel.symbol_line_edit.setText(symbol)
        if not self.info_panel.is_valid_symbol():
            return
        assert len(symbol) > 0
        prediction_days: int = self.info_panel.prediction_days_spin_box.value()
        symbol_data: pd.DataFrame = fdr.DataReader(symbol)
        todays_symbol_data: pd.DataFrame = symbol_data.iloc[-1]

        with ProgressDialog():
            s_history: tuple[str, ...] = tuple(s[0] for s in self.history)
            if symbol not in s_history:
                new_action = QtGui.QAction(symbol, self)
                new_action.triggered.connect(
                    lambda self=self, symbol=symbol: self.show_graph_and_info_panel(
                        symbol
                    )
                )
                if self.history:
                    self.history_qmenu.insertAction(
                        self.history_qmenu.actions()[0], new_action
                    )
                else:
                    self.history_qmenu.addAction(new_action)
                self.history.append((symbol, new_action))
                if len(self.history) == 2:
                    self.main_window.menuBar().addMenu(self.history_qmenu)
            else:
                i = s_history.index(symbol)
                e = self.history[i]
                del self.history[i]
                self.history.append(e)
                self.history_qmenu.removeAction(e[1])
                history_actions = self.history_qmenu.actions()
                if history_actions:
                    self.history_qmenu.insertAction(history_actions[0], e[1])
                else:
                    self.history_qmenu.addAction(e[1])
            self.__load_and_show_graph(symbol, prediction_days, symbol_data)
            self.info_panel.show_info_panel(symbol, todays_symbol_data)

    def __load_and_show_graph(
        self, symbol: str, prediction_days: int, symbol_data: pd.DataFrame
    ) -> None:
        """Creates and displays the graph."""
        if not self.info_panel.is_valid_symbol():
            return

        # select only the close column
        close = symbol_data["Close"]

        # set a period for comparing
        end_datetime = datetime.today()
        end_date = end_datetime.strftime("%Y-%m-%d")
        start_datetime = end_datetime - timedelta(days=90)
        start_date = start_datetime.strftime("%Y-%m-%d")

        base = close[start_date:end_date]  # type: ignore
        base_norm = (base - base.min()) / (base.max() - base.min())

        # window size: number of past days to see the pattern
        window_size = len(base)

        # how many days you wanna predict
        next_date = prediction_days  # 5 means one week, 10 means two weeks, etc.

        # number of search
        moving_cnt = len(close) - window_size - next_date - 1

        def cosine_similarity(x, y):
            return np.dot(x, y) / (np.sqrt(np.dot(x, x)) * np.sqrt(np.dot(y, y)))

        sim_list = []  # similarity

        for i in range(moving_cnt):
            target = close[i : i + window_size]  # noqa: E203
            target_norm = (target - target.min()) / (target.max() - target.min())
            cos_similarity = cosine_similarity(base_norm, target_norm)
            sim_list.append(cos_similarity)

        idx = pd.Series(sim_list).sort_values(ascending=False).head(1).index[0]
        # print(pd.Series(sim_list).sort_values(ascending = False).head(20))

        top_ = close[idx : idx + window_size + next_date]  # noqa: E203
        top_norm = (top_ - top_.min()) / (top_.max() - top_.min())

        dates: list[str] = self.get_dates(base_norm.index)

        figure = self.plot.getFigure()
        figure.clear()  # clear the graph's title
        subplot = figure.add_subplot(1, 1, 1)
        subplot.set_title(symbol)
        subplot.set_ylabel("Normalized Price")
        subplot.plot(dates, base_norm.values, top_norm.values)
        subplot.tick_params(axis="x", labelrotation=30, labelsize=10)
        subplot.xaxis.set_major_locator(plt.MaxNLocator(10))
        subplot.axvline(x=len(base_norm) - 1, c="r", linestyle="--", label="today")
        subplot.axvspan(
            len(base_norm.values) - 1,
            len(top_norm.values) - 1,
            facecolor="yellow",
            alpha=0.3,
        )
        subplot.legend(["actual", "predicted", "today"])
        self.plot.draw()  # required for changing from one graph to another

    def get_dates(self, index) -> list[str]:
        datetime_index = index
        dates: list[str] = [str(datetime_index[i]) for i in range(len(datetime_index))]
        return [x.split(" ")[0] for x in dates]

    def set_font(self, font: QtGui.QFont) -> None:
        """Sets the font for this widget and all its children."""
        self.setFont(font)
        self.info_panel.set_font(font)
