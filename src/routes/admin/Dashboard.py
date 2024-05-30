from PySide6 import QtWidgets, QtCore

from src.router.Route import Route
from src.stores import stores


class AdminDashboard(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.setContentsMargins(32, 32, 0, 0)

        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.setStyleSheet("color: #000000")

        self.subLayout = QtWidgets.QVBoxLayout()
        self.subLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.firstname = QtWidgets.QLabel("Bonjour " + stores.user.firstName)
        self.firstname.setStyleSheet("color: #000000")
        self.text = QtWidgets.QLabel("Pas de données à afficher pour le moment.")
        self.text.setStyleSheet("color: #000000")
        
        self.title = QtWidgets.QLabel(self.firstname.text())
        self.title.setStyleSheet("font-size: 32px;" "font-weight: 600;" "color: #000000")

        self.subLayout.addWidget(self.title)

        self.mainWidget.setLayout(self.subLayout)
        self.mainLayout.addWidget(self.mainWidget)
        self.mainLayout.addWidget(self.text)

        self.setLayout(self.mainLayout)

    def update(self):
        self.firstname.setText(stores.user.firstName)