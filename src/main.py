import sys
import PySide6.QtCore
from PySide6 import QtWidgets, QtCore
from src.routes.shared.LoginPage import LoginPage
from src.router.Router import Router

print('Current PySide version:', PySide6.__version__)
print('Current Qt version:', QtCore.__version__)


# class Window(QtWidgets.QMainWindow):
#     def __init__(self, widget):
#         super().__init__()
#         self.setWindowTitle('Schood')
#         self.setCentralWidget(LoginPage())
#         self.showMaximized()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    router = Router()
    router.show()

    sys.exit(app.exec())
