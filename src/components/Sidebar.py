from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication

from src.components.Button import Button
from src.stores import stores
from src.utils.ressources import images_path


class Sidebar(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.expanded = False
        self.setStyleSheet("background-color: #FFD2D5;"
                           "border-top-right-radius: 10px 10px;"
                           "border-bottom-right-radius: 10px 10px;")
        self.layout: Layout = Layout(self)

    def toggle_expanded(self):
        self.expanded = not self.expanded
        self.setFixedWidth(self.layout.expandedWidth if self.expanded else self.layout.collapsedWidth)
        self.layout.mainWidget.setFixedWidth(self.layout.expandedWidth if self.expanded else self.layout.collapsedWidth)
        self.layout.reduce.rotate(self.expanded)

        if self.expanded:
            for button in self.layout.buttons.values():
                button.expand_logo()
            self.layout.logo.expand_logo()
        else:
            for button in self.layout.buttons.values():
                button.shrink_logo()
            self.layout.logo.shrink_logo()


class IconTextWidget(Button):
    def __init__(self, parent, path, text, callback, current=False):
        self.parent = parent
        self.callback = callback
        self.current = current
        self.static = False
        self.disable = False

        self.normal_path = path
        self.active_path = path.replace(".svg", "_white.svg")

        super().__init__(height=30, callback=self.call_callback)

        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinAndMaxSize)

        self.setFixedHeight(30)

        self.image = QSvgWidget(self.active_path if self.current else self.normal_path)
        self.image.setFixedSize(QSize(30, 30))

        self.text = QLabel(text)

        if self.current:
            self.set_as_current()
        else:
            self.set_as_not_current()

        self.layout.addWidget(self.image)
        self.layout.addWidget(self.text)

        self.setLayout(self.layout)

        self.text.hide()

    def set_as_current(self):
        if self.static or self.disable:
            return
        self.current = True
        self.setStyleSheet("""
            QPushButton {
                background-color: #4F23E2;
                border-radius: 10px;
                padding: 0px 0px;
            }
            
            QPushButton:focus {
                outline: none
            }
        """)
        self.image.load(self.active_path)
        self.text.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-weight: 400;
                font-size: 18px;
                padding: 0px;
                background-color: transparent;
            }
        """)

    def set_as_not_current(self):
        if self.static or self.disable:
            return
        self.current = False
        self.setStyleSheet("""
            QPushButton {
                background-color: #FFD2D5;
                border-radius: 10px;
                padding: 0px 0px;
            }
            
            QPushButton:hover {
                background-color: #FFE2E5;
                padding: 0px 0px;
            }
            
            QPushButton:focus {
                outline: none
            }
        """)
        self.image.load(self.normal_path)
        self.text.setStyleSheet("""
            QLabel {
                color: #4F23E2;
                font-weight: 400;
                font-size: 18px;
                padding: 0px;
                background-color: transparent;
            }
        """)

    def set_disable(self, disable):
        self.disable = disable
        if self.disable:
            self.setStyleSheet("""
                            QPushButton {
                                background-color: rgb(120, 120, 120);
                                border-radius: 10px;
                                padding: 0px 0px;
                            }
                            
                            QPushButton:focus {
                                outline: none
                            }
                    """)
            self.image.setStyleSheet("""
                        QSvgWidget {
                            background-color: rgb(120, 120, 120);
                            border-radius: 0px;
                            padding: 0px;
                            margin: 0px;
                        }
                    """)
            self.text.setStyleSheet("""
                        QLabel {
                            background-color: rgb(120, 120, 120);
                            color: #4F23E2;
                            font-weight: 400;
                            font-size: 18px;
                            padding: 0px
                        }
                    """)
        else:
            self.set_as_not_current()

    def call_callback(self):
        if self.disable:
            return
        self.callback()
        self.set_as_current()

    def shrink_logo(self):
        self.text.hide()

    def expand_logo(self):
        self.text.show()

    def rotate(self, bool):
        path = images_path("double-chevron-left.svg") if bool else images_path("double-chevron-right.svg")
        self.image.load(path)
        self.image.setFixedSize(QSize(30, 30))

    def enterEvent(self, event):
        if self.disable:
            return
        QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)
        if not self.current:
            self.text.setStyleSheet("""
                        QLabel {
                            background-color: #FFE2E5;
                            color: #4F23E2;
                            font-weight: 400;
                            font-size: 18px;
                            padding: 0px;
                            margin: 0px
                        }
                    """)
            self.image.setStyleSheet("""
                        QSvgWidget {
                            background-color: #FFE2E5;
                            border-radius: 0px;
                            padding: 0px;
                            margin: 0px;
                        }
                    """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self.disable:
            return
        QApplication.restoreOverrideCursor()
        if not self.current:
            self.text.setStyleSheet("""
                QLabel {
                    background-color: #FFD2D5;
                    color: #4F23E2;
                    font-weight: 400;
                    font-size: 18px;
                    padding: 0px;
                    margin: 0px;
                }
            """)
            self.image.setStyleSheet("""
                        QSvgWidget {
                            background-color: #FFD2D5;
                            border-radius: 0px;
                            padding: 0px;
                            margin: 0px;
                        }
                    """)
        super().leaveEvent(event)


class Schood_Logo(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.picture = QLabel()
        self.imageProfile = QPixmap()

        self.logo_shrinked = images_path("m_logo_schood.png")
        self.logo_expanded = images_path("logo_schood.png")
        self.load_logo(self.logo_shrinked, 30)

        self.layout.addWidget(self.picture)
        self.setLayout(self.layout)

    def load_logo(self, logo_path, size):
        self.imageProfile.load(logo_path)
        self.imageProfile = self.imageProfile.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.picture.setPixmap(self.imageProfile)
        self.picture.setFixedSize(QSize(size, size))

    def shrink_logo(self):
        self.load_logo(self.logo_shrinked, 30)

    def expand_logo(self):
        self.load_logo(self.logo_expanded, 130)
        

class Layout(QVBoxLayout):
    def __init__(self, parent: Sidebar):
        super().__init__()

        self.parent = parent

        self.collapsedWidth = 70
        self.expandedWidth = 250
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinAndMaxSize)

        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.logo = Schood_Logo()

        self.reduce = IconTextWidget(self,
                                     images_path("double-chevron-right.svg"),
                                     "Réduire",
                                     parent.toggle_expanded
                                     )

        self.disconnect = IconTextWidget(self,
                                         images_path("disconnect.svg"),
                                         "Déconnexion",
                                         self.parent.parent.disconnect_user)

        self.reduce.static = True
        self.disconnect.static = True

        self.buttons: dict[str, IconTextWidget] = {
            "/reduce": self.reduce,
            "/disconnect": self.disconnect
        }

        self.mainLayout.addWidget(self.logo)
        self.mainLayout.addStretch(1)


class StudentLayout(Layout):
    def __init__(self, parent: Sidebar):
        super().__init__(parent)

        self.home = IconTextWidget(self,
                                   images_path("home.svg"),
                                   "Accueil",
                                   lambda: self.parent.parent.go_to("/"),
                                   True)

        self.questionnaires = IconTextWidget(self,
                                             images_path("file.svg"),
                                             "Mes questionnaires",
                                             lambda: self.parent.parent.go_to("/test"))
        self.stats = IconTextWidget(self,
                                    images_path("chart.svg"),
                                    "Mes statistiques",
                                    lambda: self.parent.parent.go_to("/test"))
        self.messages = IconTextWidget(self,
                                       images_path("message.svg"),
                                       "Mes messages",
                                       lambda: self.parent.parent.go_to("/test"))
        self.help = IconTextWidget(self,
                                   images_path("info.svg"),
                                   "Mes aides",
                                   lambda: self.parent.parent.go_to("/help"))
        self.profile = IconTextWidget(self,
                                      images_path("account.svg"),
                                      "Mon profil",
                                      lambda: self.parent.parent.go_to("/profile"))
        self.moods = IconTextWidget(self,
                                    images_path("face.svg"),
                                    "Mes ressentis",
                                    lambda: self.parent.parent.go_to("/test"))
        self.alerts = IconTextWidget(self,
                                     images_path("alert.svg"),
                                     "Mes alertes",
                                     lambda: self.parent.parent.go_to("/test"))

        self.current = self.home

        self.messages.set_disable(True)
        self.questionnaires.set_disable(True)
        self.stats.set_disable(True)
        self.moods.set_disable(True)
        self.alerts.set_disable(True)

        self.mainLayout.addWidget(self.home)
        self.mainLayout.addWidget(self.questionnaires)
        self.mainLayout.addWidget(self.stats)
        self.mainLayout.addWidget(self.messages)
        self.mainLayout.addWidget(self.help)
        self.mainLayout.addWidget(self.profile)
        self.mainLayout.addWidget(self.moods)
        self.mainLayout.addWidget(self.alerts)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.reduce)
        self.mainLayout.addWidget(self.disconnect)

        self.mainWidget.setLayout(self.mainLayout)

        self.addWidget(self.mainWidget)

        self.buttons["/"] = self.home
        self.buttons["/questionnaires"] = self.questionnaires
        self.buttons["/statistics"] = self.stats
        self.buttons["/messages"] = self.messages
        self.buttons["/help"] = self.help
        self.buttons["/profile"] = self.profile
        self.buttons["/moods"] = self.moods
        self.buttons["/alerts"] = self.alerts

    def on_child_click(self):
        for button in self.buttons.values():
            button.set_as_not_current()


class TeacherLayout(Layout):
    def __init__(self, parent: Sidebar):
        super().__init__(parent)

        self.home = IconTextWidget(self,
                                   images_path("home.svg"),
                                   "Accueil",
                                   lambda: self.parent.parent.go_to("/"),
                                   True)

        self.questionnaires = IconTextWidget(self,
                                             images_path("file.svg"),
                                             "Mes questionnaires",
                                             lambda: self.parent.parent.go_to("/test"))
        self.stats = IconTextWidget(self,
                                    images_path("chart.svg"),
                                    "Mes statistiques",
                                    lambda: self.parent.parent.go_to("/test"))
        self.messages = IconTextWidget(self,
                                       images_path("message.svg"),
                                       "Mes messages",
                                       lambda: self.parent.parent.go_to("/test"))
        self.help = IconTextWidget(self,
                                   images_path("info.svg"),
                                   "Mes aides",
                                   lambda: self.parent.parent.go_to("/help"))
        self.profile = IconTextWidget(self,
                                      images_path("account.svg"),
                                      "Mon profil",
                                      lambda: self.parent.parent.go_to("/profile"))
        self.alerts = IconTextWidget(self,
                                     images_path("alert.svg"),
                                     "Mes alertes",
                                     lambda: self.parent.parent.go_to("/test"))

        self.current = self.home

        self.messages.set_disable(True)
        self.questionnaires.set_disable(True)
        self.stats.set_disable(True)
        self.alerts.set_disable(True)

        self.mainLayout.addWidget(self.home)
        self.mainLayout.addWidget(self.questionnaires)
        self.mainLayout.addWidget(self.stats)
        self.mainLayout.addWidget(self.messages)
        self.mainLayout.addWidget(self.help)
        self.mainLayout.addWidget(self.profile)
        self.mainLayout.addWidget(self.alerts)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.reduce)
        self.mainLayout.addWidget(self.disconnect)

        self.mainWidget.setLayout(self.mainLayout)

        self.addWidget(self.mainWidget)

        self.buttons["/"] = self.home
        self.buttons["/questionnaires"] = self.questionnaires
        self.buttons["/statistics"] = self.stats
        self.buttons["/messages"] = self.messages
        self.buttons["/help"] = self.help
        self.buttons["/profile"] = self.profile
        self.buttons["/alerts"] = self.alerts

    def on_child_click(self):
        for button in self.buttons.values():
            button.set_as_not_current()


class AdmLayout(Layout):
    def __init__(self, parent: Sidebar):
        super().__init__(parent)

        self.home = IconTextWidget(self,
                                   images_path("home.svg"),
                                   "Accueil",
                                   lambda: self.parent.parent.go_to("/"),
                                   True)

        self.manage = IconTextWidget(self,
                                     images_path("multiple-account.svg"),
                                     "Comptes",
                                     lambda: self.parent.parent.go_to("/manage"))
        self.stats = IconTextWidget(self,
                                    images_path("chart.svg"),
                                    "Statistiques",
                                    lambda: self.parent.parent.go_to("/test"))
        self.messages = IconTextWidget(self,
                                       images_path("message.svg"),
                                       "Mes messages",
                                       lambda: self.parent.parent.go_to("/test"))
        self.help = IconTextWidget(self,
                                   images_path("info.svg"),
                                   "Aides",
                                   lambda: self.parent.parent.go_to("/help"))
        self.profile = IconTextWidget(self,
                                      images_path("account.svg"),
                                      "Mon profil",
                                      lambda: self.parent.parent.go_to("/profile"))
        self.alerts = IconTextWidget(self,
                                     images_path("alert.svg"),
                                     "Alertes",
                                     lambda: self.parent.parent.go_to("/test"))

        self.current = self.home

        self.messages.set_disable(True)
        self.stats.set_disable(True)
        self.alerts.set_disable(True)

        self.mainLayout.addWidget(self.home)
        self.mainLayout.addWidget(self.manage)
        self.mainLayout.addWidget(self.stats)
        self.mainLayout.addWidget(self.messages)
        self.mainLayout.addWidget(self.help)
        self.mainLayout.addWidget(self.profile)
        self.mainLayout.addWidget(self.alerts)
        self.mainLayout.addWidget(self.reduce)
        self.mainLayout.addWidget(self.disconnect)
        self.mainLayout.addStretch(1)

        self.mainWidget.setLayout(self.mainLayout)

        self.addWidget(self.mainWidget)

        self.buttons["/"] = self.home
        self.buttons["/manage"] = self.manage
        self.buttons["/statistics"] = self.stats
        self.buttons["/messages"] = self.messages
        self.buttons["/help"] = self.help
        self.buttons["/profile"] = self.profile
        self.buttons["/alerts"] = self.alerts

    def on_child_click(self):
        for button in self.buttons.values():
            button.set_as_not_current()


class AdminLayout(Layout):
    def __init__(self, parent: Sidebar):
        super().__init__(parent)

        self.home = IconTextWidget(self,
                                   images_path("home.svg"),
                                   "Accueil",
                                   lambda: self.parent.parent.go_to("/"),
                                   True)

        self.manage = IconTextWidget(self,
                                     images_path("multiple-account.svg"),
                                     "Gestion de l'établissement",
                                     lambda: self.parent.parent.go_to("/manage"))
        self.manage.text.setWordWrap(True)

        self.profile = IconTextWidget(self,
                                      images_path("account.svg"),
                                      "Mon profil",
                                      lambda: self.parent.parent.go_to("/profile"))

        self.current = self.home

        self.mainLayout.addWidget(self.home)
        self.mainLayout.addWidget(self.manage)
        self.mainLayout.addWidget(self.profile)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.reduce)
        self.mainLayout.addWidget(self.disconnect)

        self.mainWidget.setLayout(self.mainLayout)

        self.addWidget(self.mainWidget)

        self.buttons["/"] = self.home
        self.buttons["/manage"] = self.manage
        self.buttons["/test"] = self.profile

    def on_child_click(self):
        for button in self.buttons.values():
            button.set_as_not_current()
