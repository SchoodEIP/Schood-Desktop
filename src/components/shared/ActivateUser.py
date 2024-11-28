from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QWidget, QGridLayout, QLabel, QVBoxLayout, QSizePolicy, QPushButton

from src.components.Button import Button
from src.router.Route import Route
from src.stores import stores


class ActivateUserWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setStyleSheet("color: #000000;")

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(32, 32, 128, 128)
        self.layout.setSpacing(32)

        self.user = None
        self.text = QLabel("Etes-vous sûr de vouloir réactiver cet utilisateur ?")
        self.button = Button("Réactiver l'utilisateur", callback=self.click)

        self.text.setStyleSheet("""
            QLabel {
                font-size: 30px;
                font-weight: 600;
                color: #292929;
            }
        """)

        self.button.setStyleSheet("""
            QPushButton {
                background-color: #4F23E2;
                color: #FFFFFF;
                border: 2px solid #4F23E2;
                padding: 14px;
                border-radius: 10px;
                font-size: 22px;
            }
        """)

        self.layout.addWidget(self.text, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)

    def click(self):
        stores.users.activate_user(self.user["_id"])
        self.parent.parent.go_to("/manage")

    def update(self):
        self.user = stores.users.get_selected_user()


class ActivateUser(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.setContentsMargins(32, 32, 0, 0)

        self.mainWidget = ActivateUserWidget(self)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.mainWidget)

        self.backButton = Button(text="Retour", parent=self, callback=lambda: self.parent.go_to("/manage"), style_sheet="""
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
        self.mainWidget.update()
