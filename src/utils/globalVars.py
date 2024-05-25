from src.User import User
from src.components.Sidebar import Sidebar
from src.utils.HttpRequest import HttpRequest

user = None
request = None
sideBar = None

def init():
    global user
    user = User()

    global request
    request = HttpRequest()

    global sideBar
    sideBar = Sidebar()
