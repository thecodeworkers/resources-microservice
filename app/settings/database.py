from mongoengine import connect, disconnect
from ..constants import DATABASE_NAME

class Database():
    def __init__(self):
        self.__database_name = DATABASE_NAME

    def start_connection(self):
        connect(self.__database_name)

    def close_connection(self):
        disconnect(self.__database_name)
