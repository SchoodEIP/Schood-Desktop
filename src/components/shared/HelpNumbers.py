from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QWidget, QLabel, QVBoxLayout

from src.components.Button import Button
from src.router.Route import Route
from src.stores import stores


class HelpNumberItem(QWidget):
    def __init__(self, parent, text, _id, callback):
        super().__init__(parent=parent)

        self._id = _id
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel(text)
        self.label.setStyleSheet("""
            QLabel {
                background-color: #FFFFFF;
                color: #4F23E2;
                font-size: 22px;
                font-weight: 600;
                padding: 12px;
                border-radius: 7px;
            }
                                 
            QLabel::hover {
                background-color: #9699FF;
                color: #FFFFFF;
            }
        """)
        self.layout.addWidget(self.label)

        self.label.mousePressEvent = lambda event: callback(self._id)


class HelpNumbersWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setStyleSheet("color: #000000")
        self.helpNumbers: [str, {str, QWidget}] = {}
        self.items = []  # List to store HelpNumberItem instances

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(32, 32, 128, 128)
        self.noItem = QLabel("Aucun numéro d'aide n'a été trouvé")

        self.layout.addWidget(self.noItem)

        self.setLayout(self.layout)

    def update(self):
        self.clear_layout()
        stores.helpNumbers.fetch_numbers()
        help_numbers = stores.helpNumbers.get_numbers()

        if len(help_numbers) == 0:
            self.noItem.show()
            return

        self.items = []  # Clear the list of items

        for helpNumber in help_numbers:
            item = HelpNumberItem(self, helpNumber["name"], helpNumber["_id"], self.click)
            self.items.append(item)  # Add the item to the list
            self.helpNumbers[helpNumber["_id"]] = {"widget": item, **helpNumber}
            self.layout.addWidget(item)

    def click(self, _id):
        stores.helpNumbers.set_selected({key: value for key, value in self.helpNumbers[_id].items() if key != "widget"})
        self.parent.parent.go_to("/helpNumber")

    def clear_layout(self):
        self.noItem.hide()
        for helpNumber in self.helpNumbers.values():
            self.layout.removeWidget(helpNumber["widget"])
            helpNumber["widget"].deleteLater()
        self.helpNumbers.clear()
        self.items.clear()  # Clear the items list


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