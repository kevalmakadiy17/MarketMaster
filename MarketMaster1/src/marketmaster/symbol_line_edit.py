import json
import re

from marketmaster.resources import valid_symbols
from PySide6 import QtWidgets


class SymbolLineEdit(QtWidgets.QLineEdit):
    def __init__(self):
        QtWidgets.QLineEdit.__init__(self)
        with open(valid_symbols, "r", encoding="utf8") as file:
            self.valid_symbols: list[str] = json.load(file)
        self.__pattern = re.compile("|".join(map(re.escape, self.valid_symbols)))
        self.setPlaceholderText("Enter a stock symbol.")
        self.setCompleter(QtWidgets.QCompleter(self.valid_symbols))
        self.textChanged.connect(lambda text: self.setText(text.upper()))
        self.textChanged.connect(self.__remove_any_invalid_suffix)

    def has_valid_input(self) -> bool:
        return self.__pattern.fullmatch(self.text()) is not None

    def __remove_any_invalid_suffix(self) -> None:
        if not self.__has_valid_suffix():
            self.backspace()

    def __has_valid_suffix(self) -> bool:
        for symbol in self.valid_symbols:
            if symbol.startswith(self.text()):
                return True
        return False
