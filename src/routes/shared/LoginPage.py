from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QLineEdit

from src.components.Button import Button
from src.router.Route import Route
from src.stores import stores
from src.utils.ressources import images_path


class TextInput(QtWidgets.QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setFixedHeight(46)
        self.setFixedWidth(300)
        self.setStyleSheet("background-color: #EAEAEA;"
                           "color: #FFFFFF;"
                           "border-radius: 10px;"
                           "padding-left: 16px")
        self.setPlaceholderText(placeholder)


class LabeledInput(QtWidgets.QWidget):
    def __init__(self, placeholder="", password=False):
        super().__init__()

        self.inputLayout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel(placeholder.capitalize())
        self.label.setStyleSheet("color: #4F23E2;"
                                 "font-size: 22px;"
                                 "font-weight: 400;")
        self.input = TextInput(placeholder)
        if password:
            self.input.setEchoMode(QLineEdit.Password)
        self.inputLayout.addWidget(self.label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.inputLayout.addWidget(self.input, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.inputLayout)


class Image(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()

        self.logoImage = QtGui.QPixmap(images_path("logo_schood.png"))
        self.setPixmap(self.logoImage)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(227)
        self.setFixedWidth(356)


class LoginPage(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.logo = Image()
        self.email = LabeledInput("Email")
        self.password = LabeledInput("Mot de passe", True)
        self.forgotPassword = Button(text="Mot de passe oublié ? Cliquez ici", style_sheet="""
                    QPushButton {
                        background-color: #FFFFFF;
                        border: none;
                        color: #4F23E2;
                        font-size: 12px;
                        font-weight: 600;
                    }
                """)

        self.loginButton = Button(text="Connexion", width=200, height=55, style_sheet="""
                    QPushButton {
                        background-color: #4F23E2;
                        border-radius: 10px;
                        color: #FFFFFF;
                        font-size: 22px;
                    }
                    QPushButton:hover {
                        background-color: #4F23C2;
                    }
                """)
        self.errorText = QtWidgets.QLabel("")
        self.errorText.setStyleSheet("color: #FF0000;"
                                     "font-size: 22px;")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.layout.addStretch()
        self.layout.addWidget(self.logo, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.email, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.password.inputLayout.addWidget(self.forgotPassword, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.password, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch()
        self.layout.addWidget(self.loginButton, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.errorText, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch()
        self.loginButton.clicked.connect(self.login)
        self.forgotPassword.clicked.connect(self.forgot_password)
        self.setLayout(self.layout)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.login()

    @QtCore.Slot()
    def login(self):
        try:
            # email = self.email.input.text()
            # password = self.password.input.text()
            email = "alice.johnson.Schood1@schood.fr"
            password = "Alice_123"

            if len(email) == 0 or len(password) == 0:
                self.errorText.setText("L'email ou le mot de passe est vide.")
                return
            data = {
                "email": email,
                "password": password
            }
            # data = {
            #     "email": "pierre.dubois.Schood1@schood.fr",
            #     "password": "Pierre_123"
            # }
            res = stores.request.post("/user/login", data=data)
            if res.status_code == 200:
                stores.user.connect_user(res.json())
                self.parent.init_roles_routes()
                self.parent.go_to("/")
                self.email.input.setText("")
                self.password.input.setText("")
                self.errorText.setText("")
            elif res.status_code == 400 or res.status_code == 401:
                self.errorText.setText("Email ou mot de passe incorrect.")
            else:
                self.errorText.setText("Erreur server, veuillez réessayer plus tard.")
        except Exception as e:
            print(e)

    def forgot_password(self):
        print("A faire")
