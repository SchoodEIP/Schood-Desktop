from PySide6 import QtWidgets, QtCore, QtGui

from src.router.Route import Route
from src.utils import globalVars


class InformationLabel(QtWidgets.QWidget):
    def __init__(self, infotitle="", info=""):
        super().__init__()

        self.label = QtWidgets.QLabel(infotitle)
        self.label.setStyleSheet(
            "color: #4F23E2;" "font-size: 22px;" "font-weight: 600;"
        )
        self.email = QtWidgets.QLabel(info)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)


class ProfilePicture(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()

        self.logoImage = QtGui.QPixmap("src/images/logo_schood.png")
        self.setPixmap(self.logoImage)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setFixedHeight(300)
        self.setFixedWidth(300)


class ProfilePage(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.profilepicture = ProfilePicture()
        self.firstname = InformationLabel("First Name:", globalVars.user.firstName)
        self.lastname = InformationLabel("Last Name:", globalVars.user.lastName)
        self.classes = InformationLabel("Classe:", globalVars.user.classes)
        self.email = InformationLabel("Email:", globalVars.user.email)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.layout.setSpacing(24)
        
        self.layout.addWidget(self.profilepicture, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.firstname, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.lastname, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.classes, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.email, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        # self.layout.setSpacing(24)
        self.layout.addStretch()
        self.setLayout(self.layout)

        def RetrieveData():
            self.firstname.label.setText(globalVars.user.firstname)
            self.lastname.label.setText(globalVars.user.lastname)
            self.classes.label.setText(globalVars.user.classes)
            self.email.label.setText(globalVars.user.email)