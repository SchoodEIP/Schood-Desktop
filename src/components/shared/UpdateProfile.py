import threading

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QWidget, QGridLayout, QLabel, QVBoxLayout, QSizePolicy, QPushButton, \
    QHBoxLayout

from src.components.Button import Button
from src.components.shared.ModifyUserInfo import ModifyUserInfoWidget
from src.router.Route import Route
from src.stores import stores


class ModificationButtonsRow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.layout = QGridLayout()

        self.updateProfileButton = QPushButton("Appliquer les changements")
        self.updateProfileButton.setStyleSheet("""
                QPushButton {
                    background-color: #4F23E2;
                    color: #FFFFFF;
                    border: 2px solid #4F23E2;
                    padding: 14px;
                    border-radius: 10px;
                    font-size: 22px;
                }
            """)
        self.updateProfileButton.clicked.connect(self.parent.update_account_callback)

        self.deleteProfileButton = QPushButton("Supprimer le compte")
        self.deleteProfileButton.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF;
                    color: #DD0000;
                    border: 2px solid #DD0000;
                    padding: 14px;
                    border-radius: 10px;
                    font-size: 22px;
                }
            """)
        self.deleteProfileButton.clicked.connect(self.parent.delete_account_callback)


        self.layout.addWidget(self.updateProfileButton, 0, 0)
        self.layout.addWidget(self.deleteProfileButton, 0, 1)

        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 1)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)

        self.layout.setSpacing(40)

        self.setLayout(self.layout)



class UpdateProfile(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.setContentsMargins(32, 32, 0, 0)

        self.mainWidget = QWidget()

        self.subWidget = ModifyUserInfoWidget(self)

        self.subLayout = QVBoxLayout()
        self.subLayout.setSpacing(20)

        self.creationError = QLabel("")
        self.creationError.setStyleSheet("color: #FFFFFF;")

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.mainWidget)

        self.backButton = Button(text="Retour", parent=self, callback=self.back_button_callback, style_sheet="""
            QPushButton {
                background-color: #FFFFFF;
                color: #4F23E2;
                border: none;
                font-size: 20px;
                font-weight: 600;
            }

            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        self.title = QLabel("Modification du profil")
        self.title.setStyleSheet("""
            QLabel {
                font-size: 30px;
                font-weight: 600;
                color: #292929;
            }
        """)

        self.subLayout.addWidget(self.subWidget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.buttonRow = ModificationButtonsRow(self)
        self.subLayout.addWidget(self.buttonRow, alignment=Qt.AlignmentFlag.AlignCenter)
        self.subLayout.addWidget(self.creationError, alignment=Qt.AlignmentFlag.AlignCenter)

        self.mainWidget.setLayout(self.subLayout)

        self.mainLayout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.addWidget(self.backButton, alignment=Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.addWidget(self.scrollArea)

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

    def back_button_callback(self):
        stores.users.set_selected_user(None)
        self.subWidget.reset()
        self.parent.go_to("/manage")

    def update_account_callback(self):
        _id = self.subWidget.user["_id"]
        lastname = self.subWidget.lastname.input.text()
        firstname = self.subWidget.firstname.input.text()
        email = self.subWidget.email.input.text()
        role = self.subWidget.role.selectedOption
        title = self.subWidget.title.selectedOption
        classes = self.subWidget.classes.selectedOptions
        error = False

        if lastname == "":
            error = True
            self.subWidget.lastname.show_error()
        else:
            self.subWidget.lastname.hide_error()
        if firstname == "":
            error = True
            self.subWidget.firstname.show_error()
        else:
            self.subWidget.firstname.hide_error()
        if email == "":
            error = True
            self.subWidget.email.show_error()
        else:
            self.subWidget.email.hide_error()
        if role == "":
            error = True
            self.subWidget.role.show_error()
        else:
            self.subWidget.role.hide_error()
        if len(classes) < 1:
            error = True
            self.subWidget.classes.errorMessage.setText("Veuillez choisir au moins une option.")
            self.subWidget.classes.show_error()
        else:
            self.subWidget.classes.hide_error()

        if error:
            return

        if len(classes) > 1 and self.subWidget.role.input.currentText() == "Étudiant":
            self.subWidget.classes.errorMessage.setText("Un étudiant ne peut avoir qu'une seule classe.")
            self.subWidget.classes.show_error()
            return
        self.subWidget.classes.hide_error()

        res = stores.users.update_user(_id, lastname, firstname, email, role, title, classes)
        if res.status_code == 200:
            self.back_button_callback()
            # self.subWidget.reset()
            # self.creationError.setText("Changements appliqués.")
            # self.creationError.setStyleSheet("color: #00DD00; font-size: 20px;")
            # (threading.
            #  Timer(3,
            #     lambda: self.creationError.setStyleSheet("color: #FFFFFF; font-size: 20px;"))
            #  .start())
        else:
            self.creationError.setText(res.json()["message"])
            self.creationError.setStyleSheet("color: #DD0000; font-size: 20px;")
            self.creationError.show()

    def delete_account_callback(self):
        self.parent.go_to("/deleteAccountDialog")