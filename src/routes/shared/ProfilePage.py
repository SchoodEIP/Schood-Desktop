import base64

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy, QScrollArea
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize, Qt
from PySide6 import QtWidgets, QtCore
from PySide6.QtSvgWidgets import QSvgWidget

from src.components.Button import Button
from src.router.Route import Route
from src.stores import stores
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

        self.setFixedHeight(300)

        self.picture = QLabel()
        self.imageProfile = QPixmap()

        self.picture.setStyleSheet("""
            QWidget {
                color: #4F23E2;
                font-weight: 400;
                font-size: 25px;
                padding: 0px
            }
        """)

        if stores.user.picture is None or len(stores.user.picture.split(",")) != 2:
            self.picture = QSvgWidget(images_path("circle_account.svg"))
            self.picture.setFixedSize(QSize(200, 200))
        else:
            self.imageProfile.loadFromData(base64.b64decode(stores.user.picture.split(",")[1]))
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


class ProfileWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.profilePicture = ProfilePicture()
        self.firstname = InformationLabel("Prénom:", "")
        self.firstname.data.setStyleSheet("color: #292929;" "font-size: 22px;" "font-weight: 400;")
        self.firstname.data.setContentsMargins(0, 0, 0, 20)
        self.lastname = InformationLabel("Nom:", "")
        self.lastname.data.setStyleSheet("color: #292929;" "font-size: 22px;" "font-weight: 400;")
        self.lastname.data.setContentsMargins(0, 0, 0, 20)
        self.classes = InformationLabel("Classe:", "")
        self.classes.data.setStyleSheet("color: #292929;" "font-size: 22px;" "font-weight: 400;")
        self.classes.data.setContentsMargins(0, 0, 0, 20)
        self.email = InformationLabel("Email:", "")
        self.email.data.setStyleSheet("color: #292929;" "font-size: 22px;" "font-weight: 400;")

        self.layout = QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.profilePicture, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
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
        self.firstname.data.setText(stores.user.firstName)
        self.lastname.data.setText(stores.user.lastName)
        self.classes.data.setText(' '.join([obj['name'] for obj in stores.user.classes]))
        self.email.data.setText(stores.user.email)


class ProfilePage(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.setContentsMargins(32, 32, 0, 0)

        self.mainWidget = ProfileWidget(self)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.mainWidget)

        self.title = QLabel("Mon profil")
        self.title.setStyleSheet("""
            QLabel {
                font-size: 32px;
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
