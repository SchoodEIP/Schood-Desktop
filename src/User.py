from HttpRequest import httpRequest


class User:
    def __init__(self):
        self.token = None
        self._id = None
        self.firstName = None
        self.lastName = None
        self.email = None
        self.role = None
        self.classes = None
        self.picture = None

    def __str__(self):
        return str({
            "id": self._id,
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email,
            "role": self.role,
            "classes": self.classes
        })

    def connect_user(self, data):
        if data["token"] is not None:
            self.token = data["token"]
            httpRequest.add_token(self.token)

            res = httpRequest.get('/user/profile')
            self._id = res.json()["_id"]
            self.firstName = res.json()["firstname"]
            self.lastName = res.json()["lastname"]
            self.email = res.json()["email"]
            self.role = res.json()["role"]
            self.classes = res.json()["classes"]
            self.picture = res.json()["picture"]


user = User()
