import sys
import os
import time
import pathlib
import queue
import logging
import threading
import grpc
import PySimpleGUI as sg
from PIL import Image, ImageTk
from utils import (
    convert_imagefile_to_Image,
    save_image,
    convert_image_n_save,
    convert_image_to_Image,
    convert_bytes_to_image,
)

sys.path.append("./chat_protobufs")
from chat_protobufs.chatroom_pb2 import (
    sendMessageRequest,
    Nothing,
    connectionRequest,
    onCloseRequest,
    CustomImageEndpointRequest,
    CustomImageEndpointResponse,
    ImageData,
)
from chat_protobufs.chatroom_pb2_grpc import ChatStub


file_types = [
    ("JPEG (*.jpg)", "*.jpg"),
    ("PNG (*.png)", "*.png"),
    ("All files (*.*)", "*.*"),
]

logging.basicConfig(level=logging.INFO)

# give our window a spiffy set of colors
sg.theme("Material1")
font = ("Oswald", 10)
font_bold = ("Oswald", 10, "bold")

# ---- APPLICATION GUI LAYOUT ---------------------------------------------- #
layout = [
    [
        sg.Text(
            "",
            size=(40, 1),
            font=("Oswald", 20, "italic"),
            key="-HEADING-",
            visible=False,
        )
    ],
    [
        sg.Column(
            [
                [sg.Text("Message Board", size=(40, 1), font=font_bold)],
                [
                    sg.Multiline(
                        size=(80, 20),
                        font=font,
                        key="-OUTPUT-",
                    )
                ],
            ]
        ),
        sg.VSeperator(),
        sg.Column(
            [
                [sg.Text("Online Users", size=(15, 1), font=font_bold)],
                [
                    sg.Listbox(
                        ["JARVIS (bot)"],
                        size=(20, 20),
                        font=font,
                        key="-USERS-",
                        enable_events=True,
                    )
                ],
            ]
        ),
    ],
    [sg.Text("", size=(80, 1))],
    [sg.Text("Type your message here:", size=(80, 1), font=font_bold)],
    [
        [
            [
                sg.Multiline(
                    size=(80, 8),
                    enter_submits=False,
                    key="-QUERY-",
                    do_not_clear=True,
                ),
                sg.VSeperator(),
                sg.Column(
                    [
                        [
                            sg.Button(
                                "SEND MESSAGE",
                                button_color=(sg.YELLOWS[0], sg.BLUES[0]),
                                size=(20, 2),
                                bind_return_key=True,
                                font=font_bold,
                            )
                        ],
                        [
                            sg.Button(
                                "SEND IMAGE",
                                button_color=(sg.YELLOWS[0], sg.BLUES[0]),
                                size=(20, 2),
                                bind_return_key=True,
                                font=font_bold,
                            )
                        ],
                        [
                            sg.Button(
                                "EXIT",
                                size=(20, 2),
                                button_color=(sg.YELLOWS[0], sg.GREENS[0]),
                                font=font_bold,
                            )
                        ],
                    ]
                ),
            ],
        ]
    ],
]

window = sg.Window(
    "Chat window",
    layout,
    finalize=True,
    use_default_focus=False,
)


def display_viewer():
    layout = [
        [sg.Image(key="-IMAGE-")],
        [
            sg.Text(
                "Image File",
                font=font_bold,
            ),
            sg.Input(
                size=(25, 1),
                key="_FILEBROWSE_",
                enable_events=True,
                font=font_bold,
            ),
            sg.FileBrowse(file_types=file_types, target="_FILEBROWSE_"),
            sg.Button(
                "SUBMIT",
                button_color=(sg.YELLOWS[0], sg.GREENS[0]),
                font=font_bold,
            ),
        ],
    ]
    window_selector = sg.Window("Image Viewer", layout, element_justification="c")
    filename = ""
    while True:
        event, values = window_selector.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "_FILEBROWSE_":
            filename = values["_FILEBROWSE_"]
            if filename and os.path.exists(filename):
                image = Image.open(filename)
                convert_image_n_save(image, filename)
                window_selector["-IMAGE-"].update(filename=filename)
            else:
                filename = ""
        if event == "SUBMIT":
            break
    window_selector.close()
    return filename if filename and os.path.exists(filename) else ""


class ClientSide:
    """
    Client stub

    Boots PySimpleGUI window
    Makes requests to the server
    """

    def __init__(self, stub: ChatStub, user_name):
        self._user_name = user_name  # username passed (default anonymous)
        self._grpc_response = None  # response from server
        self.stub = stub  # gRPC stub used to make requests to server
        self.users = ["JARVIS (bot)"]  # list to check logged users

    def _get_input(self, message):
        logging.info(f"[CLIENT SIDE]: input message: {message}")
        try:
            message_request = sendMessageRequest(
                sentMessage=message, userName=self._user_name
            )
            self._grpc_response = self.stub.sendMessage(message_request)
        except grpc.RpcError as rpc_error:
            logging.info(f"[CLIENT SIDE]: Error at _get_input() CLIENT -> {rpc_error}")
            window.write_event_value(
                "Message Recieved",
                {
                    "userName": None,
                    "sentMessage": f"\nServer is down\n",
                },
            )  # in thread

    def _sendImage(self, image):
        logging.info(f"[CLIENT SIDE]: input image")
        try:
            image_request = CustomImageEndpointRequest(
                image=image, userName=self._user_name
            )
            self._grpc_response = self.stub.sendImage(image_request)
        except grpc.RpcError as rpc_error:
            logging.info(f"[CLIENT SIDE]: Error at _get_input() CLIENT -> {rpc_error}")
            window.write_event_value(
                "Message Recieved",
                {
                    "userName": None,
                    "sentMessage": f"\nServer is down\n",
                },
            )  # in thread

    def _get_messages(self):
        logging.info("[CLIENT SIDE]: Listening for messages")
        request = Nothing(nothing=True)
        try:
            for _message in self.stub.messageStream(request):
                user = str(_message.userName)
                if "terminate_" in str(_message.sentMessage):
                    if user != self._user_name:
                        self.users = list(filter(lambda a: not (user in a), self.users))
                        window.write_event_value(
                            "Users Updated",
                            self.users,
                        )  # in thread
                elif "create_" in str(_message.sentMessage):
                    if not any(user in u for u in self.users):
                        self.users.append(user)
                        window.write_event_value(
                            "Users Updated",
                            self.users,
                        )  # in thread
                else:
                    window.write_event_value(
                        "Message Recieved",
                        {
                            "userName": _message.userName,
                            "sentMessage": _message.sentMessage,
                        },
                    )  # in thread
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.CANCELLED:
                pass
            else:
                logging.info(
                    f"[CLIENT SIDE]: Error at _get_messages() CLIENT -> {rpc_error}"
                )
                window.write_event_value(
                    "Message Recieved",
                    {
                        "userName": None,
                        "sentMessage": f"\nServer is down\n",
                    },
                )  # in thread

    def _get_images(self):
        logging.info("[CLIENT SIDE]: Listening for images")
        request = Nothing(nothing=True)
        try:
            image_num = 0
            images_displayed = []
            for _image in self.stub.imageStream(request):
                image = convert_bytes_to_image(
                    _image.image.data,
                    _image.image.width,
                    _image.image.height,
                    _image.image.color,
                )
                timestr = time.strftime("%Y%m%d-%H%M%S")
                outfile = os.path.join(
                    os.path.abspath("recv_imgs"), f"{_image.userName}_{timestr}.png"
                )
                window.write_event_value(
                    "Message Recieved",
                    {
                        "userName": _image.userName,
                        "sentMessage": "Sent a Image",
                    },
                )  # in thread
                if _image.userName != self._user_name:
                    if not os.path.basename(outfile) in images_displayed:
                        save_image(image, outfile)
                        images_displayed.append(os.path.basename(outfile))
                        window.write_event_value(
                            "Image Recieved",
                            {"username": _image.userName, "image": outfile},
                        )  # in thread
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.CANCELLED:
                pass
            else:
                logging.info(
                    f"[CLIENT SIDE]: Error at _get_images() CLIENT -> {rpc_error}"
                )
                window.write_event_value(
                    "Message Recieved",
                    {
                        "userName": None,
                        "sentMessage": f"\nServer is down\n",
                    },
                )  # in thread

    def _get_online_users(self):
        logging.info("[CLIENT SIDE]: Listening for connected users")
        request = Nothing(nothing=False)
        try:
            for _user in self.stub.messageStream(request):
                user = (
                    str(_user)
                    .replace("sentMessage", "")
                    .replace(":", "")
                    .replace('"', "")
                    .strip()
                )
                if not user in self.users:
                    self.users.append(user)
                    window.write_event_value(
                        "Users Updated",
                        self.users,
                    )  # in thread
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.UNAVAILLE:
                logging.info("[CLIENT SIDE]: Server is Down")
                pass
            elif rpc_error.code() == grpc.StatusCode.CANCELLED:
                pass
            else:
                logging.info(
                    f"[CLIENT SIDE]: Error at _get_messages() CLIENT -> {rpc_error}"
                )
                window.write_event_value(
                    "Message Recieved",
                    {
                        "userName": None,
                        "sentMessage": f"\nServer is down\n",
                    },
                )  # in thread

    def _create_connection(self):
        try:
            request = connectionRequest(userName=self._user_name)
            response = self.stub.connectedUser(request)
            if response.connected:
                logging.info(f"[CLIENT SIDE]: Created connection {self._user_name}")
        except grpc.RpcError as e:
            logging.info(f"[CLIENT SIDE]: Error at _create_connection() CLIENT -> {e}")
            window.write_event_value(
                "Message Recieved",
                {
                    "userName": None,
                    "sentMessage": f"\nServer is down\n",
                },
            )  # in thread

    def _on_close(self):
        try:
            if len(self.users) > 1:
                message_request = sendMessageRequest(
                    sentMessage=f"terminate_{self._user_name}",
                    userName=f"{self._user_name}",
                )
                self.stub.sendMessage(message_request)
            request = onCloseRequest(userName=self._user_name)
            response = self.stub.onDisconnection(request)
        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.UNAVAILLE:
                logging.info("[CLIENT SIDE]: Closing window. Server Down")
        finally:
            window.close()

    def run(self) -> None:
        """
        Boots client stub
        """
        window["-HEADING-"].update(visible=True)
        window["-HEADING-"].update(value=f"Welcome {self._user_name} to the ChatRoom.")
        self._create_connection()  # Connection Request to server
        logging.info("Initialized No Error")
        self._get_input(f"create_{self._user_name}")
        t1 = threading.Thread(target=self._get_messages)
        t1.setDaemon(True)
        t1.start()  # Thread on message stream from server
        t2 = threading.Thread(target=self._get_images)
        t2.setDaemon(True)
        t2.start()  # Thread on images stream from server
        t3 = threading.Thread(target=self._get_online_users)
        t3.setDaemon(True)
        t3.start()  # Thread on connected user stream from server
        images_displayed = []
        while True:  # The Event Loop
            event, value = window.read(20)
            if event == "Image Recieved":
                if "Image Recieved" in value:
                    data = value["Image Recieved"]
                    sg.popup_no_buttons(
                        f"{data['username']}: Sent a Image",
                        title="Preview Image",
                        keep_on_top=True,
                        image=data["image"],
                    )
            if event == "Message Recieved":
                if "Message Recieved" in value:
                    data = value["Message Recieved"]
                    text = window["-OUTPUT-"]
                    if data["userName"] is None:
                        text.update(text.get() + f"\n{data['sentMessage']}\n")
                    else:
                        text.update(
                            text.get()
                            + f"\n{data['userName']}: {data['sentMessage']}\n"
                        )
            if event == "Users Updated":
                if "Users Updated" in value:
                    data = value["Users Updated"]
                    window["-USERS-"].update(values=data)
            if event in (sg.WIN_CLOSED, "EXIT"):  # quit if exit button or X
                break
            if event == "SEND MESSAGE":
                query = value["-QUERY-"].rstrip()
                window["-QUERY-"].update("")
                self._get_input(query)
            if event == "SEND IMAGE":
                imfile = display_viewer()
                if imfile:
                    # img = resize_image_with_aspect_ratio(img)
                    image = convert_imagefile_to_Image(imfile, rgb=True)
                    self._sendImage(image)
            if event == "-USERS-":
                selection = value[event]
                # if selection:
                #     item = selection[0]
                #     if item.strip() != self._user_name:
                #         index = window["-USERS-"].get_indexes()[0]
                #         answer = sg.popup_yes_no(
                #             f"Do you want to chat privately with {item}",
                #         )
        #                 if answer == "YES":
        #                     print(f'Line {index+1}, "{item}" selected')
        #                     # TODO private chat
        #                 else:
        #                     window["-USERS-"].update(set_to_index=[])
        self._on_close()
