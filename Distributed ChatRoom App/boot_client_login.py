import PySimpleGUI as sg
from dblite import DBlite
import json
import grpc
import re, sys
import argparse

sys.path.append("./chat_protobufs")
from chat_protobufs.chatroom_pb2_grpc import ChatStub


def run_client(server_address, name):
    if (
        name == "None"
    ):  # If username not provided when booting client default to anonymous
        name = "Anonymous"
    from client_side import ClientSide

    with grpc.insecure_channel(
        server_address
    ) as channel:  # Open a gRPC channel with provided IP
        stub = ChatStub(channel)  # bind the chatStub in the gRPC channel
        client_stub = ClientSide(
            stub, user_name=name
        )  # Pass stub object and userName to tkinter client class
        client_stub.run()


sg.theme("Material2")  # give our window a spiffy set of colors
font = ("Oswald", 10)
font_bold = ("Oswald", 10, "bold")
font_bold_med = ("Oswald", 15, "bold")
font_bold_large = ("Oswald", 25, "bold")

pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
match = re.compile(pattern)

main_layout = [
    [sg.Text("Welcome to ChatRoom", font=font_bold_large)],
    [
        sg.Button("Login", size=(12, 1), key="Login-main", font=font_bold_med),
        sg.Button("Sign-up", size=(12, 1), key="Sign-up-main", font=font_bold_med),
    ],
]

login_layout = [
    [
        sg.Text("Username:", font=font_bold_med),
        sg.Input(key="username", font=font_bold_med),
    ],
    [
        sg.Text("Password:", font=font_bold_med),
        sg.Input(password_char="*", key="password", font=font_bold_med),
    ],
    [sg.Button("Login", bind_return_key=True, key="Login-login", font=font_bold_med)],
]

signup_layout = [
    [
        sg.Text("Username:", font=font_bold_med),
        sg.Input(key="username", font=font_bold_med),
    ],
    [sg.Text("Email:", font=font_bold_med), sg.Input(key="email", font=font_bold_med)],
    [
        sg.Text("Password:", font=font_bold_med),
        sg.Input(password_char="*", key="password", font=font_bold_med),
    ],
    [
        sg.Button(
            "Sign-up",
            bind_return_key=True,
            key="Sign-up-signup",
            font=font_bold_med,
        )
    ],
]

main_window = sg.Window(
    "Main Menu",
    main_layout,
    element_justification="center",
)


class DB_Handler:
    """
    Database Transaction Handler Class
    """

    def __init__(self, Database="users.db"):
        self.db = DBlite(Database)
        self.id = 0

    def create_table(self, table="USER"):
        assert table, "Improper data"
        self.db.add_table(
            table,
            id="INTEGER PRIMARY KEY",
            username="TEXT NOT NULL",
            email="TEXT NOT NULL",
            password="TEXT NOT NULL",
        )
        if self.get_lastentry():
            self.id = self.get_lastentry() + 1

    def insert_entry(self, data, table="USER"):
        """
        Insert into table
        """
        assert isinstance(data, list) and len(data) == 3, "Improper data"
        self.id += 1
        data = [str(self.id)] + data
        self.db.insert(table, *data)

    def get_lastentry(self, table="USER"):
        """
        Get last entry from database
        """
        last_entry = self.db.get_items_query("SELECT MAX(id+0) FROM {}".format(table))[
            0
        ][0]
        if last_entry:
            return int(last_entry)
        return 0

    def login(self, values, table="USER"):
        check = self.db.get_items(
            table,
            "username = '{}' AND password = '{}'".format(
                values["username"], values["password"]
            ),
        )
        if check:
            sg.popup("You are now logged in.")
            return check[0][1]
        else:
            sg.popup_error("Invalid username or password")
            return None

    def signup(self, values, table="USER"):
        check = self.db.get_items(
            table,
            "username = '{}'".format(values["username"]),
        )
        if not check:
            self.id += 1
            data = [str(self.id)] + [
                values["username"],
                values["email"],
                values["password"],
            ]
            self.db.insert(table, *data)
            sg.popup("Username {} has been created".format(values["username"]))
            return values["username"]
        else:
            sg.popup_error(
                "Username {} already exists. Please Login.".format(values["username"])
            )
            return None

    def close(self):
        self.db.close_connection()


# ---- MAIN EVENT LOOP ----------------------------------------------------- #
db = DB_Handler()
db.create_table()
login_window = None
signup_window = None
logged_user = None
login_hide = False
signup_hide = False
parser = argparse.ArgumentParser(description="ChatRoom client(gui)")
parser.add_argument(
    "--ip",
    type=str,
    default="127.0.0.1",
    required=False,
    help="IPv4 address at which server machine is running.",
)
parser.add_argument(
    "--port",
    default="50052",
    type=str,
    required=False,
    help="PORT address at which server machine is running.",
)
args = parser.parse_args()
while True:
    event, values = main_window.read()
    if event in (None, "Cancel"):
        break
    if event == "Login-main":
        if login_window is None:
            login_window = sg.Window(
                "Login", login_layout, element_justification="right", finalize=True
            )
        if login_hide:
            login_window.UnHide()
            login_hide = False

        log_event, log_values = login_window.read()

        if log_event == "Login-login":
            logged_user = db.login(log_values)
            login_window.Hide()
            if not (logged_user is None):
                not (login_window is None) and login_window.close()
                not (signup_window is None) and signup_window.close()
                not (main_window is None) and main_window.close()
                db.close()
                run_client(
                    server_address="{}:{}".format(
                        str(args.ip).strip("'"), str(args.port).strip("'")
                    ),
                    name=logged_user,
                )
            break

    if event == "Sign-up-main":
        if signup_window is None:
            signup_window = sg.Window(
                "Create Account",
                signup_layout,
                element_justification="right",
                finalize=True,
            )
        if signup_hide:
            signup_window.UnHide()
            signup_hide = False
        sign_event, sign_values = signup_window.read()
        if sign_event == "Sign-up-signup":
            if not sign_values["email"] or not re.match(match, sign_values["email"]):
                sg.popup_error("Invalid Email. Try again!")
            elif len(sign_values["username"]) < 3:
                sg.popup_error(
                    "Invalid Username. Username must be atleast 2 characters and unique. Try again!"
                )
            elif "JARVIS" in sign_values["username"].strip():
                sg.popup_error(
                    "Invalid Username. JARVIS username is forbiddened. Try again!"
                )
            elif len(sign_values["password"]) < 6:
                sg.popup_error(
                    "Invalid Password. Password must be atleast 6 characters. Try again!"
                )
            else:
                print("sign")
                logged_user = db.signup(sign_values)
                signup_window.Hide()
                signup_hide = True
                if not (logged_user is None):
                    not (login_window is None) and login_window.close()
                    not (signup_window is None) and signup_window.close()
                    not (main_window is None) and main_window.close()
                    db.close()
                    run_client(
                        server_address="{}:{}".format(
                            str(args.ip).strip("'"), str(args.port).strip("'")
                        ),
                        name=logged_user,
                    )
                break
if logged_user is None:
    not (login_window is None) and login_window.close()
    not (signup_window is None) and signup_window.close()
    not (main_window is None) and main_window.close()
    db.close()
