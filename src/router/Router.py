from PySide6 import QtWidgets

from src.routes.shared.LoginPage import LoginPage
from src.routes.student.Dashboard import StudentDashboard


class Router(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.routes = QtWidgets.QStackedWidget()
        self.widgets = []
        self.indexes = {}

        self.init_routes()
        self.routes.setCurrentIndex(0)
        self.setCentralWidget(self.routes)

        self.setWindowTitle('Schood')
        self.showMaximized()

    def init_routes(self):
        self.widgets.append(LoginPage(self))
        self.indexes["/login"] = 0

        self.widgets.append(StudentDashboard(self))
        self.indexes["/"] = 1

        for _, page in enumerate(self.widgets):
            self.routes.addWidget(page)

    def go_to(self, route: str):
        self.widgets[self.indexes[route]].update()
        self.routes.setCurrentIndex(self.indexes[route])
