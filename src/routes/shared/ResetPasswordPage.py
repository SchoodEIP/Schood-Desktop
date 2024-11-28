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
                           "color: #292929;"
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


class ResetPasswordPage(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.logo = Image()
        self.email = LabeledInput("Adresse email")

        self.resetButton = Button(text="Demander un nouveau mot de passe", width=415, height=55, style_sheet="""
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

        self.homeButton = Button(text="Retour à l'accueil", style_sheet="""
                            QPushButton {
                                background-color: #FFFFFF;
                                border: none;
                                color: #4F23E2;
                                font-size: 12px;
                                font-weight: 600;
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
        self.layout.addWidget(self.resetButton, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.homeButton, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.errorText, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch()
        self.resetButton.clicked.connect(self.reset)
        self.homeButton.clicked.connect(self.home)
        self.setLayout(self.layout)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.reset()

    @QtCore.Slot()
    def reset(self):
        try:
            email = self.email.input.text()

            if len(email) == 0:
                self.errorText.setText("L'email est vide.")
                return
            data = {
                "email": email
            }
            res = stores.request.post("/user/forgottenPassword?mail=true", data=data)
            print(res)
            if res.status_code == 200:
                self.parent.go_to("/login")
            elif res.status_code == 400 or res.status_code == 401:
                self.errorText.setText("Email  incorrect.")
            else:
                self.errorText.setText("Erreur server, veuillez réessayer plus tard.")
        except Exception as e:
            print(e)

    @QtCore.Slot()
    def home(self):
        self.parent.go_to("/login")
