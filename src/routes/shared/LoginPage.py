from PySide6 import QtWidgets, QtCore, QtGui

from src.HttpRequest import httpRequest
from src.User import user
from src.router.Route import Route


class Button(QtWidgets.QPushButton):
    def __init__(self):
        super().__init__()
        self.setText("Connexion")
        self.setFixedHeight(55)
        self.setFixedWidth(200)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4F23E2;
                border-radius: 26px;
                color: #FFFFFF;
                font-size: 22px;
            }
            QPushButton:hover {
                background-color: #4F23C2;
            }
        """)


class TextInput(QtWidgets.QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setFixedHeight(46)
        self.setFixedWidth(300)
        self.setStyleSheet("background-color: #FFD2D5;"
                           "border-radius: 23px;"
                           "padding-left: 16px")
        self.setPlaceholderText(placeholder)


class LabeledInput(QtWidgets.QWidget):
    def __init__(self, placeholder=""):
        super().__init__()

        self.inputLayout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel(placeholder.capitalize())
        self.label.setStyleSheet("color: #4F23E2;"
                                 "font-size: 22px;"
                                 "font-weight: 600;")
        self.input = TextInput(placeholder)
        self.inputLayout.addWidget(self.label, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.inputLayout.addWidget(self.input, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.inputLayout)


class Image(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()

        self.logoImage = QtGui.QPixmap("src/images/logo_schood.png")
        self.setPixmap(self.logoImage)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(247)
        self.setFixedWidth(356)


class LoginPage(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.logo = Image()
        self.email = LabeledInput("email")
        self.password = LabeledInput("mot de passe")
        self.forgotPassword = QtWidgets.QPushButton("Mot de passe oublié ? Cliquez ici")
        self.forgotPassword.setStyleSheet("background-color: #FFFFFF;"
                                          "border: none;"
                                          "color: #4F23E2;"
                                          "font-size: 12px;"
                                          "font-weight: 600;")
        self.loginButton = Button()
        self.errorText = QtWidgets.QLabel("")
        self.errorText.setStyleSheet("color: #FF0000;"
                                     "font-size: 22px;")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.layout.setSpacing(24)
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

    @QtCore.Slot()
    def login(self):
        try:
            email = self.email.input.text()
            password = self.password.input.text()

            if len(email) == 0 or len(password) == 0:
                self.errorText.setText("L'email ou le mot de passe est vide.")
                return
            data = {
                "email": email,
                "password": password
            }
            res = httpRequest.post("/user/login", data=data)
            if res.status_code == 200:
                user.connect_user(res.json())
                self.parent.go_to("/")
            elif res.status_code == 400 or res.status_code == 401:
                self.errorText.setText("Email ou mot de passe incorrect.")
            else:
                self.errorText.setText("Erreur server, veuillez réessayer plus tard.")
        except Exception as e:
            print(e)

    def forgot_password(self):
        print("A faire")
