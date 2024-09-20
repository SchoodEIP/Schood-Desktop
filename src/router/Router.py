from PySide6 import QtWidgets
from PySide6.QtGui import QIcon

from src.components.adm.Sidebar import AdmSidebar
from src.components.admin.Sidebar import AdminSidebar
from src.components.shared.HelpNumber import HelpNumber
from src.components.shared.HelpNumberCategories import HelpNumberCategories
from src.components.shared.HelpNumbers import HelpNumbers
from src.components.student.Sidebar import StudentSidebar
from src.components.teacher.Sidebar import TeacherSidebar
from src.routes.shared.LoginPage import LoginPage
from src.routes.shared.ProfilePage import ProfilePage
from src.routes.student.Dashboard import StudentDashboard
from src.routes.teacher.Dashboard import TeacherDashboard
from src.routes.adm.Dashboard import AdmDashboard
from src.routes.admin.Dashboard import AdminDashboard
from src.components.Sidebar import Sidebar
from src.stores import stores
from src.utils.ressources import images_path
from src.routes.student.Test import StudentTest


class Router(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.mainWidget: QtWidgets.QWidget = QtWidgets.QWidget()
        self.mainLayout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()

        self.sidebar: Sidebar = StudentSidebar(self)
        self.routes: QtWidgets.QStackedWidget = QtWidgets.QStackedWidget()
        self.widgets: list = []
        self.indexes: dict = {}

        self.mainLayout.addWidget(self.sidebar)
        self.mainLayout.addWidget(self.routes)

        self.mainWidget.setLayout(self.mainLayout)
        self.mainWidget.setStyleSheet("margin: 0px;"
                                      "padding: 0px;")

        self.init_routes()
        self.routes.setCurrentIndex(0)
        self.sidebar.hide()

        self.setCentralWidget(self.mainWidget)

        self.setWindowTitle("Schood")
        self.setStyleSheet("background-color: #FFFFFF;"
                           "margin: 0px;"
                           "padding: 0px;")
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowIcon(QIcon(images_path("m_logo_schood.ico")))
        self.showMaximized()

    def init_routes(self):
        self.widgets.append(LoginPage(self))
        self.indexes["/login"] = 0
        self.widgets.append(ProfilePage(self))
        self.indexes["/profile"] = 1

        self.update_routes()

    def update_routes(self):
        for page in self.widgets:
            self.routes.addWidget(page)

    def go_to(self, route: str):
        if route in self.sidebar.layout.buttons.keys():
            self.sidebar.layout.on_child_click()
            self.sidebar.layout.buttons[route].set_as_current()
        self.widgets[self.indexes[route]].update()
        self.routes.setCurrentIndex(self.indexes[route])
        if route != "/login":
            self.sidebar.show()
        else:
            self.sidebar.hide()

    def init_roles_routes(self):
        name = stores.user.role['name']
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
        self.mainLayout.removeWidget(self.sidebar)
        self.sidebar = StudentSidebar(self)
        self.mainLayout.insertWidget(0, self.sidebar)
        self.widgets.append(StudentDashboard(self))
        self.indexes["/"] = 2
        self.widgets.append(HelpNumberCategories(self))
        self.indexes["/help"] = 3
        # self.widgets.append(HelpNumbers(self))
        # self.indexes["/helpNumbers"] = 4
        # self.widgets.append(HelpNumber(self))
        # self.indexes["/helpNumber"] = 5

        self.update_routes()

    def init_teacher_routes(self):
        self.mainLayout.removeWidget(self.sidebar)
        self.sidebar = TeacherSidebar(self)
        self.mainLayout.insertWidget(0, self.sidebar)
        self.widgets.append(TeacherDashboard(self))
        self.indexes["/"] = 2
        self.widgets.append(HelpNumberCategories(self))
        self.indexes["/help"] = 3
        # self.widgets.append(HelpNumbers(self))
        # self.indexes["/helpNumbers"] = 4
        # self.widgets.append(HelpNumber(self))
        # self.indexes["/helpNumber"] = 5

        self.update_routes()

    def init_adm_routes(self):
        self.mainLayout.removeWidget(self.sidebar)
        self.sidebar = AdmSidebar(self)
        self.mainLayout.insertWidget(0, self.sidebar)
        self.widgets.append(AdmDashboard(self))
        self.indexes["/"] = 2
        self.widgets.append(HelpNumberCategories(self))
        self.indexes["/help"] = 3
        # self.widgets.append(HelpNumbers(self))
        # self.indexes["/helpNumbers"] = 4
        # self.widgets.append(HelpNumber(self))
        # self.indexes["/helpNumber"] = 5

        self.update_routes()

    def init_admin_routes(self):
        self.mainLayout.removeWidget(self.sidebar)
        self.sidebar = AdminSidebar(self)
        self.mainLayout.insertWidget(0, self.sidebar)
        self.widgets.append(AdminDashboard(self))
        self.indexes["/"] = 2
        self.widgets.append(HelpNumberCategories(self))
        self.indexes["/help"] = 3
        # self.widgets.append(HelpNumbers(self))
        # self.indexes["/helpNumbers"] = 4
        # self.widgets.append(HelpNumber(self))
        # self.indexes["/helpNumber"] = 5

        self.update_routes()

    def reset_routes(self):
        for widget in self.widgets[2:]:
            self.routes.removeWidget(widget)
        self.widgets = [self.widgets[0], self.widgets[1]]
        self.indexes.clear()
        self.indexes["/login"] = 0
        self.indexes["/profile"] = 1

    def disconnect_user(self):
        stores.user.disconnect_user()
        self.go_to("/login")
        self.reset_routes()
