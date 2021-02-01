from ..channel import service_bus_connection
from ...models import Currencies
from ...utils import parser_all_object
import json

class WebsocketEmitter():
    def __init__(self):
        self.__start_emitters()

    def emit_binance_websocket(self):
        service_bus_connection.add_queue('coins', self.__data_callback)

    def __data_callback(self, data):
        try:
            cryptos = Currencies.objects(pair=data['s'])
            print(data['s'])
            print(cryptos)
            cryptos.update_one(set__price=data['c'])
            print(parser_all_object(cryptos))

            return parser_all_object(cryptos)

        except Exception as error:
            return str(error)

    def __start_emitters(self):
        self.emit_binance_websocket()

def start_binance_emit():
    WebsocketEmitter()
    service_bus_connection.send()
