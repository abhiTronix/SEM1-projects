from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pwd(password: str):
    return pwd_context.hash(password)


def verify_pwd(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


class logged:
    def __init__(self):
        self.__users = {}
        self.__roles = {}
        self.__logged = False

    def login(self, username, role, token):
        print("User successfully LoggedIn!")
        self.__users[username] = token
        self.__roles[username] = role
        self.__logged = True

    def logout(self, username):
        print(username)
        if username in self.__users:
            print("User successfully LogOut!")
            self.__users.pop(username, None)
            self.__roles.pop(username, None)
            self.__logged = False
            return True
        else:
            print("Failed to LogOut!")
            return False

    def is_logged_auth(self, user):
        return True if user in self.__users else False

    def get_logged_users(self):
        return self.__users

    def get_role_auth(self, username):
        return True if username in self.__roles else False


log_stat = logged()
