from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QApplication


class Button(QPushButton):
    def __init__(self, text='', style_sheet=None, width=None, height=None, callback=None, parent=None):
        super().__init__()

        self.parent = parent
        self.setText(text)
        if width is not None:
            self.setFixedWidth(width)
        if height is not None:
            self.setFixedHeight(height)
        if style_sheet is not None:
            self.setStyleSheet(style_sheet)
        if callback is not None:
            self.clicked.connect(callback)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event):
        QApplication.restoreOverrideCursor()
        super().leaveEvent(event)

