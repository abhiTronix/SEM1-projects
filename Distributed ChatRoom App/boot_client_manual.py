import logging
import argparse
import json
import grpc

from client_side import ClientSide
from chat_protobufs.chatroom_pb2_grpc import ChatStub


def run_client(server_address, name):
    if (
        name == "None"
    ):  # If username not provided when booting client default to anonymous
        name = "Anonymous"
    with grpc.insecure_channel(
        server_address
    ) as channel:  # Open a gRPC channel with provided IP
        stub = ChatStub(channel)  # bind the chatStub in the gRPC channel
        client_stub = ClientSide(
            stub, user_name=name
        )  # Pass stub object and userName to tkinter client class
        client_stub.run()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="ChatRoom client(manual)")

    parser.add_argument(
        "--user",
        metavar="name of user connecting",
        type=str,
        required=False,
        help="Name of user on client side",
    )
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
    run_client(
        server_address="{}:{}".format(
            str(args.ip).strip("'"), str(args.port).strip("'")
        ),
        name=str(args.user).strip("'"),
    )
