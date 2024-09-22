from src.stores import stores


class RolesStore:
    def __init__(self):
        self.roles = []

    def get_roles(self):
        return self.roles

    def fetch_roles(self):
        self.roles = stores.request.get("/shared/roles").json()["roles"]
