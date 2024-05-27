from PySide6 import QtWidgets, QtCore

from src.router.Route import Route
from src.stores import stores


class AdminDashboard(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.layout = QtWidgets.QVBoxLayout()
        self.fullName = QtWidgets.QLabel("")
        self.text = QtWidgets.QLabel("Admin dashboard")
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.fullName)
        self.layout.addWidget(self.text)

        self.setLayout(self.layout)

    def update(self):
        self.fullName.setText(stores.user.firstName + " " + stores.user.lastName)
