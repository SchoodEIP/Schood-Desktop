from src.stores.UserStore import UserStore
from src.stores.HttpRequestStore import HttpRequestStore
from src.stores.HelpNumberCategoriesStore import HelpNumberCategoriesStore
from src.stores.HelpNumbersStore import HelpNumbersStore

user = None
request = None
helpNumberCategories = None
helpNumbers = None


def init():
    global user
    user = UserStore()

    global request
    request = HttpRequestStore()

    global helpNumberCategories
    helpNumberCategories = HelpNumberCategoriesStore()

    global helpNumbers
    helpNumbers = HelpNumbersStore()
