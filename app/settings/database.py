from mongoengine import connect, disconnect
from ..constants import DATABASE_NAME

class Database():
    def start_connection(self):
        connect(DATABASE_NAME)

    def close_connection(self):
        disconnect(DATABASE_NAME)
