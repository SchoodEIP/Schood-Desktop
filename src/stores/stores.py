from src.stores.ClassesStore import ClassesStore
from src.stores.FacilitiesStore import FacilitiesStore
from src.stores.RolesStore import RolesStore
from src.stores.TitlesStore import TitlesStore
from src.stores.UserStore import UserStore
from src.stores.HttpRequestStore import HttpRequestStore
from src.stores.HelpNumberCategoriesStore import HelpNumberCategoriesStore
from src.stores.HelpNumbersStore import HelpNumbersStore
from src.stores.UsersStore import UsersStore

user = None
request = None
helpNumberCategories = None
helpNumbers = None
users = None
roles = None
titles = None
classes = None
facilities = None


def init():
    global user
    user = UserStore()

    global request
    request = HttpRequestStore()

    global helpNumberCategories
    helpNumberCategories = HelpNumberCategoriesStore()

    global helpNumbers
    helpNumbers = HelpNumbersStore()

    global users
    users = UsersStore()

    global roles
    roles = RolesStore()

    global titles
    titles = TitlesStore()

    global classes
    classes = ClassesStore()

    global facilities
    facilities = FacilitiesStore()