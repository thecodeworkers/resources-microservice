from .currency import start_currency_service
from .language import start_language_service
from .websockets import start_binance_emit, start_getcoins_emit

def start_all_servicers():
    start_currency_service()
    start_language_service()

def start_all_emitters():
    start_binance_emit()
    start_getcoins_emit()
