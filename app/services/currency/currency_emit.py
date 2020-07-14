from ...servicebus import ServiceBus
from ...utils import parser_all_object
from ...models import Currency

def emit_currencies():
    service_bus = ServiceBus()
    service_bus.send('currencies', get_all_currencies)

    return service_bus

def get_all_currencies():
    currencies = parser_all_object(Currency.objects.all())
    return currencies
