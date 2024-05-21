from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QPixmap

from src.router.Route import Route
from src.utils import globalVars


class TeacherDashboard(Route):
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
        self.text = QtWidgets.QLabel("Teacher dashboard")

        self.subLayout.addWidget(self.fullName)
        self.subLayout.addWidget(self.text)

        self.mainWidget.setLayout(self.subLayout)

        self.mainLayout.addWidget(self.mainWidget)

        self.setLayout(self.mainLayout)

    def update(self):
        self.fullName.setText(globalVars.user.firstName + " " + globalVars.user.lastName)

