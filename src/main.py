import os
import sys
src_dir = os.path.abspath(".")
sys.path.append(src_dir)

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
    app = QtWidgets.QApplication([])
    globalVars.init()

    router = Router()
    router.show()

    sys.exit(app.exec())
