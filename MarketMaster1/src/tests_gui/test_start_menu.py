import pytest
from marketmaster.main_window import MainWindow
from PySide6 import QtCore
from pytestqt import qtbot  # noqa: F401

# pip install pytest-qt==4.2.0


@pytest.mark.filterwarnings("ignore::DeprecationWarning")  # from Matplotlib
def test_show_graph_menu(qtbot):  # noqa: F811
    main_window = MainWindow()
    main_window.show()
    qtbot.addWidget(main_window)
    main_window.start_menu.symbol_line_edit.setText("AAPL")
    main_window.start_menu.show_graph_menu()
    assert main_window.graph_menu.isVisible() is True


@pytest.mark.filterwarnings("ignore::DeprecationWarning")  # from Matplotlib
def test_symbol_enter_press(qtbot):  # noqa: F811
    main_window = MainWindow()
    main_window.show()
    qtbot.addWidget(main_window)
    qtbot.keyClicks(main_window.start_menu.symbol_line_edit, "AAPL")
    qtbot.keyPress(main_window.start_menu.symbol_line_edit, QtCore.Qt.Key_Enter)
    assert main_window.graph_menu.isVisible() is True


def test_symbol_button_press(qtbot):  # noqa: F811
    main_window = MainWindow()
    main_window.show()
    qtbot.addWidget(main_window)
    qtbot.keyClicks(main_window.start_menu.symbol_line_edit, "AAPL")
    qtbot.mouseClick(main_window.start_menu.submit_symbol_button, QtCore.Qt.LeftButton)
    assert main_window.graph_menu.isVisible() is True
