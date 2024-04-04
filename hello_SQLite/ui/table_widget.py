from PySide6 import QtWidgets, QtCore, QtGui

from employee import Employee
from ui import ui_settings


class Table_Widget(QtWidgets.QTableWidget):
    def __init__(self, employees: [Employee]):
        super().__init__()
        self.row_under_mouse = -1
        self.employees = employees
        self.__sort()
        self.__set_settings()
        self.__add_functionality()
        self.__add_data()

    def __sort(self):
        self.employees = sorted(self.employees, key=lambda item: item.first)
        self.employees = sorted(self.employees, key=lambda item: item.last)

    def __set_settings(self):
        self.setHorizontalHeaderLabels(self.__get_headers())
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setFont(ui_settings.table_header_font)
        self.horizontalHeader().setStyleSheet(ui_settings.table_header_stylesheet)

        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(60)  # Set the default row height
        self.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.SingleSelection)
        self.setShowGrid(False)
        self.setMouseTracking(True)
        self.setStyleSheet(ui_settings.table_stylesheet_dark_mode)

    def __get_headers(self):
        self.setColumnCount(3)
        return ["Name", "Email", "Salary"]

    def __add_functionality(self):
        self.itemPressed.connect(self.__cell_pressed)
        self.itemClicked.connect(self.__row_clicked)

    def __add_data(self):
        current_row_count = self.rowCount()

        for row, item in enumerate(self.employees):
            if row >= current_row_count:
                self.setRowCount(row + 1)

            # create table cells
            items = self.__update_table_widget_items(row, 3)

            # set text for table cell
            items[0].setText(item.full_name)  # name
            items[1].setText(item.email)  # email
            items[2].setText(f"${item.pay}")  # salary

            if row >= current_row_count:
                # profit.setForeground(QtGui.QBrush(ui_settings.green_color))

                self.__format_table_items(items)

                # Set text color
                items[0].setForeground(ui_settings.text_color)  # Name
                items[1].setForeground(ui_settings.text_color)  # Email
                items[2].setForeground(ui_settings.text_color)  # Salary

                # add table cell
                self.__set_items(row, items)

    def __format_table_items(self, items: [QtWidgets.QTableWidgetItem]):
        for item in items:
            item.setTextAlignment(QtGui.Qt.AlignmentFlag.AlignCenter)
            item.setFont(ui_settings.table_font)

    def __set_items(self, row, items: [QtWidgets.QTableWidgetItem]):
        for count, item in enumerate(items):
            self.setItem(row, count, item)

    def __update_table_widget_items(self, row: int, amount: int) -> [QtWidgets.QTableWidgetItem]:

        items: [QtWidgets.QTableWidgetItem] = []
        for count in range(amount):
            item = self.item(row, count) or QtWidgets.QTableWidgetItem()
            items.append(item)

        return items

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        # Override the default behavior to prevent selection dragging
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            return

        super(Table_Widget, self).mouseMoveEvent(event)

        # Determine the current row when the mouse moves over the table
        pos = event.pos()
        index = self.indexAt(pos)
        # print("in mouse event")
        if index.isValid():
            # print("index is valid")
            row = index.row()
            if row != self.row_under_mouse:
                # print("row is not equal to row under mouse")
                # Clear previous highlight
                self.clear_highlight()

                # Highlight the current row
                self.row_under_mouse = row
                self.highlight_row(row)
        else:
            # If the mouse is not over a valid index, clear the highlight
            self.clear_highlight()


    @QtCore.Slot()
    def __row_clicked(self, item):
        employee = self.employees[item.row()]

        from ui import window_controller
        from ui.adjust_salary_dialog import Adjust_Salary_Dialog
        window_controller.create_dialog(Adjust_Salary_Dialog(employee))

    @QtCore.Slot()
    def __cell_pressed(self, item):
        # Get the row index of the clicked item
        row = item.row()
        # Set rest of table as not selected
        self.clear_highlight()

        # Set the entire row as selected
        self.highlight_row(row)

    def highlight_row(self, row):
        # Highlight the entire row
        for col in range(self.columnCount()):
            item = self.item(row, col)
            item.setSelected(True)

    def clear_highlight(self):
        # Clear highlighting for all rows
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.item(row, col)
                item.setSelected(False)

    def leaveEvent(self, event):
        # Reset the row index when leaving the table
        self.row_under_mouse = -1
        self.clear_highlight()
        super(Table_Widget, self).leaveEvent(event)
