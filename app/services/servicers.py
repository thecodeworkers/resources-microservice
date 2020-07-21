from .currency import start_currency_service
from .language import start_language_service

def start_all_servicers():
    start_currency_service()
    start_language_service()

def start_all_emiters():
    pass
