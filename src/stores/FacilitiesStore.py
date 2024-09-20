from src.stores import stores


class FacilitiesStore:
    def __init__(self):
        self.facilities = []

    def get_facilities(self):
        return self.facilities

    def fetch_facilities(self):
        return []
        # TODO: compléter la route une fois qu'elle existera
        self.facilities = stores.request.get("ROUTE RECUPERATION ETABLISSEMENTS").json()
