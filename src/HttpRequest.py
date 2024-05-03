import requests


class HttpRequest:
    def __init__(self):
        self.headers = {}
        self.baseUrl = "http://localhost:8080"

    def add_token(self, token):
        self.headers["x-auth-token"] = token

    def get(self, route):
        return requests.get(self.baseUrl + route, headers=self.headers)

    def post(self, route, data):
        return requests.post(self.baseUrl + route, headers=self.headers, data=data)

    def patch(self, route, data):
        return requests.patch(self.baseUrl + route, headers=self.headers, data=data)

    def delete(self, route):
        return requests.delete(self.baseUrl + route, headers=self.headers)


httpRequest = HttpRequest()
