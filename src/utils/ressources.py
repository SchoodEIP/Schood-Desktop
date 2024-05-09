import os
import sys


def images_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./images")

    return os.path.join(base_path, relative_path)
