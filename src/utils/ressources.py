import os
import sys
import platform

def images_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./src/images" if platform.system() == "Darwin" else "./images")

    return os.path.join(base_path, relative_path)
