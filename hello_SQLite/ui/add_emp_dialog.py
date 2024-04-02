from PySide6 import QtWidgets, QtGui

import sqlite_demo
from employee import Employee
from ui import ui_settings

class Add_Employee_Dialog(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.page_name = QtWidgets.QLabel("Add Employee to Database")
        self.first_name_label = QtWidgets.QLabel("First Name:")
        self.last_name_label = QtWidgets.QLabel("Last Name: ")
        self.salary_label = QtWidgets.QLabel("Salary: ")

        ui_settings.format_page_name(self.page_name)
        ui_settings.format_label(self.first_name_label)
        ui_settings.format_label(self.last_name_label)
        ui_settings.format_label(self.salary_label)

        self.first_name_text = QtWidgets.QLineEdit()
        self.last_name_text = QtWidgets.QLineEdit()
        self.salary_text = QtWidgets.QLineEdit()

        ui_settings.format_text_field(self.first_name_text, validator_type=ui_settings.char_validator, max_length=15)
        ui_settings.format_text_field(self.last_name_text, validator_type=ui_settings.char_validator, max_length=15)
        ui_settings.format_text_field(self.salary_text, validator_type=ui_settings.int_validator, max_length=7)

        self.message = QtWidgets.QLabel("")
        ui_settings.format_label(self.message)

        self.submit_button = QtWidgets.QPushButton("Submit")
        ui_settings.format_button(self.submit_button)
        self.submit_button.clicked.connect(self.submit_clicked)
        self.setLayout(QtWidgets.QVBoxLayout())

        self.align()

    def align(self):
        top_widget = ui_settings.align_horizontal([self.page_name], stretch_beginning=True, stretch_end=True)
        left_widget = ui_settings.align_vertical([self.first_name_label, self.last_name_label, self.salary_label])
        right_widget = ui_settings.align_vertical([self.first_name_text, self.last_name_text, self.salary_text])
        central_widget = ui_settings.align_horizontal([left_widget, right_widget], stretch_beginning=True, stretch_end=True)
        central_bottom_widget = ui_settings.align_horizontal([self.message], stretch_beginning=True, stretch_end=True)
        bottom_widget = ui_settings.align_horizontal([self.submit_button], stretch_beginning=True, stretch_end=True)

        self.layout().addWidget(top_widget)
        self.layout().addWidget(central_widget)
        self.layout().addWidget(central_bottom_widget)
        self.layout().addWidget(bottom_widget)

    # sets background color
    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        rect = event.rect()
        painter = QtGui.QPainter(self)
        painter.fillRect(rect, ui_settings.background_color)

    def submit_clicked(self):
        first = self.first_name_text.text()
        last = self.last_name_text.text()
        salary = int(self.salary_text.text())

        employee_list = sqlite_demo.get_from_last_name(last)

        for employee in employee_list:
            if employee.first == first:
                self.message.setText("Employee already exists")
                return

        emp = Employee(first, last, salary)

        sqlite_demo.add_data(emp)
        from ui import window_controller
        from ui.main_widget import Main_Widget
        window_controller.switch_ui(Main_Widget())
        window_controller.close_dialog()
