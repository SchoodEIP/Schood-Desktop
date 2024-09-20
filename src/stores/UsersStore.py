import json
from json import JSONEncoder

from src.stores import stores


class UsersStore:
    def __init__(self):
        self.users = []
        self.selectedUser = None

    def get_users(self):
        return self.users

    def fetch_users(self):
        self.users = stores.request.get("/user/all").json()

    def get_selected_user(self):
        return self.selectedUser

    def set_selected_user(self, selectedUser):
        if selectedUser is None:
            self.selectedUser = None
            return
        for user in self.users:
            if user["_id"] == selectedUser:
                self.selectedUser = user

    def create_user(self, lastname, firstname, email, role, title, classes):
        payload = {
            "lastname": lastname,
            "firstname": firstname,
            "email": email,
            "role": role,
            "title": title,
            "classes": classes
        }
        if title == "":
            del payload["title"]
        return stores.request.post("/adm/register/?mail=false", data=payload)

    def update_user(self, _id, lastname, firstname, email, role, title, classes):
        payload = {
            "lastname": lastname,
            "firstname": firstname,
            "email": email,
            "role": role,
            "title": title,
            "classes": classes
        }
        if title == "":
            del payload["title"]
        return stores.request.patch("/user/" + str(_id), data=payload)

    def delete_user(self, _id, delete_permanently):
        print(_id)
        return stores.request.delete("/adm/deleteUser/" + str(_id), data={ "deletePermanently": delete_permanently})
