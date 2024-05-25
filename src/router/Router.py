from PySide6 import QtWidgets

from src.utils import globalVars
from src.routes.shared.LoginPage import LoginPage
from src.routes.shared.ProfilePage import ProfilePage
from src.routes.student.Dashboard import StudentDashboard
from src.routes.teacher.Dashboard import TeacherDashboard
from src.routes.adm.Dashboard import AdmDashboard
from src.routes.admin.Dashboard import AdminDashboard


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
        self.setStyleSheet('background-color: #FFFFFF;')
        self.setContentsMargins(0, 0, 0, 0)
        self.showMaximized()

    def init_routes(self):
        self.widgets.append(LoginPage(self))
        self.indexes["/login"] = 0

        self.update_routes()

    def update_routes(self):
        for _, page in enumerate(self.widgets):
            self.routes.addWidget(page)

    def go_to(self, route: str):
        self.widgets[self.indexes[route]].update()
        self.routes.setCurrentIndex(self.indexes[route])

    def init_roles_routes(self):
        name = globalVars.user.role['name']
        if name is None:
            print('Role name not set')
            return
        match name:
            case "student":
                self.init_student_routes()
                return
            case "teacher":
                self.init_teacher_routes()
                return
            case "administration":
                self.init_adm_routes()
                return
            case "admin":
                self.init_admin_routes()
                return
            case _:
                print('Role not found')

    def init_student_routes(self):
        self.widgets.append(StudentDashboard(self))
        self.indexes["/"] = 1

        self.update_routes()

    def init_teacher_routes(self):
        self.widgets.append(TeacherDashboard(self))
        self.indexes["/"] = 1

        self.update_routes()

    def init_adm_routes(self):
        self.widgets.append(AdmDashboard(self))
        self.indexes["/"] = 1

        self.update_routes()

    def init_admin_routes(self):
        self.widgets.append(AdminDashboard(self))
        self.indexes["/"] = 1

        self.update_routes()

    def init_profile_routes(self):
        self.widgets.append(ProfilePage(self))
        self.indexes["/profile"] = 2

        self.update_routes()