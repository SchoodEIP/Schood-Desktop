from PySide6 import QtWidgets, QtCore

from src.router.Route import Route
from src.utils import globalVars


class StudentDashboard(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.layout = QtWidgets.QVBoxLayout()
        self.fullName = QtWidgets.QLabel("")
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.fullName)

        self.setLayout(self.layout)

    def update(self):
        self.fullName.setText(globalVars.user.firstName + " " + globalVars.user.lastName)
