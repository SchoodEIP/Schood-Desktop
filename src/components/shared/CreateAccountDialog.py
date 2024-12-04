import json

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QWidget, QGridLayout, QLabel, QVBoxLayout, QSizePolicy, QPushButton, \
    QFileDialog

from src.components.Button import Button
from src.router.Route import Route
from src.stores import stores


class CreateAccountDialogWidget(QWidget):
    def __init__(self, parent, callbackSingle, callbackMultiple):
        super().__init__()

        self.parent = parent

        self.setStyleSheet("color: #000000;")

        self.layout = QGridLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(32, 32, 128, 128)
        self.layout.setSpacing(32)

        self.single = Button("Ajouter un compte")
        self.single.clicked.connect(callbackSingle)
        self.multiple = Button("Ajouter des comptes")
        self.multiple.clicked.connect(callbackMultiple)

        self.error = QLabel("")
        self.error.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #DD0000;
            }
        """)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error.setWordWrap(True)
        self.error.setFixedWidth(380)
        self.scroll.setWidget(self.error)

        self.single.setStyleSheet("""
            QPushButton {
                background-color: #4F23E2;
                color: #FFFFFF;
                border: 2px solid #4F23E2;
                padding: 14px;
                border-radius: 10px;
                font-size: 22px;
            }
        """)

        self.multiple.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0;
                color: #000000;
                border: 2px solid #F0F0F0;
                padding: 14px;
                border-radius: 10px;
                font-size: 22px;
            }
        """)

        self.single.setMaximumWidth(400)
        self.multiple.setMaximumWidth(400)

        self.layout.addWidget(self.single, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.multiple, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.scroll, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 1)
        self.layout.setRowStretch(2, 1)

        self.layout.setColumnStretch(0, 1)

        self.setLayout(self.layout)


class CreateAccountDialog(Route):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.setContentsMargins(32, 32, 0, 0)

        self.mainWidget = CreateAccountDialogWidget(self, lambda: self.parent.go_to("/updateProfileButton"), self.select_file)

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

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "CSV Files (*.csv)")
        if file_path and file_path.endswith(".csv"):
            res = stores.users.create_users_file(file_path)
            if res is not None and res.status_code == 200:
                self.mainWidget.error.setText("")
                self.parent.go_to("/manage")
            else:
                self.mainWidget.error.setText(self.createError(res.text, res.status_code))
        else:
            print("No file selected")

    def createError(self, text, code):
        if code == 500:
            return text
        parsedText = json.loads(text)
        error = ""
        for line in parsedText:
            error += "Ligne " + str(line["rowCSV"]) + ": " + " ".join(line["errors"]) + "\n"
        return error
