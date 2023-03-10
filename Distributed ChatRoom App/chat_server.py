import threading
import time
import logging
import grpc
import sys
import keyboard
from concurrent.futures import ThreadPoolExecutor

sys.path.append("./chat_protobufs")
from chat_protobufs.chatroom_pb2_grpc import add_ChatServicer_to_server
from chat_protobufs.grpc_servicer import InfoService

logging.basicConfig(level=logging.INFO)
logging.getLogger("[CHAT SERVER]")


class ChatServer:
    def __init__(self, grpc_address):
        self._grpc_service = (
            InfoService()
        )  # gRPC user defined class to implement gRPC services
        self._grpc_address = (
            grpc_address  # gRPC IP address passed from server_config.json
        )
        self._terminate = False

    def _grpc_server(self) -> None:
        """grpc service"""
        grpc_server = grpc.server(ThreadPoolExecutor(max_workers=10))
        add_ChatServicer_to_server(self._grpc_service, grpc_server)
        grpc_server.add_insecure_port(self._grpc_address)
        logging.info(f"[CHAT SERVER]: Starting server on {self._grpc_address}")
        grpc_server.start()
        grpc_server.wait_for_termination()

    # Three functions below log events going through the infoService
    # No event handling nor actions performed

    def _message_handler(self) -> None:
        last_message = 0
        while not self._terminate:
            while len(self._grpc_service.message_handled) > last_message:
                logging.info(
                    f"[CHAT SERVER]: Got message {self._grpc_service.message_handled[last_message]}"
                )
                last_message += 1

    def _image_handler(self) -> None:
        last_image = 0
        while not self._terminate:
            while len(self._grpc_service.image_handled) > last_image:
                logging.info(f"[CHAT SERVER]: Got image")
                last_image += 1

    def _user_handler(self) -> None:
        logging.info(f"[CHAT SERVER]: Listening for connections")
        last_user = 0
        while not self._terminate:
            while len(self._grpc_service.connected_users) > last_user:
                logging.info(
                    f"[CHAT SERVER]: Connected user {self._grpc_service.connected_users[last_user]}"
                )
                last_user += 1

    def _disconnected_user_handler(self) -> None:
        logging.info("[CHAT SERVER]: Listening for disconnections")
        last_user = 0
        while not self._terminate:
            while len(self._grpc_service.disconnected_users) > last_user:
                logging.info(
                    f"[CHAT SERVER]: Disconnected user: {self._grpc_service.disconnected_users[last_user]}"
                )
                last_user += 1

    def close(self):
        self._terminate = True

    # Start threads and run the server

    def run(self):
        # Create new Threads for each task in server side
        grpc_thread = threading.Thread(target=self._grpc_server)
        handler_thread = threading.Thread(target=self._message_handler)
        imghandler_thread = threading.Thread(target=self._image_handler)
        user_thread = threading.Thread(target=self._user_handler)
        disconnection_handler = threading.Thread(target=self._disconnected_user_handler)

        # Start and Join threads
        handler_thread.start()
        grpc_thread.start()
        user_thread.start()
        imghandler_thread.start()
        try:
            disconnection_handler.start()
            grpc_thread.join()
            handler_thread.join()
            user_thread.join()
            imghandler_thread.join()
            disconnection_handler.join()
        except KeyboardInterrupt:
            self.close()
