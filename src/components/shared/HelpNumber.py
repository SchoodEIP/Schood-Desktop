from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import QScrollArea, QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QGraphicsDropShadowEffect

from src.utils.ressources import load_image
from src.components.Button import Button
from src.router.Route import Route
from src.stores import stores

class InfoBox(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.component = QWidget(self)
        self.component.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.component.setContentsMargins(32, 32, 32, 32)
        self.componentLayout = QVBoxLayout()

        self.setStyleSheet("""
            QWidget {
                border: solid #ffffff;
                border-radius: 26px;
            }
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor("#9699FF"))
        self.setGraphicsEffect(shadow)

        self.title = QLabel("")
        self.title.setStyleSheet("""
            QLabel {
                font-size: 30px;
                font-weight: 600;
                color: #292929;
                border: none;
            }
        """)

        self.description = QLabel("")
        self.description.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #292929;
                border: none;
            }
        """)

        self.fieldStyleSheet = """
            QLabel { 
                font-size: 18px;
                font-weight: 600;
                color: #292929;
                border: none;
            }
        """

        self.locationIcon = self.resize_icon(load_image("location-dot-solid.svg"), QSize(20, 20))
        self.phoneIcon = self.resize_icon(load_image("phone-solid.svg"), QSize(20, 20))
        self.hourIcon = self.resize_icon(load_image("clock-solid.svg"), QSize(20, 20))

        self.address = QLabel("Aucune information donnée")
        self.phone = QLabel("Aucune information donnée")
        self.hours = QLabel("Aucune information donnée")
        self.address.setStyleSheet(self.fieldStyleSheet)
        self.phone.setStyleSheet(self.fieldStyleSheet)
        self.hours.setStyleSheet(self.fieldStyleSheet)

        addressLayout = QHBoxLayout()
        addressLayout.addWidget(self.locationIcon)
        addressLayout.addWidget(self.address)

        phoneLayout = QHBoxLayout()
        phoneLayout.addWidget(self.phoneIcon)
        phoneLayout.addWidget(self.phone)

        hoursLayout = QHBoxLayout()
        hoursLayout.addWidget(self.hourIcon)
        hoursLayout.addWidget(self.hours)

        self.componentLayout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.componentLayout.addSpacing(48)
        self.componentLayout.addWidget(self.description, alignment=Qt.AlignmentFlag.AlignCenter)
        self.componentLayout.addSpacing(24)
        self.componentLayout.addLayout(addressLayout)
        self.componentLayout.addLayout(phoneLayout)
        self.componentLayout.addLayout(hoursLayout)

        self.component.setLayout(self.componentLayout)

        self.layout.addWidget(self.component)

        self.setLayout(self.layout)

    def resize_icon(self, label, size):
        """ Resize the icon QLabel to the specified size """
        pixmap = label.pixmap()
        if pixmap:
            pixmap = pixmap.scaled(size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            label.setPixmap(pixmap)
        return label
    
    def update(self):
        self.title.setText(self.parent.helpNumber["name"])
        self.description.setText(self.parent.helpNumber["description"])
        if "telephone" in self.parent.helpNumber:
            self.phone.setText(self.parent.helpNumber["telephone"])
        if "email" in self.parent.helpNumber:
            self.phone.setText(self.parent.helpNumber["email"])


class HelpNumbersWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setStyleSheet("color: #292929;")

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(32, 32, 128, 128)
        self.layout.setSpacing(32)

        self.helpNumber = None
        self.infoBox = InfoBox(self)

        self.layout.addWidget(self.infoBox)

        self.setLayout(self.layout)

    def update(self):
        self.helpNumber = stores.helpNumbers.get_selected()
        self.infoBox.update()


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
