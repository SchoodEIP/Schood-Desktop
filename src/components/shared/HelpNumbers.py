from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QWidget, QGridLayout, QLabel, QVBoxLayout

from src.components.Button import Button
from src.router.Route import Route
from src.stores import stores


class HelpNumberButton(Button):
    def __init__(self, parent, text, _id, callback):
        super().__init__(parent=parent, text=text)

        self._id = _id
        self.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #4F23E2;
                border: 4px solid #4F23E2;
                font-size: 20px;
                font-weight: 600;
                padding: 12px;
                border-radius: 16px;
            }

            QPushButton::hover {
                background-color: #4F23E2;
                color: #FFFFFF;
            }
        """)

        self.clicked.connect(lambda: callback(self._id))


class HelpNumbersWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setStyleSheet("color: #000000")
        self.number_columns = 3

        self.helpNumbers: [str, {str, QWidget}] = {}

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(32, 32, 128, 128)
        self.layout.setSpacing(32)
        self.noItem = QLabel("Aucun numéro d'aide n'a été trouvé")

        self.layout.addWidget(self.noItem, 0, 0)

        self.setLayout(self.layout)

    def update(self):
        self.clear_layout()
        stores.helpNumbers.fetch_numbers()
        help_numbers = stores.helpNumbers.get_numbers()

        if len(help_numbers) == 0:
            self.noItem.show()
            return

        for index, helpNumber in enumerate(help_numbers):
            row = index // self.number_columns
            col = index % self.number_columns
            widget: HelpNumberButton = HelpNumberButton(self, helpNumber["name"], helpNumber["_id"], self.click)
            self.helpNumbers[helpNumber["_id"]] = {"widget": widget, **helpNumber}
            self.layout.addWidget(widget, row, col)

        for i in range(self.number_columns):
            self.layout.setColumnStretch(i, 1)

    def click(self, _id):
        stores.helpNumbers.set_selected({key: value for key, value in self.helpNumbers[_id].items() if key != "widget"})
        self.parent.parent.go_to("/helpNumber")

    def clear_layout(self):
        self.noItem.hide()
        for helpNumber in self.helpNumbers.values():
            self.layout.removeWidget(helpNumber["widget"])
            helpNumber["widget"].deleteLater()
        self.helpNumbers.clear()


class HelpNumbers(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.setContentsMargins(32, 32, 0, 0)

        self.mainWidget = HelpNumbersWidget(self)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.mainWidget)

        self.title = QLabel("Mes numéros d'aide")
        self.title.setStyleSheet("""
            QLabel {
                font-size: 30px;
                font-weight: 600;
                color: #292929;
            }
        """)

        self.backButton = Button(text="Retour", parent=self, callback=lambda: self.parent.go_to("/help"), style_sheet="""
            QPushButton {
                background-color: #FFFFFF;
                color: #4F23E2;
                border: none;
                font-size: 20px;
                font-weight: 600;
            }

            QPushButton:hover {
                text-decoration: underline;
            }
        """)

        self.mainLayout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.addSpacing(32)
        self.mainLayout.addWidget(self.backButton, alignment=Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.addWidget(self.scrollArea)

        self.setLayout(self.mainLayout)

        self.scrollArea.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 14px;
                margin: 0px 0px 0px 0px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background: #FFD2D5;
                border-radius: 7px;
            }
            QScrollBar::add-line:vertical {
                border: none;
                background: #f0f0f0;
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                border: none;
                background: #f0f0f0;
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar:horizontal {
                border: none;
                background: #f0f0f0;
                width: 14px;
                margin: 0px 0px 0px 0px;
                border-radius: 7px;
            }
            QScrollBar::handle:horizontal {
                background: #FFD2D5;
                border-radius: 7px;
            }
            QScrollBar::add-line:horizontal {
                border: none;
                background: #f0f0f0;
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:horizontal {
                border: none;
                background: #f0f0f0;
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
                border: none;
                background: none;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """)

    def update(self):
        self.mainWidget.update()
