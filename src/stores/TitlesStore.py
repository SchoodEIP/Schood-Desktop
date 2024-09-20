from src.stores import stores


class TitlesStore:
    def __init__(self):
        self.titles = []

    def get_titles(self):
        return self.titles

    def fetch_titles(self):
        self.titles = stores.request.get("/shared/titles").json()
