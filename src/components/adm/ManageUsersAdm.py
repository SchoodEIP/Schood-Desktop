from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QWidget, QGridLayout, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, \
    QDialog

from src.components.Button import Button
from src.components.adm.UsersListAdm import UserListAdmWidget
from src.router.Route import Route
from src.stores import stores


class ButtonsRow(QWidget):
    activeStyle = """
        QPushButton {
            background-color: #4F23E2;
            color: #FFFFFF;
            border: 2px solid #4F23E2;
            padding: 14px;
            border-radius: 10px;
            font-size: 22px;
        }
    """
    nonActiveStyle = """
        QPushButton {
            background-color: #FFFFFF;
            color: #4F23E2;
            border: 2px solid #4F23E2;
            border-radius: 10px;             
            padding: 14px;
            font-size: 22px;
        }
    """

    def __init__(self, parent, callback):
        super().__init__(parent)
        self.parent = parent
        self.callback = callback

        self.setFixedWidth(750)

        self.studentSwitch = Button("Comptes étudiants")
        self.teacherSwitch = Button("Comptes professeurs")

        self.studentSwitch.setStyleSheet(self.activeStyle)
        self.teacherSwitch.setStyleSheet(self.nonActiveStyle)

        self.studentSwitch.clicked.connect(lambda: self.buttonClicked(0))
        self.teacherSwitch.clicked.connect(lambda: self.buttonClicked(1))

        self.layout = QGridLayout()
        self.layout.addWidget(self.studentSwitch, 0, 0)
        self.layout.addWidget(self.teacherSwitch, 0, 1)

        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)

        self.setLayout(self.layout)

    def buttonClicked(self, mode):
        self.callback(mode)
        if mode == 0:
            self.studentSwitch.setStyleSheet(self.activeStyle)
            self.teacherSwitch.setStyleSheet(self.nonActiveStyle)
        else:
            self.teacherSwitch.setStyleSheet(self.activeStyle)
            self.studentSwitch.setStyleSheet(self.nonActiveStyle)



class ManageUsersAdm(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.setContentsMargins(32, 32, 0, 0)

        self.mainWidget = QWidget()
        self.subLayout = QVBoxLayout()

        self.subWidget = UserListAdmWidget(self)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.subWidget)
        self.scrollArea.setFixedHeight(400)
        self.scrollArea.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title = QLabel("Gestion de comptes")
        self.title.setStyleSheet("""
                    QLabel {
                        font-size: 30px;
                        font-weight: 600;
                        color: #292929;
                    }
                """)

        self.mainLayout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignLeft)

        self.createAccount = Button("Ajouter un compte")
        self.createAccount.clicked.connect(self.displayCreateAccount)
        self.buttonsRow = ButtonsRow(self, self.subWidget.switchLayout)
        self.createAccount.setStyleSheet(self.buttonsRow.activeStyle)
        self.createAccount.setFixedWidth(350)

        self.subLayout.addWidget(self.buttonsRow, alignment=Qt.AlignmentFlag.AlignCenter)
        self.subLayout.addWidget(self.scrollArea)
        self.subLayout.addWidget(self.createAccount, alignment=Qt.AlignmentFlag.AlignCenter)

        self.mainWidget.setLayout(self.subLayout)

        self.mainLayout.addWidget(self.mainWidget)
        self.setLayout(self.mainLayout)

        self.scrollArea.setStyleSheet("""
                    QScrollBar:vertical {
                        border: none;
                        background: #f0f0f0;
                        width: 14px;
                        margin: 0px 0px 0px 0px;
                        border-radius: 7px;
                    }
                    QScrollBar::handle:vertical {
                        background: #FFD2D5;
                        border-radius: 7px;
                    }
                    QScrollBar::add-line:vertical {
                        border: none;
                        background: #f0f0f0;
                        height: 0px;
                        subcontrol-position: bottom;
                        subcontrol-origin: margin;
                    }
                    QScrollBar::sub-line:vertical {
                        border: none;
                        background: #f0f0f0;
                        height: 0px;
                        subcontrol-position: top;
                        subcontrol-origin: margin;
                    }
                    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                        border: none;
                        background: none;
                    }
                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                        background: none;
                    }
                    QScrollBar:horizontal {
                        border: none;
                        background: #f0f0f0;
                        width: 14px;
                        margin: 0px 0px 0px 0px;
                        border-radius: 7px;
                    }
                    QScrollBar::handle:horizontal {
                        background: #FFD2D5;
                        border-radius: 7px;
                    }
                    QScrollBar::add-line:horizontal {
                        border: none;
                        background: #f0f0f0;
                        height: 0px;
                        subcontrol-position: bottom;
                        subcontrol-origin: margin;
                    }
                    QScrollBar::sub-line:horizontal {
                        border: none;
                        background: #f0f0f0;
                        height: 0px;
                        subcontrol-position: top;
                        subcontrol-origin: margin;
                    }
                    QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
                        border: none;
                        background: none;
                    }
                    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                        background: none;
                    }
                """)

    def update(self):
        self.subWidget.update()

    def displayCreateAccount(self):
        self.parent.go_to("/createAccountDialog")