from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QWidget, QScrollArea, QPushButton, QVBoxLayout, QLabel

from src.components.Button import Button
from src.router.Route import Route
from src.stores import stores


class CategoryButton(Button):
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


class HelpNumberCategoriesWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.setStyleSheet("color: #000000")
        self.number_columns = 3

        self.categories: [str, {str, QWidget}] = {}

        self.helpNumbersLayout = QVBoxLayout()

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(32, 32, 128, 128)
        self.layout.setSpacing(32)

        self.setLayout(self.layout)

    def update(self):
        stores.helpNumberCategories.fetch_categories()
        categories = stores.helpNumberCategories.get_categories()

        for index, category in enumerate(categories):
            row = index // self.number_columns
            col = index % self.number_columns
            widget: CategoryButton = CategoryButton(self, category["name"], category["_id"], self.click)
            self.categories[category["_id"]] = {"widget": widget, "name": category["name"]}
            self.layout.addWidget(widget, row, col)

        for i in range(self.number_columns):
            self.layout.setColumnStretch(i, 1)

    def click(self, _id):
        stores.helpNumbers.set_category(_id)
        self.parent.parent.go_to("/helpNumbers")


class HelpNumberCategories(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.setContentsMargins(32, 32, 0, 0)

        self.mainWidget = HelpNumberCategoriesWidget(self)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.mainWidget)
        self.title = QLabel("Mes catégories de numéro d'aide")
        self.title.setStyleSheet("""
            QLabel {
                font-size: 30px;
                font-weight: 600;
                color: #292929;
            }
        """)

        self.mainLayout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignLeft)
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
