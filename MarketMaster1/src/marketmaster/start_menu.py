from marketmaster.resources import light_search_icon_path
from marketmaster.resources import search_icon_path
from marketmaster.resources import start_photo
from marketmaster.scaled_label import ScaledLabel
from marketmaster.symbol_line_edit import SymbolLineEdit
from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets


class StartMenu(QtWidgets.QWidget):
    def __init__(self, main_window: QtWidgets.QMainWindow, dark_mode: bool = False):
        super().__init__(main_window)
        self.main_window = main_window
        self.layout = QtWidgets.QVBoxLayout(self)
        top_row_layout = QtWidgets.QHBoxLayout()
        self.symbol_line_edit = SymbolLineEdit()
        self.symbol_line_edit.returnPressed.connect(self.show_graph_menu)
        top_row_layout.addWidget(self.symbol_line_edit)
        self.submit_symbol_button = QtWidgets.QPushButton()
        if dark_mode:
            self.submit_symbol_button.setIcon(QtGui.QIcon(light_search_icon_path))
        else:
            self.submit_symbol_button.setIcon(QtGui.QIcon(search_icon_path))
        self.submit_symbol_button.clicked.connect(self.show_graph_menu)
        top_row_layout.addWidget(self.submit_symbol_button)
        self.layout.addLayout(top_row_layout)
        self.invalid_input_label = QtWidgets.QLabel("Invalid symbol")
        self.invalid_input_label.setStyleSheet("color: red; font-size: 20px;")
        self.invalid_input_label.setVisible(False)
        self.layout.addWidget(self.invalid_input_label)
        photo_label = ScaledLabel(self, alignment=QtCore.Qt.AlignCenter)
        photo_label.setPixmap(QtGui.QPixmap(start_photo))
        self.layout.addWidget(photo_label)
        self.about_button = QtWidgets.QPushButton("about")
        self.about_button.clicked.connect(self.main_window.show_about_dialog)
        self.layout.addWidget(self.about_button)

    def show_graph_menu(self) -> None:
        if self.symbol_line_edit.has_valid_input():
            self.main_window.show_graph_menu(self.symbol_line_edit.text())
            self.invalid_input_label.setVisible(False)
        else:
            self.symbol_line_edit.setStyleSheet("border: 1px solid red;")
            self.invalid_input_label.setVisible(True)

    def set_font(self, font: QtGui.QFont) -> None:
        """Sets the font for this widget and all its children."""
        self.setFont(font)
        self.symbol_line_edit.setFont(font)
        self.about_button.setFont(font)
