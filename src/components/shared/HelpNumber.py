from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy

from src.components.Button import Button
from src.router.Route import Route
from src.stores import stores


class InfoBox(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.component = QWidget(self)
        self.component.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.component.setContentsMargins(32, 32, 32, 32)
        self.componentLayout = QVBoxLayout()

        self.setStyleSheet("""
            QWidget {
                border: 4px solid #4F23E2;
                border-radius: 24px;
            }
        """)

        self.title = QLabel("")
        self.title.setStyleSheet("""
            QLabel {
                font-size: 40px;
                font-weight: 600;
                border: none;
            }
        """)

        self.fieldStyleSheet = """
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #4F23E2;
                border: none;
            }
        """
        self.labelStyleSheet = """
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: #000000;
                border: none;
            }
        """

        self.address = QLabel("-")
        self.addressLabel = QLabel("Adresse")
        self.phone = QLabel("-")
        self.phoneLabel = QLabel("Numéro de téléphone")
        self.hours = QLabel("-")
        self.hoursLabel = QLabel("Horaires")
        self.infos = QLabel("-")
        self.infosLabel = QLabel("informations")
        self.address.setStyleSheet(self.fieldStyleSheet)
        self.phone.setStyleSheet(self.fieldStyleSheet)
        self.hours.setStyleSheet(self.fieldStyleSheet)
        self.infos.setStyleSheet(self.fieldStyleSheet)
        self.addressLabel.setStyleSheet(self.labelStyleSheet)
        self.hoursLabel.setStyleSheet(self.labelStyleSheet)
        self.infosLabel.setStyleSheet(self.labelStyleSheet)
        self.phoneLabel.setStyleSheet(self.labelStyleSheet)

        self.componentLayout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.componentLayout.addSpacing(48)
        self.componentLayout.addWidget(self.phoneLabel)
        self.componentLayout.addWidget(self.phone)
        self.componentLayout.addSpacing(24)
        self.componentLayout.addWidget(self.hoursLabel)
        self.componentLayout.addWidget(self.hours)
        self.componentLayout.addSpacing(24)
        self.componentLayout.addWidget(self.infosLabel)
        self.componentLayout.addWidget(self.infos)
        self.componentLayout.addSpacing(24)
        self.componentLayout.addWidget(self.addressLabel)
        self.componentLayout.addWidget(self.address)

        self.component.setLayout(self.componentLayout)

        self.layout.addWidget(self.component)

        self.setLayout(self.layout)

    def update(self):
        self.title.setText(self.parent.helpNumber["name"])
        if "telephone" in self.parent.helpNumber:
            self.phone.setText(self.parent.helpNumber["telephone"])
        if "email" in self.parent.helpNumber:
            self.phone.setText(self.parent.helpNumber["email"])


class DescriptionBox(QLabel):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.setStyleSheet("""
            QLabel {
                border: 4px solid #4F23E2;
                border-radius: 24px;
                font-size: 16px;
                font-weight: 600;
            }
        """)
        self.setWordWrap(True)

    def update(self):
        self.setText(self.parent.helpNumber["description"] if "description" in self.parent.helpNumber else "-")


class HelpNumbersWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setStyleSheet("color: #000000;")

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(32, 32, 128, 128)
        self.layout.setSpacing(32)

        self.helpNumber = None
        self.infoBox = InfoBox(self)
        self.descriptionBox = DescriptionBox(self)

        self.layout.addWidget(self.infoBox, 0, 0)
        self.layout.addWidget(self.descriptionBox, 0, 1)

        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)

        self.layout.setRowStretch(0, 1)

        self.setLayout(self.layout)

    def update(self):
        self.helpNumber = stores.helpNumbers.get_selected()
        self.infoBox.update()
        self.descriptionBox.update()
        print(self.helpNumber)


class HelpNumber(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.setContentsMargins(32, 32, 0, 0)

        self.mainWidget = HelpNumbersWidget(self)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.mainWidget)

        self.title = QLabel("Mes numéros d'aide")
        self.title.setStyleSheet("""
            QLabel {
                font-size: 30px;
                font-weight: 600;
                color: #292929;
            }
        """)

        self.backButton = Button(text="Retour", parent=self, callback=lambda: self.parent.go_to("/helpNumbers"), style_sheet="""
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

        self.mainLayout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.addSpacing(32)
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
