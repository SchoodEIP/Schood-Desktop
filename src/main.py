import sys

import PySide6.QtCore
from PySide6 import QtWidgets, QtCore
from dotenv import load_dotenv

from src.stores import stores

if not load_dotenv():
    print('Dotenv not found.')

from src.router.Router import Router

print('Current PySide version:', PySide6.__version__)
print('Current Qt version:', QtCore.__version__)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    stores.init()

    router = Router()
    router.show()

    sys.exit(app.exec())
