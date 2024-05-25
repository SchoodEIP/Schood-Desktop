from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame


class NotExpandedLayout(QFrame):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.width = 70
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinAndMaxSize)
        self.label = QLabel("Bonjour")
        self.labell = QLabel("Aaaaah")
        self.button = QPushButton("To expand")
        self.button.clicked.connect(parent.toggle_expanded)

        self.addWidget(self.label)
        self.addWidget(self.labell)
        self.addWidget(self.button)


class ExpandedLayout(QVBoxLayout):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.width = 240
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinAndMaxSize)
        self.label = QLabel("Nan")
        self.labell = QLabel("Booh")
        self.button = QPushButton("To reduce")
        self.button.clicked.connect(parent.toggle_expanded)

        self.addWidget(self.label)
        self.addWidget(self.labell)
        self.addWidget(self.button)


class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.expanded = False
        self.notExpandedLayout = NotExpandedLayout(self)
        self.expandedLayout = ExpandedLayout(self)
        self.currentLayout = self.notExpandedLayout
        self.setStyleSheet("background-color: #FFD2D5;"
                           "padding: 8px;"
                           "border-top-right-radius: 20px 20px;")

        # self.notificationImage = QtGui.QPixmap("src/images/bell.svg")
        # self.notification = QLabel()
        # self.notification.setPixmap(self.notificationImage)
        # self.notification.setMaximumWidth(21)
        # self.notification.setMaximumHeight(24)
        # self.notification.setParent(self)
        # self.notification.pos = QtCore.QPoint(1, 1)
        # self.notification.show()

        self.setFixedWidth(self.notExpandedLayout.width)
        self.setFixedHeight(1000)
        self.setLayout(self.notExpandedLayout)

    def toggle_expanded(self):
        print("toggle_expanded")
        self.expanded = not self.expanded
        self.currentLayout = self.expandedLayout if self.expanded else self.notExpandedLayout
        self.setLayout(self.currentLayout)
        self.setFixedWidth(self.currentLayout.width)
        self.setStyleSheet("background-color: #FFD2D5;"
                           "padding: 8px;"
                           "border-top-right-radius: 20px 20px;")
