from PySide6 import QtWidgets, QtGui

import sqlite_demo
from employee import Employee
from ui import ui_settings


class Adjust_Salary_Dialog(QtWidgets.QWidget):

    def __init__(self, employee):
        super().__init__()
        self.employee = employee
        self.page_name = QtWidgets.QLabel("Update Employee Salary")
        self.first_name_label = QtWidgets.QLabel(f"First Name:")
        self.last_name_label = QtWidgets.QLabel(f"Last Name:")
        self.salary_label = QtWidgets.QLabel("Salary: ")

        ui_settings.format_page_name(self.page_name)
        ui_settings.format_label(self.first_name_label)
        ui_settings.format_label(self.last_name_label)
        ui_settings.format_label(self.salary_label)

        self.first_label = QtWidgets.QLabel(employee.first)
        self.last_label = QtWidgets.QLabel(employee.last)
        self.salary_text = QtWidgets.QLineEdit(str(employee.pay))

        ui_settings.format_label(self.first_label)
        ui_settings.format_label(self.last_label)
        ui_settings.format_text_field(self.salary_text, validator_type=ui_settings.int_validator, max_length=7)

        self.submit_button = QtWidgets.QPushButton("Submit")
        ui_settings.format_button(self.submit_button)
        self.submit_button.clicked.connect(self.submit_clicked)
        self.setLayout(QtWidgets.QVBoxLayout())

        self.align()

    def align(self):
        top_widget = ui_settings.align_horizontal([self.page_name], stretch_beginning=True, stretch_end=True)
        left_widget = ui_settings.align_vertical([self.first_name_label, self.last_name_label, self.salary_label])
        right_widget = ui_settings.align_vertical([self.first_label, self.last_label, self.salary_text])
        central_widget = ui_settings.align_horizontal([left_widget, right_widget], stretch_beginning=True, stretch_end=True)
        bottom_widget = ui_settings.align_horizontal([self.submit_button], stretch_beginning=True, stretch_end=True)

        self.layout().addWidget(top_widget)
        self.layout().addWidget(central_widget)
        self.layout().addWidget(bottom_widget)

    # sets background color
    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        rect = event.rect()
        painter = QtGui.QPainter(self)
        painter.fillRect(rect, ui_settings.background_color)

    def submit_clicked(self):

        salary = int(self.salary_text.text())
        if salary <= 0:
            return

        sqlite_demo.update_pay(self.employee, salary)
        from ui import window_controller
        from ui.main_widget import Main_Widget
        window_controller.switch_ui(Main_Widget())
        window_controller.close_dialog()
