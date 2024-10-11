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
        if type(selectedUser) is dict:
            self.selectedUser = selectedUser
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
        return stores.request.post("/adm/register/?mail=true", data=payload)

    def create_users_file(self, file_path):
        try:
            files = { "csv": open(file_path, "rb") }
            print("files: ", files)
            res = stores.request.post("/adm/csvRegisterUser", files=files)
            print("res: ", res.status_code, res.text)
        except Exception as e:
            print(e)

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
        return stores.request.delete("/adm/deleteUser/" + str(_id), data={ "deletePermanently": delete_permanently})

    def fetch_and_get_disabled_users(self):
        return stores.request.get("/user/getDisabled").json()

    def activate_user(self, _id):
        try:
            stores.request.post("/adm/activateUser/" + str(_id))
        except Exception as e:
            print(e)