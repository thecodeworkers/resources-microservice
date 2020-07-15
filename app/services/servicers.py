from multiprocessing import Process
import time
from .currency import start_currency_service, start_currency_emit
from .language import start_language_service
from ..servicebus import ServiceBus

def start_all_servicers():
    start_currency_service()
    start_language_service()

def start_all_emiters():
    start_currency_emit()
