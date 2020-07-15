from ...utils import parser_all_object
from ...models import Currency
from ..bootstrap import service_bus

class CurrencyEmitter():
    def __init__(self):
        self.__start_emitters()

    def emit_currencies(self):
        service_bus.add_queue('currencies', self.__get_all_currencies)

    def emit_currency(self):
        service_bus.add_queue('currency', self.__get_one_currency)

    def __get_all_currencies(self):
        currencies = parser_all_object(Currency.objects.all())
        return currencies

    def __get_one_currency(self):
        currency = self.__get_all_currencies()[0]
        return currency

    def __start_emitters(self):
        self.emit_currencies()
        self.emit_currency()

def start_currency_emit():
    CurrencyEmitter()
    service_bus.send()
