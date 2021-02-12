from ..channel import service_bus_connection
from ...models import Currencies
from ...utils import parser_all_object
import json

class GetCoinsEmitter():
    def __init__(self):
        self.__start_emitters()

    def emit_get_coins(self):
        service_bus_connection.add_queue('get_coins', self.__data_callback)

    def __data_callback(self, data):
        try:
            cryptos = Currencies.objects.filter(type='CRYPTO').filter(symbol__ne='USDT')

            return parser_all_object(cryptos)

        except Exception as error:
            return str(error)

    def __start_emitters(self):
        self.emit_get_coins()

def start_getcoins_emit():
    GetCoinsEmitter()
    service_bus_connection.send()
