from PySide6.QtCore import QSize, Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication

from src.components.Button import Button
from src.components.DarkenWidget import DarkenWidget
from src.utils.ressources import images_path


class Sidebar(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.expanded = False
        self.layout = Layout(self)
        self.setStyleSheet("background-color: #FFD2D5;"
                           "padding: 8px;"
                           "border-top-right-radius: 20px 20px;"
                           "border-bottom-right-radius: 20px 20px;")

        # self.notificationImage = QtGui.QPixmap("src/images/bell.svg")
        # self.notification = QLabel()
        # self.notification.setPixmap(self.notificationImage)
        # self.notification.setMaximumWidth(21)
        # self.notification.setMaximumHeight(24)
        # self.notification.setParent(self)
        # self.notification.pos = QtCore.QPoint(1, 1)
        # self.notification.show()

        self.setFixedWidth(self.layout.collapsedWidth)
        self.setLayout(self.layout)

    def toggle_expanded(self):
        self.expanded = not self.expanded
        self.setFixedWidth(self.layout.expandedWidth if self.expanded else self.layout.collapsedWidth)
        self.layout.mainWidget.setFixedWidth(self.layout.expandedWidth if self.expanded else self.layout.collapsedWidth)
        self.layout.reduce.rotate(self.expanded)
        if self.expanded:
            for button in self.layout.buttons.values():
                button.show_text()
        else:
            for button in self.layout.buttons.values():
                button.hide_text()


class IconTextWidget(Button):
    def __init__(self, parent, path, text, callback, current=False):
        self.parent = parent
        self.callback = callback
        super().__init__(height=30, callback=self.call_callback)

        self.current = current
        self.static = False
        self.disable = False

        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinAndMaxSize)

        self.setFixedHeight(30)

        self.image = QSvgWidget(path)
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

    def set_disable(self, disable):
        self.disable = disable
        if self.disable:
            self.setStyleSheet("""
                            QPushButton {
                                background-color: rgb(120, 120, 120);
                                border-radius: 20px;
                                padding: 0px 0px;
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
                            font-weight: 600;
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

    def hide_text(self):
        self.text.hide()

    def show_text(self):
        self.text.show()

    def set_as_current(self):
        if self.static or self.disable:
            return
        self.current = True
        self.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF;
                    border-radius: 20px;
                    padding: 0px 0px;
                }
        """)
        self.image.setStyleSheet("""
            QSvgWidget {
                background-color: #FFFFFF;
                border-radius: 0px;
                padding: 0px;
                margin: 0px;
            }
        """)
        self.text.setStyleSheet("""
            QLabel {
                background-color: #FFFFFF;
                color: #4F23E2;
                font-weight: 600;
                font-size: 18px;
                padding: 0px
            }
        """)

    def set_as_not_current(self):
        if self.static or self.disable:
            return
        self.current = False

        self.setStyleSheet("""
                QPushButton {
                    background-color: #FFD2D5;
                    border-radius: 20px;
                    padding: 0px 0px;
                }
                
                QPushButton:hover {
                    background-color: #FFE2E5;
                    padding: 0px 0px;
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
        self.text.setStyleSheet("""
                QLabel {
                    background-color: #FFD2D5;
                    color: #4F23E2;
                    font-weight: 600;
                    font-size: 18px;
                    padding: 0px
                }
            """)

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
                            font-weight: 600;
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
                    font-weight: 600;
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


class Layout(QVBoxLayout):
    def __init__(self, parent: Sidebar):
        super().__init__()

        self.parent = parent

        self.expandedWidth = 250
        self.collapsedWidth = 70
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinAndMaxSize)

        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.addStretch(1)

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
                                   lambda: self.parent.parent.go_to("/test"))
        self.profile = IconTextWidget(self,
                                      images_path("account.svg"),
                                      "Mon profil",
                                      lambda: self.parent.parent.go_to("/test"))
        self.moods = IconTextWidget(self,
                                    images_path("face.svg"),
                                    "Mes ressentis",
                                    lambda: self.parent.parent.go_to("/test"))
        self.alerts = IconTextWidget(self,
                                     images_path("alert.svg"),
                                     "Mes alertes",
                                     lambda: self.parent.parent.go_to("/test"))
        self.reduce = IconTextWidget(self,
                                     images_path("double-chevron-right.svg"),
                                     "Réduire",
                                     parent.toggle_expanded
                                     )
        self.disconnect = IconTextWidget(self,
                                         images_path("disconnect.svg"),
                                        "Déconnexion",
                                        self.parent.parent.disconnect_user)

        self.current = self.home

        self.reduce.static = True
        self.disconnect.static = True
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
        self.mainLayout.addWidget(self.reduce)
        self.mainLayout.addWidget(self.disconnect)
        self.mainLayout.addStretch(1)

        self.mainWidget.setLayout(self.mainLayout)

        self.addWidget(self.mainWidget)

        self.buttons: dict[str, IconTextWidget] = {
            "/": self.home,
            "/test": self.questionnaires,
            "/statistics": self.stats,
            "/messages": self.messages,
            "/help": self.help,
            "/profile": self.profile,
            "/moods": self.moods,
            "/alerts": self.alerts,
            "/reduce": self.reduce,
            "/disconnect": self.disconnect
        }

    def on_child_click(self):
        for button in self.buttons.values():
            button.set_as_not_current()
