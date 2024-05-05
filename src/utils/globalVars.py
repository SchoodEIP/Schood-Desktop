from src.User import User
from src.utils.HttpRequest import HttpRequest

user = None
request = None


def init():
    global user
    user = User()

    global request
    request = HttpRequest()
