from PySide6 import QtWidgets, QtGui, QtCore
import sqlite_demo
from employee import Employee
from ui.table_widget import Table_Widget

from ui import ui_settings


class Main_Widget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.page_name = QtWidgets.QLabel("Database")
        ui_settings.format_page_name(self.page_name)

        self.table = Table_Widget(sqlite_demo.get_employees())
        self.add_emp_button = QtWidgets.QPushButton("Add Employee")
        self.add_emp_button.clicked.connect(self.button_clicked)
        ui_settings.format_button(self.add_emp_button)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.create_window()

    def create_window(self):
        top_widget = ui_settings.align_horizontal([self.page_name], stretch_beginning=True, stretch_end=True)
        center_widget = ui_settings.align_vertical([top_widget, self.table])
        bottom_widget = ui_settings.align_horizontal([self.add_emp_button], stretch_beginning=True, stretch_end=True)
        self.layout().addWidget(top_widget)
        self.layout().addWidget(center_widget)
        self.layout().addWidget(bottom_widget)

    # sets background color
    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        rect = event.rect()
        painter = QtGui.QPainter(self)
        painter.fillRect(rect, ui_settings.background_color)

    def button_clicked(self):
        from ui import window_controller
        from ui.add_emp_dialog import Add_Employee_Dialog
        window_controller.create_dialog(Add_Employee_Dialog())
