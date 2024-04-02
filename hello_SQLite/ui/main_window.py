from PySide6 import QtWidgets, QtGui
import sqlite_demo


class Main_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        sqlite_demo.close()
        event.accept()

