from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QScrollArea, QWidget, QGridLayout, QLabel, QVBoxLayout, QSizePolicy, QPushButton, \
    QLineEdit, QComboBox, QListView

from src.components.Button import Button
from src.components.MultiComboBox import MultiSelectComboBox
from src.router.Route import Route
from src.routes.shared.LoginPage import TextInput
from src.stores import stores


class NormalInput(QWidget):
    def __init__(self, parent, label):
        super().__init__(parent)

        self.parent = parent

        self.label = QLabel(label)
        self.input = QLineEdit()
        self.input.setMinimumWidth(200)
        self.input.setPlaceholderText(label)
        self.label.setStyleSheet("color: #292929; font-size: 22px; font-weight: 600;")
        self.input.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                color: #4F23E2;
                border-radius: 10px;
                padding-left: 20px;
                padding-top: 14px;
                padding-bottom: 14px;
                font-size: 14px;
                font-weight: 600;
            }
        """)
        self.errorMessage = QLabel("Ce champs est obligatoire.")
        self.errorMessage.setStyleSheet("color: #DD0000;")

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.errorMessage)

        self.hide_error()

        self.setLayout(self.layout)

    def show_error(self):
        self.errorMessage.setStyleSheet("color: #DD0000;")

    def hide_error(self):
        self.errorMessage.setStyleSheet("color: #FFFFFF;")

    def reset(self):
        self.hide_error()
        self.input.setText("")


class SelectInput(QWidget):
    def __init__(self, parent, label, items):
        super().__init__(parent)

        self.parent = parent
        self.items = items

        self.label = QLabel(label)
        self.label.setStyleSheet("color: #292929; font-size: 22px; font-weight: 600;")
        self.input = QComboBox()
        self.input.setPlaceholderText(label)
        self.input.setMinimumWidth(200)
        self.errorMessage = QLabel("Ce champs est obligatoire.")
        self.errorMessage.setStyleSheet("color: #FFFFFF;")
        self.selectedOption = ""

        self.input.setStyleSheet("""
            QComboBox {
                background-color: #F0F0F0;
                color: #4F23E2;
                border-radius: 10px;
                padding-left: 20px;
                padding-top: 14px;
                padding-bottom: 14px;
                font-size: 14px;
                font-weight: 600;
            }
            
            QComboBox:drop-down {
                border: none;
            }
            
            QComboBox QAbstractItemView {
                background-color: #F0F0F0;
                color: #000000;
            }
        """)

        self.input.addItems(self.items.keys())
        self.input.currentIndexChanged.connect(self.on_option_selected)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.errorMessage)

        self.hide_error()

        self.setLayout(self.layout)

    def show_error(self):
        self.errorMessage.setStyleSheet("color: #DD0000;")

    def hide_error(self):
        self.errorMessage.setStyleSheet("color: #FFFFFF;")

    def on_option_selected(self, option=None):
        if option is not None and type(option) == str:
            self.selectedOption = self.items[option]
            idx = 0
            for key in self.items.keys():
                if key == option:
                    self.input.setCurrentIndex(idx)
                idx += 1
            return
        self.selectedOption = self.items[self.input.currentText()]

    def reset(self):
        self.hide_error()
        self.selectedOption = ""


class MultiSelectInput(QWidget):
    def __init__(self, parent, label, items):
        super().__init__(parent)

        self.parent = parent
        self.items = items
        self.selectedOptions = []

        self.label = QLabel(label)
        self.label.setStyleSheet("color: #292929; font-size: 22px; font-weight: 600;")
        self.input = QListView()
        self.input.setMinimumWidth(200)
        self.input.setFixedHeight(45)
        self.model = QStandardItemModel()

        self.errorMessage = QLabel("Veuillez choisir au moins une option.")

        self.input.setStyleSheet("""
            QListView {
                background-color: #F0F0F0;
                color: #4F23E2;
                border-radius: 10px;
                padding-left: 20px;
                font-size: 14px;
                font-weight: 600;
            }

            QListView:drop-down {
                border: none;
            }

            QListView QAbstractItemView {
                background-color: #F0F0F0;
                color: #000000;
            }
        """)

        for key in self.items.keys():
            item = QStandardItem(key)
            item.setCheckable(True)
            item.setCheckState(Qt.CheckState.Unchecked)
            item.setEditable(False)
            self.model.appendRow(item)

        self.model.itemChanged.connect(self.on_item_selected)
        self.input.setModel(self.model)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.errorMessage)

        self.hide_error()

        self.setLayout(self.layout)

    def show_error(self):
        self.errorMessage.setStyleSheet("color: #DD0000;")

    def hide_error(self):
        self.errorMessage.setStyleSheet("color: #FFFFFF;")

    def on_item_selected(self, item, forced=False):
        item_id = self.items[item.text()] if type(forced) != bool or not forced else item
        if item_id in self.selectedOptions:
            self.selectedOptions.remove(item_id)
        else:
            self.selectedOptions.append(item_id)
        if forced:
            item_text = None
            for key, value in self.items.items():
                if value == item_id:
                    item_text = key
                    break
            if item_text is None:
                return
            for row in range(self.model.rowCount()):
                i = self.model.item(row)
                if i.text() == item_text:
                    i.setCheckState(Qt.CheckState.Checked)
                    break

    def reset(self):
        self.hide_error()
        self.selectedOptions = []


class ModifyUserInfoAdminWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setStyleSheet("color: #000000;")
        self.user = None

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(40)

        self.facilitiesItems = {}

        self.firstname = NormalInput(self, "Prénom")
        self.lastname = NormalInput(self, "Nom")
        self.email = NormalInput(self, "Email")

        self.layout.addWidget(self.firstname)
        self.layout.addWidget(self.lastname)
        self.layout.addWidget(self.email)

        self.setLayout(self.layout)
        self.setMaximumWidth(750)
        self.setMaximumHeight(500)

    def update(self):
        self.init_user()
        self.init_roles()

    def reset(self):
        self.lastname.reset()
        self.firstname.reset()
        self.email.reset()

    def init_roles(self):
        stores.roles.fetch_roles()

    def init_user(self):
        self.user = stores.users.get_selected_user()
        if self.user is None:
            return
        self.lastname.input.setText(self.user["lastname"])
        self.firstname.input.setText(self.user["firstname"])
        self.email.input.setText(self.user["email"])
