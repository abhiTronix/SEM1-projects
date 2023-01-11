import logging
import argparse
import json

from chat_server import ChatServer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ChatRoom server")
    parser.add_argument(
        "--port",
        default="50052",
        type=str,
        required=False,
        help="PORT address at which server machine is running.",
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    server = ChatServer("[::]:{}".format(str(args.port).strip("'")))
    server.run()
