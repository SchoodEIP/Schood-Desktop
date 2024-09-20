from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QWidget, QGridLayout, QLabel, QVBoxLayout, QSizePolicy, QPushButton

from src.components.Button import Button
from src.components.admin.ModifyUserInfoAdmin import ModifyUserInfoAdminWidget
from src.components.shared.ModifyUserInfo import ModifyUserInfoWidget
from src.router.Route import Route
from src.stores import stores


class CreateAccountAdmin(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.setContentsMargins(32, 32, 0, 0)

        self.mainWidget = QWidget()

        self.subWidget = ModifyUserInfoAdminWidget(self)

        self.creationError = QLabel("")
        self.creationError.setStyleSheet("color: #DD0000;")

        self.createAccount = QPushButton("Créer le compte")
        self.createAccount.setStyleSheet("""
            QPushButton {
                background-color: #4F23E2;
                color: #FFFFFF;
                border: 2px solid #4F23E2;
                padding: 14px;
                border-radius: 10px;
                font-size: 22px;
            }
        """)
        self.createAccount.clicked.connect(self.create_account_callback)

        self.subLayout = QVBoxLayout()
        self.subLayout.setSpacing(20)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.mainWidget)

        self.backButton = Button(text="Retour", parent=self, callback=self.back_button_callback, style_sheet="""
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
        self.title = QLabel("Création d'un compte")
        self.title.setStyleSheet("""
            QLabel {
                font-size: 30px;
                font-weight: 600;
                color: #292929;
            }
        """)

        self.subLayout.addWidget(self.subWidget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.subLayout.addWidget(self.createAccount, alignment=Qt.AlignmentFlag.AlignCenter)
        self.subLayout.addWidget(self.creationError, alignment=Qt.AlignmentFlag.AlignCenter)

        self.creationError.hide()

        self.mainWidget.setLayout(self.subLayout)

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
        self.subWidget.update()

    def back_button_callback(self):
        stores.users.set_selected_user(None)
        self.subWidget.reset()
        self.parent.go_to("/manage")

    def create_account_callback(self):
        lastname = self.subWidget.lastname.input.text()
        firstname = self.subWidget.firstname.input.text()
        email = self.subWidget.email.input.text()
        facility = self.subWidget.facility.selectedOption
        error = False

        if lastname == "":
            error = True
            self.subWidget.lastname.show_error()
        else:
            self.subWidget.lastname.hide_error()
        if firstname == "":
            error = True
            self.subWidget.firstname.show_error()
        else:
            self.subWidget.firstname.hide_error()
        if email == "":
            error = True
            self.subWidget.email.show_error()
        else:
            self.subWidget.email.hide_error()
        if facility == "":
            error = True
            self.subWidget.facility.show_error()
        else:
            self.subWidget.facility.hide_error()

        if error:
            return

        res = stores.users.create_user(lastname, firstname, email, None, None, None)
        if res.status_code == 200:
            self.back_button_callback()
        else:
            self.creationError.setText(res.json()["message"])
            self.creationError.show()