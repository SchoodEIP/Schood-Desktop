from PySide6 import QtWidgets, QtCore

from src.router.Route import Route
from src.utils import globalVars


class StudentDashboard(Route):
    def __init__(self, parent):
        super().__init__()

        color = "color: #000000;"
        self.parent = parent
        self.layout = QtWidgets.QVBoxLayout()
        self.fullName = QtWidgets.QLabel("")
        self.fullName.setStyleSheet(color)
        self.text = QtWidgets.QLabel("Student dashboard")
        self.text.setStyleSheet(color)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.fullName)
        self.layout.addWidget(self.text)

        self.setLayout(self.layout)

    def update(self):
        self.fullName.setText(globalVars.user.firstName + " " + globalVars.user.lastName)
