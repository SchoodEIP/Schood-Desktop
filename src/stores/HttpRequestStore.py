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

    def post(self, route, data):
        return requests.post(self.baseUrl + route, headers=self.headers, json=data)

    def patch(self, route, data):
        return requests.patch(self.baseUrl + route, headers=self.headers, json=data)

    def delete(self, route, data):
        return requests.delete(self.baseUrl + route, headers=self.headers, json=data)
