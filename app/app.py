from .settings import Database, Server
from .models import Currency
from .utils import paginate

class App():
    def __init__(self):
        init_database = Database()
        init_database.start_connection()

        init_server = Server()
        init_server.connection = init_database
        init_server.start_server()
