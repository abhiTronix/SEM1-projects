from distutils.command import clean
import logging
import re, time
from chat_protobufs.chatroom_pb2_grpc import ChatServicer
from chat_protobufs.chatroom_pb2 import Nothing, connectionConfirm, sendMessageRequest
from chat_protobufs.chatroom_pb2 import disconnectionConfirm, connectionRequest
from chat_protobufs.chatroom_pb2 import (
    CustomImageEndpointRequest,
    CustomImageEndpointResponse,
    ImageData,
)
from Bot import ChatBot as bot

ob = bot.ChatBot.getBot()
ob.response("Hello")

pattern = re.compile("jarvis", re.IGNORECASE)

logging.basicConfig(level=logging.INFO)


def pack_message(_message) -> sendMessageRequest:
    # Pack messages to be sent through gRPC channel
    return sendMessageRequest(
        sentMessage=_message["message"], userName=_message["user_name"]
    )


def pack_image(_image) -> CustomImageEndpointRequest:
    # Pack images to be sent through gRPC channel
    return CustomImageEndpointRequest(
        image=_image["image"], userName=_image["user_name"]
    )


def pack_user(_user) -> connectionRequest:
    # Pack gRPC message to send through channel
    return connectionRequest(userName=_user["user_name"])


class InfoService(ChatServicer):
    """
    Handles message requests
    Posts message back
    """

    def __init__(self):
        self.message_handled = []  # Contains all messages sent through server
        self.image_handled = []  # Contains all images sent through server
        self.connected_users = []  # List of currently connected users
        self.disconnected_users = []  # List of users that disconnected
        self.internal_messages = []

    def messageStream(self, request, context):
        if request.nothing is True:  # True for yielding all messages in server list
            last_message = 0
            last_internal_message = 0
            while True:
                while (
                    len(self.message_handled) > last_message
                    or len(self.internal_messages) > last_internal_message
                ):
                    if len(self.internal_messages) > last_internal_message:
                        _message = self.internal_messages[last_internal_message]
                        last_internal_message += 1
                    else:
                        _message = self.message_handled[last_message]
                        last_message += 1
                    yield pack_message(_message)
        if (
            request.nothing is False
        ):  # False for yielding all connected users in server list
            last_user = 0
            while True:
                while len(self.connected_users) > last_user:
                    _user = self.connected_users[last_user]
                    last_user += 1
                    yield pack_user(_user)

    def imageStream(self, request, context):
        last_image = 0
        while True: # True for yielding all images in server list
            while len(self.image_handled) > last_image:
                _image = self.image_handled[last_image]
                last_image += 1
                yield pack_image(_image)

    def sendImage(self, request, context):
        _image = request.image
        _user_name = request.userName
        self.image_handled.append(
            {  # Store sent message to server list
                "image": _image,
                "user_name": _user_name,
            }
        )
        logging.info(f"[INFO GRPC SERVICE]: Received image from: {_user_name}")
        response = CustomImageEndpointResponse(
            response=f"Received image from: {_user_name}"
        )
        return response

    def sendMessage(self, request, context):
        _message = request.sentMessage
        _user_name = request.userName
        if "jarvis".casefold() in _message.casefold():
            cleaned = pattern.sub("", _message)
            self.message_handled.append(
                {  # Store sent message to server list
                    "message": _message,
                    "user_name": _user_name,
                }
            )
            self.message_handled.append(
                {  # Store sent jarvis bot message to server list
                    "message": ob.response(cleaned),
                    "user_name": "JARVIS",
                }
            )
        elif any(map(_message.__contains__, ["terminate_", "create_"])):
            self.internal_messages.append(
                {  # Store sent internal message to server list
                    "message": _message,
                    "user_name": _user_name,
                }
            )
        else:
            self.message_handled.append(
                {  # Store sent message to server list
                    "message": _message,
                    "user_name": _user_name,
                }
            )

        logging.info(f"[INFO GRPC SERVICE]: Received message: {_message}")
        response = Nothing(
            nothing=True
        )  # Response is required so we just send a dummy Object
        return response

    def connectedUser(self, request, context):
        _new_user = request.userName
        if (
            _new_user is not None and not _new_user in self.connected_users
        ):  # Currently does not check for "username already exist"
            self.connected_users.append({"user_name": _new_user})
            self.disconnected_users = [
                item for item in self.disconnected_users if item != _new_user
            ]
            return connectionConfirm(
                connected=True
            )  # User added to connected users list
        else:
            return connectionConfirm(connnected=False)  # No user was passed

    def onDisconnection(self, request, context):
        incoming = request.userName
        if not incoming in self.disconnected_users:
            self.disconnected_users.append(incoming)
        self.connected_users = [
            item for item in self.connected_users if item["user_name"] != incoming
        ]
        self.internal_messages = [
            item for item in self.internal_messages if item["user_name"] != incoming
        ]

        response = disconnectionConfirm(disconnected=True)
        return response
