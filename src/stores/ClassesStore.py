from src.stores import stores


class ClassesStore:
    def __init__(self):
        self.classes = []

    def get_classes(self):
        return self.classes

    def fetch_classes(self):
        self.classes = stores.request.get("/shared/classes").json()
