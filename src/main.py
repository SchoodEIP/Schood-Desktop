import os
import sys

import PySide6.QtCore
from PySide6 import QtWidgets, QtCore
from dotenv import load_dotenv

if not load_dotenv():
    print('Dotenv not found.')

from src.router.Router import Router
from src.utils import globalVars

print('Current PySide version:', PySide6.__version__)
print('Current Qt version:', QtCore.__version__)

if __name__ == "__main__":
    globalVars.init()
    app = QtWidgets.QApplication([])

    router = Router()
    router.show()

    sys.exit(app.exec())
