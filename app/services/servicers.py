from multiprocessing import Process
import time
from .currency import start_currency_service, emit_currencies
from .language import start_language_service
from ..servicebus import ServiceBus

def start_all_servicers():
    start_currency_service()
    start_language_service()

def start_all_emiters():
    return [
        emit_currencies()
    ]

# def emit_one():
#     service_bus = ServiceBus()
#     service_bus.send('currencies', test_func)

#     return service_bus
 
# def emit_two():
#     service_bus = ServiceBus()
#     service_bus.send('currency', test_func2)

#     return service_bus

# def start_all_emiters():
    # threads = [emit_one(), emit_two()]

    # server = emit_currencies()
    # server.run()

    # try:
    #     for thread in threads:
    #         thread.start()
    #         time.sleep(1)
            
    # except KeyboardInterrupt:
    #     print('hola')
    #     for thread in threads:
    #         thread.join()
            
    
# def test_func():
#     return 'enter 1'

# def test_func2():
#     return 'enter 2'
