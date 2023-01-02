from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pwd(password: str):
    return pwd_context.hash(password)


def verify_pwd(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


class logged:
    def __init__(self, username, role, token=None):
        self.__user = username
        self.__role = role
        self.__token = token
        self.__logged = False

    def login(self, user_name, role, token):
        print("User successfully LoggedIn!")
        self.__user = user_name
        self.__role = role
        self.__token = token
        self.__logged = True

    def logout(self, username):
        print(username)
        print(self.__user)
        if username == self.__user:
            print("User successfully LogOut!")
            self.__user = "UNKNOWN"
            self.__role = "UNKNOWN"
            self.__token = None
            self.__logged = False
            return True
        else:
            print("Failed to LogOut!")
            return False

    def is_loggedin(self):
        return self.__logged

    def get_role(self):
        return self.__role


log_stat = logged("UNKNOWN", "UNKNOWN")
