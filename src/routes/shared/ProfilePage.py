import base64

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize, Qt
from PySide6 import QtWidgets, QtCore
from PySide6.QtSvgWidgets import QSvgWidget

from src.router.Route import Route
from src.utils import globalVars
from src.utils.ressources import images_path

class ProfilePicture(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("""
            QWidget {
                padding: 0px 0px;
            }
        """)

        self.setFixedHeight(200)

        self.picture = QLabel()
        self.imageProfile = QPixmap()

        self.picture.setStyleSheet("""
            QWidget {
                color: #4F23E2;
                font-weight: 600;
                font-size: 25px;
                padding: 0px
            }
        """)

        if globalVars.user.picture is None or len(globalVars.user.picture.split(",")) != 2:
            self.picture = QSvgWidget(images_path("circle_account.svg"))
            self.picture.setFixedSize(QSize(200, 200))
        else:
            self.imageProfile.loadFromData(base64.b64decode(globalVars.user.picture.split(",")[1]))
            self.imageProfile = self.imageProfile.scaled(200, 200, Qt.AspectRatioMode.IgnoreAspectRatio,
                                                         Qt.TransformationMode.SmoothTransformation)
            self.picture.setPixmap(self.imageProfile)

        self.layout.addWidget(self.picture)
        self.setLayout(self.layout)

class InformationLabel(QtWidgets.QWidget):
    def __init__(self, infotitle="", info=""):
        super().__init__()

        self.label = QtWidgets.QLabel(infotitle)
        self.label.setStyleSheet(
            "color: #4F23E2;" "font-size: 22px;" "font-weight: 600;"
        )
        self.data = QtWidgets.QLabel(info)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.data)
        self.setLayout(layout)

class ProfilePage(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.profilepicture = ProfilePicture()
        self.firstname = InformationLabel("First Name:", "")
        self.firstname.data.setStyleSheet("color: #000000;" "font-size: 22px;" "font-weight: 600;")
        self.lastname = InformationLabel("Last Name:", "")
        self.lastname.data.setStyleSheet("color: #000000;" "font-size: 22px;" "font-weight: 600;")
        self.classes = InformationLabel("Classe:", "")
        self.classes.data.setStyleSheet("color: #000000;" "font-size: 22px;" "font-weight: 600;")
        self.email = InformationLabel("Email:", "")
        self.email.data.setStyleSheet("color: #000000;" "font-size: 22px;" "font-weight: 600;")

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(0, 150, 0, 0)

        self.layout.addWidget(self.profilepicture, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.firstname, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.firstname.data, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.lastname, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.lastname.data, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.classes, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.classes.data, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.email, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.email.data, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def update(self):
        self.firstname.data.setText(globalVars.user.firstName)
        self.lastname.data.setText(globalVars.user.lastName)
        # self.classes.data.setText(globalVars.user.classes)
        self.email.data.setText(globalVars.user.email)
