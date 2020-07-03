from ..services import grpc_server, start_all_servicers
from ..constants import SECURE_SERVER
import time
import sys
import os

class Server():
    def __init__(self):
        self.connection = None

    def start_server(self):
        start_all_servicers()
        self.__set_correct_server()

    def __set_private_keys(self):
        with open('keys/private.key', 'rb') as f:
            print('Open Private Key')
            private_key = f.read()

        with open('keys/cert.pem', 'rb') as f:
            print('Open Public Key')
            public_key = f.read()

        server_credentials = grpc.ssl_server_credentials(
            ((private_key, public_key))
        )

        return server_credentials

    def __set_correct_server(self):
        try:
            grpc_server.add_insecure_port('[::]:50051')
            if SECURE_SERVER == 'False': print("The server was unsecure")

            if SECURE_SERVER == 'True':
                credentials = self.__set_private_keys()
                grpc_server.add_secure_port('[::]:50051', credentials)
                print("The server was secure")

            grpc_server.start()
            print('Starting server. Listening on port 50051.')
            self.__loop_server()

        except Exception as error:
            print(error)

    def __loop_server(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            grpc_server.stop(0)
            self.connection.close_connection()
