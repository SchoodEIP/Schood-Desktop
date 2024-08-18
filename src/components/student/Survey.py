from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QWidget, QScrollArea
)

from src.components.Button import Button
from src.stores import stores


class Survey(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set up layout for this widget
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.setContentsMargins(32, 32, 32, 0)  # Add margins around the content
        
        # Create a scrollable area for the content
        self.mainWidget = QWidget(self)
        self.mainWidgetLayout = QVBoxLayout(self.mainWidget)
        self.mainWidgetLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWidgetLayout.setSpacing(30)  # Set spacing between items
        self.mainWidgetLayout.setContentsMargins(0, 0, 0, 0)  # No extra margins in scroll area

        # Set up scroll area
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.mainWidget)

        # Title for the widget
        self.title = QLabel("Mes questionnaires")
        self.title.setStyleSheet("""
            QLabel {
                font-size: 30px;
                font-weight: 600;
                color: #292929;
            }
        """)

        # Details label
        self.detailLabel = QLabel("")
        self.detailLabel.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 400;
                color: #292929;
                margin-top: 20px;
            }
        """)

        # Add widgets to layout
        self.mainLayout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.addWidget(self.scrollArea)
        self.mainLayout.addWidget(self.detailLabel, alignment=Qt.AlignmentFlag.AlignLeft)

        # Set the main layout for this widget
        self.setLayout(self.mainLayout)

    def update(self):
        # Method to refresh or update the widget content
        self.mainWidget.update()