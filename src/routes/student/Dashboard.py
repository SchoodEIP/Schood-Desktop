from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel


from src.router.Route import Route
from src.stores import stores

class StudentDashboard(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.setContentsMargins(32, 32, 32, 32)

        self.mainWidget = QWidget()
        self.mainWidget.setStyleSheet("color: #292929")

        self.subLayout = QVBoxLayout()
        self.subLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.firstname = QLabel("Bonjour " + stores.user.firstName + ", comment te sens-tu aujourd'hui?")
        self.firstname.setStyleSheet("color: #292929")
        self.text = QLabel("Pas de données à afficher pour le moment.")
        self.text.setStyleSheet("color: #292929")
        
        self.title = QLabel(self.firstname.text())
        self.title.setStyleSheet("font-size: 32px;" "font-weight: 600;" "color: #292929")

        self.subLayout.addWidget(self.title)

        self.mainWidget.setLayout(self.subLayout)
        self.mainLayout.addWidget(self.mainWidget)
        self.mainLayout.addWidget(self.text)

        self.setLayout(self.mainLayout)

    def update(self):
        self.firstname.setText(stores.user.firstName)
