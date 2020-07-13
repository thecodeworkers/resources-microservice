from ..services import grpc_server, start_all_servicers, service_bus
from ..constants import SECURE_SERVER, HOST
import time
import sys
import os

class Server():
    def __init__(self):
        self.connection = None
        self.__secure_server = SECURE_SERVER

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
            if self.__secure_server == 'False': 
                grpc_server.add_insecure_port(HOST)
                print("The server was unsecure")

            if self.__secure_server == 'True':
                credentials = self.__set_private_keys()
                grpc_server.add_secure_port(HOST, credentials)
                print("The server was secure")

            grpc_server.start()
            print('Starting server. Listening on port 50051.')
            self.__loop_server()

        except Exception as error:
            print(error)

    def __loop_server(self):
        try:
            service_bus.start_connection()
        except KeyboardInterrupt:
            grpc_server.stop(0)
            service_bus.close_connection()
            self.connection.close_connection()
