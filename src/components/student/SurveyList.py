from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QScrollArea, QHBoxLayout, QSizePolicy, QGraphicsDropShadowEffect

from src.components.Button import Button
from src.stores import stores
from src.components.student.Survey import Survey


class SurveyListWidget(QWidget):
    def __init__(self, parent, start_date, end_date, surveyList):
        super().__init__(parent)
        self.parent = parent

        # Create the white container
        self.container = QWidget(self)
        self.container.setStyleSheet("background-color: #ffffff; border-radius: 26px;")

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 5)
        shadow.setColor(QColor("#9699FF"))
        self.container.setGraphicsEffect(shadow)

        # Layout for the container
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setSpacing(15)

        # Date label
        dateRange = f"Du {start_date.toString('dd MMM yyyy')} au {end_date.toString('dd MMM yyyy')}"
        dateLabel = QLabel(dateRange)
        dateLabel.setStyleSheet("color: #292929; font-size: 22px; font-weight: 600;")
        self.layout.addWidget(dateLabel)

        # Survey items
        for survey in surveyList:
            surveyLayout = QHBoxLayout()
            surveyLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

            surveyLabel = QLabel(survey)
            surveyLabel.setStyleSheet("color: #292929; font-size: 22px; font-weight: 400;")

            percentageLabel = QLabel("75%")
            percentageLabel.setStyleSheet("color: #292929; font-size: 22px; font-weight: 600;")

            arrowLabel = QLabel("→")
            arrowLabel.setStyleSheet("color: #4F23E2; font-size: 22px; font-weight: 600;")

            surveyLayout.addWidget(surveyLabel)
            surveyLayout.addStretch()
            surveyLayout.addWidget(percentageLabel)
            surveyLayout.addWidget(arrowLabel)

            # Clickable container
            surveyContainer = QWidget()
            surveyContainer.setLayout(surveyLayout)
            surveyContainer.setStyleSheet("QWidget:hover { background-color: #f0f0f0; }")
            surveyContainer.mousePressEvent = lambda e: self.redirect_to_survey()

            self.layout.addWidget(surveyContainer)
            self.layout.addSpacing(10)

        self.container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Set main layout
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.container)
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(mainLayout)

    def redirect_to_survey(self):
        # Hide the SurveyList widget and show the Survey widget
        self.parent.hide()
        surveyWidget = Survey(self.parent.parent())
        self.parent.parent().layout().addWidget(surveyWidget)


class SurveyList(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.setContentsMargins(32, 32, 0, 0)

        # Scroll area containing survey list widgets
        self.mainWidget = QWidget(self)
        self.mainWidgetLayout = QVBoxLayout(self.mainWidget)
        self.mainWidgetLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainWidgetLayout.setSpacing(30)
        self.mainWidgetLayout.setContentsMargins(400, 0, 400, 0)

        # Example data (date range with multiple surveys)
        surveyList_data = [
            (QDate(2024, 8, 10), QDate(2024, 8, 17), ["Survey 1", "Survey 1.1"]),
            (QDate(2024, 9, 1), QDate(2024, 9, 5), ["Survey 2", "Survey 2.1"]),
            (QDate(2024, 10, 20), QDate(2024, 10, 25), ["Survey 3", "Survey 3.1", "Survey 3.2"]),
        ]

        for start_date, end_date, surveyList in surveyList_data:
            surveylistWidget = SurveyListWidget(self, start_date, end_date, surveyList)
            self.mainWidgetLayout.addWidget(surveylistWidget)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.mainWidget)

        self.title = QLabel("Mes questionnaires")
        self.title.setStyleSheet("""
            QLabel {
                font-size: 30px;
                font-weight: 600;
                color: #292929;
            }
        """)

        self.mainLayout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.addWidget(self.scrollArea)

        self.setLayout(self.mainLayout)

    def update(self):
        self.mainWidget.update()