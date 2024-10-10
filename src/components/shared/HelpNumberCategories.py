from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QWidget, QLabel, QGraphicsDropShadowEffect, QSizePolicy
from PySide6.QtGui import QColor
from src.components.Button import Button
from src.router.Route import Route
from src.stores import stores


class HelpNumberInfo:
    def __init__(self, help_number_list_content: QLabel):
        self.help_number_list_content = help_number_list_content

    def clear_display(self):
        self.help_number_list_content.setText("Sélectionnez une aide")

    def setStyleSheet(self, style: str):
        self.help_number_list_content.setStyleSheet(style)

    def display_number_info(self, number_info):
        description = number_info.get('description', 'Description indisponible')
        location = number_info.get('location', 'Information indisponible')
        name = number_info.get('name', 'Information indisponible')
        phone = number_info.get('telephone', 'Information indisponible')
        hours = number_info.get('hours', 'Information indisponible')

        location_icon_svg = "src/images/location-dot-solid.svg"
        phone_icon_svg = "src/images/phone-solid.svg"
        hour_icon_svg = "src/images/clock-solid.svg"

        help_details = f"""
        <div style="margin: 20px;">
            <p style="font-size: 30px; font-weight: bold; text-align: center; margin-bottom: 50px;">{name}</p>

            <p style="font-size: 16px; text-align: left; margin-bottom: 50px;">{description}</p>

            <p style="font-size: 16px; text-align: left; margin-bottom: 10px;">
                <img src="{location_icon_svg}" width="18" height="18" style="vertical-align: middle; margin-right: 40px;">
                {location}
            </p>

            <p style="font-size: 16px; text-align: left; margin-bottom: 20px;">
                <img src="{phone_icon_svg}" width="18" height="18" style="vertical-align: middle; margin-right: 40px;">
                {phone}
            </p>

            <p style="font-size: 16px; text-align: left;">
                <img src="{hour_icon_svg}" width="18" height="18" style="vertical-align: middle; margin-right: 40px;">
                {hours}
            </p>
        </div>
        """

        self.help_number_list_content.setText(help_details)


class HelpNumberList:
    def __init__(self, categories, help_number_list_box, help_number_list_content):
        self.categories = categories
        self.help_number_list_box = help_number_list_box
        self.help_number_list = HelpNumberInfo(help_number_list_content)
        self.help_number_list_box.setSpacing(5)  # Set spacing between help_number_buttons to 5px

    def handle_click(self, _id):
        if _id not in self.categories:
            print(f"Category with ID {_id} not found!")
            return

        category_name = self.categories[_id]["name"]
        stores.helpNumbers.set_category(_id)
        stores.helpNumbers.fetch_numbers(_id)
        help_numbers = stores.helpNumbers.get_numbers()

        for i in reversed(range(self.help_number_list_box.count())):
            widget_to_remove = self.help_number_list_box.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()

        if help_numbers:
            for number_info in help_numbers:
                help_number_button = Button(parent=None, text=number_info['name'])
                help_number_button.setStyleSheet("""
                    QPushButton {
                        background-color: #FFFFFF;
                        color: #4F23E2;
                        font-size: 18px;
                        font-weight: 600;
                        padding: 8px;
                        border-radius: 5px;
                    }
                    QPushButton::hover {
                        background-color: #9699FF;
                        color: #FFFFFF;
                    }
                """)
                help_number_button.clicked.connect(lambda _, hn=number_info: self.help_number_list.display_number_info(hn))
                self.help_number_list_box.addWidget(help_number_button)
        else:
            no_help_label = QLabel("Liste de numéro indisponible")
            no_help_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_help_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            self.help_number_list_box.addWidget(no_help_label)

        self.help_number_list.clear_display()


class CategoryButton(Button):
    def __init__(self, parent, text, _id, callback):
        super().__init__(parent=parent, text=text)

        self._id = _id
        self.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #4F23E2;
                font-size: 21px;
                font-weight: 600;
                padding: 11px;
                border-radius: 7px;
                border: 1px solid #4F23E2;
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

        self.setStyleSheet("color: #292929")
        self.number_columns = 3
        self.categories = {}

        self.helpNumbersLayout = QVBoxLayout()

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(175, 86, 200, 128)

        # Adjust column stretch to prevent horizontal scroll
        for i in range(self.number_columns):
            self.layout.setColumnStretch(i, 1)

        self.setLayout(self.layout)

        self.help_number_list_box = QVBoxLayout()
        self.help_number_list_box.setSpacing(5)  # Set spacing between help number buttons
        self.help_number_list_box.setContentsMargins(0, 0, 0, 0)

        self.help_number_list = QWidget()
        self.help_number_list.setLayout(self.help_number_list_box)

        self.help_number_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.help_number_list.setMinimumSize(200, 400)
        self.help_number_list.setMaximumSize(600, 800)  # Adjust maximum size to prevent overflow
        self.help_number_list.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #4F23E2;
            border-radius: 7px;       
        """)

        self.number_info = QWidget()
        self.number_info.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #4F23E2;
            border-radius: 7px;
        """)

        self.help_number_layout = QVBoxLayout()
        self.help_number_layout.setContentsMargins(0, 0, 0, 0)

        self.help_number_list_content = QLabel("Sélectionnez une catégorie d'aide")
        self.help_number_list_content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.help_number_list_content.setStyleSheet("""
            font-size: 16px;
            margin: 0px;  
        """)
        self.help_number_list_content.setWordWrap(True)  # Ensure word wrapping to avoid overflow

        self.help_number_layout.addWidget(self.help_number_list_content)

        self.number_info.setLayout(self.help_number_layout)

        self.number_info.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.number_info.setMinimumSize(300, 400)
        self.number_info.setMaximumSize(1200, 800)  # Ensure it doesn't expand too wide

        self.click_handler = HelpNumberList(self.categories, self.help_number_list_box, self.help_number_list_content)

        self.update()

    def update(self):
        stores.helpNumberCategories.fetch_categories()
        categories = stores.helpNumberCategories.get_categories()

        self.categories.clear()

        for index, category in enumerate(categories):
            row = index // self.number_columns
            col = index % self.number_columns
            button = CategoryButton(self, category["name"], category["_id"], self.click_handler.handle_click)

            self.categories[category["_id"]] = {"button": button, "name": category["name"]}

            self.layout.addWidget(button, row, col)

        row = (len(categories) // self.number_columns) + 1

        self.layout.addWidget(self.help_number_list, row, 0, 1, 1)
        self.layout.addWidget(self.number_info, row, 1, 1, 3)

class HelpNumberCategories(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.setContentsMargins(32, 32, 32, 32)

        self.mainWidget = HelpNumberCategoriesWidget(self)

        self.title = QLabel("Mes catégories de numéro d'aide")
        self.title.setStyleSheet("""
            QLabel {
                font-size: 31px;
                font-weight: 600;
                color: #292929;
            }
        """)

        self.mainLayout.addWidget(self.title)
        self.mainLayout.addWidget(self.mainWidget)

        self.setLayout(self.mainLayout)