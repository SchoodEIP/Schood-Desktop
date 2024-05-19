import base64

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from src.router.Route import Route
from src.utils import globalVars


class StudentDashboard(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.setStyleSheet("color: #000000")

        self.subLayout = QtWidgets.QVBoxLayout()
        self.subLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.fullName = QtWidgets.QLabel("")
        self.text = QtWidgets.QLabel("Student dashboard")

        self.profile = QtWidgets.QLabel()
        self.imageProfile = QPixmap()

        self.subLayout.addWidget(self.fullName)
        self.subLayout.addWidget(self.text)
        self.subLayout.addWidget(self.profile)

        self.mainWidget.setLayout(self.subLayout)

        self.mainLayout.addWidget(self.mainWidget)

        self.setLayout(self.mainLayout)

    def update(self):
        self.fullName.setText(globalVars.user.firstName + " " + globalVars.user.lastName)
        self.imageProfile.loadFromData(base64.b64decode(globalVars.user.picture.split(",")[1]))
        self.imageProfile = self.imageProfile.scaled(90, 90, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.profile.setPixmap(self.imageProfile)
