from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import *
from ui import ui_settings


class Dialog_Window(QDialog):

    def __init__(self, widget: QWidget = None, parent=None):

        super(Dialog_Window, self).__init__(parent)

        self.custom_layout = QVBoxLayout()
        self.setLayout(self.custom_layout)

        if not widget:
            self.button_switch = QPushButton("Switch Widget")
            self.test_layout()
        else:
            self.set_widget(widget)

    def test_layout(self):
        # Example widgets
        label = QLabel("This is the initial widget")
        self.custom_layout.addWidget(label)
        self.button_switch.clicked.connect(self.clear_widgets)
        self.custom_layout.addWidget(self.button_switch)

    def clear_widgets(self):
        # Clear existing widgets from the layout
        while self.custom_layout.count():
            item = self.custom_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

    def set_widget(self, widget: QWidget):
        self.custom_layout.addWidget(widget)

    # sets background color
    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        rect = event.rect()
        painter = QtGui.QPainter(self)
        painter.fillRect(rect, ui_settings.background_color)

