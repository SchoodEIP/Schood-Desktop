from src.stores import stores


class HelpNumberCategoriesStore:
    def __init__(self):
        self.categories = []

    def get_categories(self):
        return self.categories

    def fetch_categories(self):
        self.categories = stores.request.get("/user/helpNumbersCategories").json()
