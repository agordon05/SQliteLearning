from PySide6.QtGui import Qt, QFont
from PySide6 import QtGui, QtWidgets, QtCore

window_title = "Employee Database"

# Color
background_color: QtGui.QColor = QtGui.QColor(40, 40, 40)  # Dark gray or black
text_color: QtGui.QColor = QtGui.QColor(210, 210, 210)  # Light gray or off-white
table_selected_color: QtGui.QColor = QtGui.QColor("#505050")
button_color: QtGui.QColor = QtGui.QColor(Qt.GlobalColor.gray)
header_color: QtGui.QColor = QtGui.QColor(50, 50, 50)  # Replace with your preferred RGB values
click_color: QtGui.QColor = QtGui.QColor(Qt.GlobalColor.darkGray)
hover_color: QtGui.QColor = QtGui.QColor('#005050')
green_color: QtGui.QColor = QtGui.QColor(Qt.GlobalColor.darkGreen)
red_color: QtGui.QColor = QtGui.QColor(Qt.GlobalColor.red)
yellow_color: QtGui.QColor = QtGui.QColor(Qt.GlobalColor.yellow)
orange_color: QtGui.QColor = QtGui.QColor('#ffa500')


# Style Sheet
button_stylesheet = "background-color: {};".format(button_color.name())
label_stylesheet = "color: {};".format(text_color.name())
green_label_stylesheet = "color: {}; background-color: {};".format(green_color.name(), background_color.name())
red_label_stylesheet = "color: {}; background-color: {};".format(red_color.name(), background_color.name())

table_header_stylesheet = "background-color: {}; color: {}".format(header_color.name(), text_color.name())


# Styled Dark Mode Table Style Sheet
table_stylesheet_dark_mode = (
    "QTableWidget {"
    "    background-color: %s;"
    "}"
    "QTableWidget::item {"
    "    border-bottom: 1px solid #000000;"
    "}"
    "QTableWidget::item:selected {"
    "    background-color: %s;"
    "}"
) % (background_color.name(), table_selected_color.name())


# Font
table_font = QFont()
table_font.setPointSize(18)

table_header_font = QFont("Arial", 14)  # Replace with your preferred font and size
table_header_font.setBold(True)

page_name_font = QFont()
page_name_font.setPointSize(30)

page_data_font = QFont()
page_data_font.setPointSize(18)


# Sizes
dialog_width: int = 400
dialog_height: int = 300
dialog_text_min_width = 100
dialog_text_max_height = 30
dialog_num_min_width = 100
dialog_num_max_height = 30
key_text_max_char = 75
dialog_new_bot_height = 620


# # text validators
int_validator = "int"
float_validator = "float"
char_validator = "char"
key_validator = "key"

ui_refresh_rate = 60000  # 1 Minute


def format_page_name(widget: QtWidgets.QLabel):
    widget.setFont(page_name_font)
    widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    widget.setStyleSheet(label_stylesheet)


def format_label(widget: QtWidgets.QLabel):
    widget.setFont(page_data_font)
    widget.setStyleSheet(label_stylesheet)
    widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)


def format_green_label(widget: QtWidgets.QLabel):
    widget.setFont(page_data_font)
    widget.setStyleSheet(green_label_stylesheet)
    widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)


def format_red_label(widget: QtWidgets.QLabel):
    widget.setFont(page_data_font)
    widget.setStyleSheet(red_label_stylesheet)
    widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)


def format_button(widget: QtWidgets.QPushButton):
    widget.setStyleSheet(button_stylesheet)


def format_text_field(widget: QtWidgets.QLineEdit, validator_type: str = int_validator, max_length: int = 8, decimal_places: int = 2):

    widget.setMinimumWidth(dialog_num_min_width)
    widget.setMaximumHeight(dialog_num_max_height)
    widget.setMaxLength(max_length)

    if validator_type == int_validator:
        validator = QtGui.QIntValidator()
        widget.setValidator(validator)

    elif validator_type == float_validator:
        validator = QtGui.QDoubleValidator(widget)
        validator.setNotation(QtGui.QDoubleValidator.Notation.StandardNotation)
        validator.setDecimals(decimal_places)
        widget.setValidator(validator)

    elif validator_type == char_validator:
        validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[a-zA-Z0-9]+"), widget)
        widget.setValidator(validator)

    elif validator_type == key_validator:
        widget.setMaxLength(key_text_max_char)
        validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression("[a-zA-Z0-9]+"), widget)
        widget.setValidator(validator)


def format_chart(widget: QtWidgets.QWidget):
    widget.setMaximumHeight(400)
    widget.setMaximumWidth(900)
    widget.setMinimumWidth(800)


def align_horizontal(items: [], stretch_beginning: bool = False, stretch_end: bool = False,
                     stretch_middle: bool = False) -> QtWidgets.QWidget:
    hor = QtWidgets.QWidget()
    hor.setLayout(QtWidgets.QHBoxLayout())

    if stretch_beginning is True:
        hor.layout().addStretch()

    for count, item in enumerate(items):
        hor.layout().addWidget(item)
        if stretch_middle is True and count < len(items) - 1:
            hor.layout().addStretch()

    if stretch_end is True:
        hor.layout().addStretch()

    return hor


def align_vertical(items: [], stretch_beginning: bool = False, stretch_end: bool = False,
                   stretch_middle: bool = False) -> QtWidgets.QWidget:
    ver = QtWidgets.QWidget()
    ver.setLayout(QtWidgets.QVBoxLayout())

    if stretch_beginning is True:
        ver.layout().addStretch()

    for count, item in enumerate(items):
        ver.layout().addWidget(item)
        if stretch_middle is True and count < len(items) - 1:
            ver.layout().addStretch()

    if stretch_end is True:
        ver.layout().addStretch()

    return ver
