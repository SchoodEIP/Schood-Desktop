from src.stores import stores


class HelpNumbersStore:
    def __init__(self):
        self.numbers = []
        self.category = ""
        self.selected = None

    def set_category(self, category):
        self.category = category

    def set_selected(self, selected):
        self.selected = selected

    def get_category(self):
        return self.category

    def get_selected(self):
        return self.selected

    def get_numbers(self):
        return self.numbers

    def fetch_numbers(self, _id=None):
        if self.category == "":
            return []
        self.numbers = stores.request.get("/user/helpNumbers/" + (self.category if _id is None else _id)).json()
