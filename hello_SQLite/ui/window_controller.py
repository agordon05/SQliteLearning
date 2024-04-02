import sys
from PySide6 import QtWidgets

from ui import ui_settings
from ui.main_window import Main_Window
from ui.main_widget import Main_Widget
from ui.dialog_window import Dialog_Window

app = QtWidgets.QApplication()
widget: QtWidgets = Main_Widget()
window: Main_Window = Main_Window()
log_window: Dialog_Window = Dialog_Window()


def switch_ui(temp_widget: QtWidgets):
    global widget
    widget = temp_widget
    window.setCentralWidget(widget)


def create_dialog(widget_dialog: QtWidgets.QWidget):
    global log_window, window
    log_window = Dialog_Window(widget=widget_dialog, parent=window)
    log_window.setWindowTitle(ui_settings.window_title)
    log_window.setModal(True)  # Make it a modal dialog

    center_x: int = int(window.geometry().center().x() - ui_settings.dialog_width // 2)
    # if isinstance(widget_dialog, new_bot_widget):
    #     center_y: int = int(window.geometry().center().y() - ui_settings.dialog_new_bot_height // 2)
    # else:
    center_y: int = int(window.geometry().center().y() - ui_settings.dialog_height // 2)
    log_window.setGeometry(center_x, center_y, ui_settings.dialog_width, ui_settings.dialog_height)
    log_window.show()
    print(f"height: {log_window.height()}")


def close_dialog():
    global log_window
    log_window.accept()


def run_ui():
    window.setWindowTitle("Employee Database")
    window.resize(800, 600)
    # window.showFullScreen()
    window.show()
    window.setCentralWidget(widget)
    sys.exit(app.exec())

