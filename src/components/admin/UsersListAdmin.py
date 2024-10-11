import base64
from enum import Enum

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPainter, QFontMetrics, QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QScrollArea, QWidget, QGridLayout, QLabel, QVBoxLayout, QPushButton, QHBoxLayout

from src.components.Button import Button
from src.router.Route import Route
from src.stores import stores
from src.stores.stores import users
from src.utils.ressources import images_path


class ButtonLabel(QLabel):
    def paintEvent(self, event):
        painter = QPainter(self)
        metrics = QFontMetrics(self.font())
        elided = metrics.elidedText(self.text(), Qt.TextElideMode.ElideRight, self.width())
        painter.drawText(self.rect(), self.alignment(), elided)


class UserButton(QWidget):
    clicked = Signal()

    def __init__(self, parent, user, callback):
        super().__init__()

        self.parent = parent
        self.user = user
        self.layout = QHBoxLayout()
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                color: #4F23E2;
                border-bottom: 1px solid #9699FF;
                font-size: 20px;
                font-weight: 600;
            }
        """)

        self.mainWidget = QWidget(self)
        self.mainWidget.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 16px;
                font-weight: 600;
                border: none;
            }
        """)
        self.subLayout = QGridLayout()

        self.firstname = ButtonLabel(self.user["firstname"])
        self.lastname = ButtonLabel(self.user["lastname"])
        self.email = ButtonLabel(self.user["email"])
        self.facility = ButtonLabel(self.user["facility"]["name"])
        self.picture = QLabel()
        self.imageProfile = QPixmap()

        if "picture" not in self.user.keys() or len(self.user["picture"].split(",")) != 2:
            self.picture = QSvgWidget(images_path("circle_account.svg"))
            self.picture.setFixedSize(QSize(30, 30))
        else:
            self.imageProfile.loadFromData(base64.b64decode(self.user["picture"].split(",")[1]))
            self.imageProfile = self.imageProfile.scaled(30, 30, Qt.AspectRatioMode.IgnoreAspectRatio,
                                                         Qt.TransformationMode.SmoothTransformation)
            self.picture.setPixmap(self.imageProfile)

        self.picture.setStyleSheet("border: none;")

        self.subLayout.addWidget(self.picture, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.subLayout.addWidget(self.firstname, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.subLayout.addWidget(self.lastname, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.subLayout.addWidget(self.email, 0, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        self.subLayout.addWidget(self.facility, 0, 4, alignment=Qt.AlignmentFlag.AlignCenter)

        for i in range(1, 5):
            self.subLayout.setColumnStretch(i, 1)

        self.mainWidget.setLayout(self.subLayout)
        self.layout.addWidget(self.mainWidget)
        self.setLayout(self.layout)
        self.clicked.connect(lambda: callback(self.user["_id"]))

    def mousePressEvent(self, event):
        self.clicked.emit()


class UserListHeader(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.layout = QHBoxLayout()
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                color: #4F23E2;
                border-bottom: 1px solid #9699FF;
                font-size: 20px;
                font-weight: 600;
            }
        """)

        self.mainWidget = QWidget(self)
        self.mainWidget.setStyleSheet("""
            QLabel {
                color: #4F23E2;
                font-size: 20px;
                font-weight: 600;
                border: none;
            }
        """)
        self.subLayout = QGridLayout()

        self.firstname = ButtonLabel("Prénom")
        self.lastname = ButtonLabel("Nom")
        self.email = ButtonLabel("Email")
        self.facility = ButtonLabel("Etablissement")
        self.picture = QLabel()
        self.picture.setFixedWidth(30)

        self.subLayout.addWidget(self.picture, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.subLayout.addWidget(self.firstname, 0, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.subLayout.addWidget(self.lastname, 0, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.subLayout.addWidget(self.email, 0, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        self.subLayout.addWidget(self.facility, 0, 4, alignment=Qt.AlignmentFlag.AlignCenter)

        for i in range(1, 5):
            self.subLayout.setColumnStretch(i, 1)

        self.mainWidget.setLayout(self.subLayout)
        self.layout.addWidget(self.mainWidget)
        self.setLayout(self.layout)


class UserListAdminWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.users: [str, QWidget] = {}

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(200, 0, 120, 0)

        self.header = UserListHeader(self)

        self.setLayout(self.layout)

    def update(self):
        self.clearUsers()
        stores.users.fetch_users()
        users = stores.users.get_users()

        for user in users:
            widget: UserButton = UserButton(self, user, self.click)
            if user["role"]["levelOfAccess"] == 2:
                self.users[user["_id"]] = widget
        self.fillLayout()

    def clearLayout(self):
        while self.layout.count():
            w = self.layout.takeAt(0)
            if w.widget():
                w.widget().hide()
                self.layout.removeWidget(w.widget())

    def fillLayout(self):
        self.layout.addWidget(self.header)
        self.header.show()
        for widget in self.users.values():
            self.layout.addWidget(widget)
            widget.show()

    def clearUsers(self):
        for widget in self.users.values():
            self.layout.removeWidget(widget)
            widget.deleteLater()
        self.users.clear()

    def click(self, _id):
        stores.users.set_selected_user(_id)
        self.parent.parent.go_to("/updateProfile")