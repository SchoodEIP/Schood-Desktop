from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QWidget, QLabel, QScrollArea, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
from src.components.Button import Button
from src.router.Route import Route
from src.stores import stores


# Class for displaying number info with its own setStyleSheet
class HelpNumberInfo:
    def __init__(self, help_number_info_content: QLabel):
        # This QLabel will be updated with number info
        self.help_number_info_content = help_number_info_content
    #     self.apply_styles()

    # def apply_styles(self):
    #     # Apply its own stylesheet
    #     self.setStyleSheet("""
    #         QLabel {
    #             background-color: #FFFFFF;
    #             color: #4F23E2;
    #             font-size: 20px;
    #             font-weight: bold;
    #             padding: 10px;
    #             border: 2px solid #4F23E2;
    #             border-radius: 7px;
    #         }
    #     """)

    def clear_display(self):
        # Clears the QLabel content
        self.help_number_info_content.setText("Sélectionnez une aide")

    def setStyleSheet(self, style: str):
        # Set the stylesheet for the help_number_info_content QLabel
        self.help_number_info_content.setStyleSheet(style)

    def display_number_info(self, number_info):
        name = number_info.get('name', 'N/A')
        phone = number_info.get('telephone', 'N/A')
        email = number_info.get('email', 'N/A')
        description = number_info.get('description', 'No description available')

        help_details = f"""
        <p>
            <span style="font-size: 40px; font-weight: bold;">{name}</span> <br>
            <span style="font-size: 28px;">{description}</span> <br>
            Telephone: {phone} <br>
            Email: {email}
        </p>
        """

        # Update the QLabel with the number details
        self.help_number_info_content.setText(help_details)


# Class to handle click events and with its own setStyleSheet
class HelpNumberList:
    def __init__(self, categories, help_number_list_box, help_number_info_content):
        self.categories = categories
        self.help_number_list_box = help_number_list_box
        self.help_number_info = HelpNumberInfo(help_number_info_content)
    #     self.apply_styles()

    # def apply_styles(self):
    #     # Apply its own stylesheet for service displayer specific elements
    #     self.help_number_info.setStyleSheet("""
    #         QLabel {
    #             background-color: #FFFFFF;
    #             color: #292929;
    #             font-size: 18px;
    #             padding: 12px;
    #             border: 2px solid #FF0000;
    #             border-radius: 7px;
    #         }
    #     """)

    def handle_click(self, _id):
        if _id not in self.categories:
            print(f"Category with ID {_id} not found!")
            return

        category_name = self.categories[_id]["name"]
        stores.helpNumbers.set_category(_id)
        stores.helpNumbers.fetch_numbers(_id)
        help_numbers = stores.helpNumbers.get_numbers()

        # Clear the existing widgets in the layout
        for i in reversed(range(self.help_number_list_box.count())):
            widget_to_remove = self.help_number_list_box.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()

        # Populate the layout with the new help numbers
        if help_numbers:
            for number_info in help_numbers:
                help_button = Button(parent=None, text=number_info['name'])
                help_button.setStyleSheet("""
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
                help_button.clicked.connect(lambda _, hn=number_info: self.help_number_info.display_number_info(hn))
                self.help_number_list_box.addWidget(help_button)
        else:
            no_help_label = QLabel("No help numbers available")
            no_help_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_help_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            self.help_number_list_box.addWidget(no_help_label)

        # Clear the display until a help number is clicked
        self.help_number_info.clear_display()


# Class for the category button
class CategoryButton(Button):
    def __init__(self, parent, text, _id, callback):
        super().__init__(parent=parent, text=text)

        self._id = _id
        self.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                color: #4F23E2;
                font-size: 22px;
                font-weight: 600;
                padding: 12px;
                border-radius: 7px;
            }
            
            QPushButton::hover {
                background-color: #9699FF;
                color: #FFFFFF;
            }
        """)

        self.clicked.connect(lambda: callback(self._id))


# Main widget class for Help Number Categories
class HelpNumberCategoriesWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.setStyleSheet("color: #292929")
        self.number_columns = 5
        self.categories = {}

        self.helpNumbersLayout = QVBoxLayout()

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(200, 86, 200, 128)

        for i in range(self.number_columns):
            self.layout.setColumnStretch(i, 1)

        self.setLayout(self.layout)

        self.help_number_list_box = QVBoxLayout()

        self.help_numbers_scroll = QScrollArea()
        self.help_numbers_scroll.setWidgetResizable(True)
        self.help_numbers_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.help_numbers_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.help_numbers_scroll.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background-color: #ffffff;
                width: 7px;
                margin: 0px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background-color: #9699FF;
                border-radius: 3px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background-color: #f0f0f0;
                height: 0px;
            }
        """)
        
        self.help_number_info = QWidget()
        self.help_number_info.setLayout(self.help_number_list_box)
        self.help_number_info.setFixedSize(190, 620)
        self.help_number_info.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #4F23E2;
            border-radius: 7px;       
        """)

        self.help_numbers_scroll.setWidget(self.help_number_info)

        self.number_info = QWidget()
        self.number_info.setStyleSheet("""
            background-color: #ffffff;
            border: 2px solid #FF0000;
            border-radius: 7px;
        """)

        self.help_number_layout = QVBoxLayout()

        self.help_number_info_content = QLabel("Sélectionnez une catégorie d'aide")
        self.help_number_info_content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.help_number_info_content.setStyleSheet("font-size: 16px;")

        self.help_number_layout.addWidget(self.help_number_info_content)

        self.number_info.setLayout(self.help_number_layout)
        self.number_info.setFixedSize(900, 620)

        # Initialize the HelpNumberList with the necessary data
        self.click_handler = HelpNumberList(self.categories, self.help_number_list_box, self.help_number_info_content)

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

            # button.setFixedSize(150, 50)
            self.layout.addWidget(button, row, col)

        row = (len(categories) // self.number_columns) + 1

        # Add scroll area and help number widget to the layout
        self.layout.addWidget(self.help_numbers_scroll, row, 0, 1, 1)
        self.layout.addWidget(self.number_info, row, 1, 1, 3)


# Route class for Help Number Categories
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
                font-size: 32px;
                font-weight: 600;
                color: #292929;
            }
        """)

        self.mainLayout.addWidget(self.title)
        self.mainLayout.addWidget(self.mainWidget)

        self.setLayout(self.mainLayout)