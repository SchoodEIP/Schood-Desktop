import requests
import os


class HttpRequestStore:
    def __init__(self):
        self.headers = { "Content-Type": "application/json" }
        self.baseUrl = os.getenv('BACKEND_API_URL')

    def add_token(self, token):
        self.headers["x-auth-token"] = token

    def get(self, route):
        return requests.get(self.baseUrl + route, headers=self.headers)

    def post(self, route, data=None, files=None):
        headers = self.headers
        if files:
            del(headers["Content-Type"])
            print("Headers: ", headers)
        return requests.post(self.baseUrl + route, headers=headers, json=data, files=files)

    def patch(self, route, data):
        return requests.patch(self.baseUrl + route, headers=self.headers, json=data)

    def delete(self, route, data):
        return requests.delete(self.baseUrl + route, headers=self.headers, json=data)
