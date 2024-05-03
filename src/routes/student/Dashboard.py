from PySide6 import QtWidgets, QtCore

from src.User import user
from src.router.Route import Route


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
        self.fullName.setText(user.firstName + " " + user.lastName)
