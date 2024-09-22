import os
import sys
import platform
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap

def images_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./src/images" if platform.system() == "Darwin" else "./images")

    return os.path.join(base_path, relative_path)

def load_image(image_filename):
    image_path = images_path(image_filename)
    pixmap = QPixmap(image_path)

    image_label = QLabel()
    image_label.setPixmap(pixmap)
    return image_label