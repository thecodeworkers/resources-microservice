from ..channel import service_bus_connection
import time

class WebsocketEmitter():
    def __init__(self):
        self.__start_emitters()

    def emit_binance_websocket(self):
        service_bus_connection.add_queue('coins', self.__data_callback)

    def __data_callback(self, data):
        try:
            print(data)
            return True
        except Exception as error:
            return str(error)

    def __start_emitters(self):
        self.emit_binance_websocket()

def start_binance_emit():
    WebsocketEmitter()
    service_bus_connection.send()


    # connection = pika.BlockingConnection(pika.ConnectionParameters(BUS_URL))
    # channel = connection.channel()
    # channel.queue_declare(queue='coins')

    # def callback(ch, method, properties, body):
    #     print(" [x] Received %r" % body)

    # channel.basic_consume(queue='coins',
    #                     auto_ack=True,
    #                     on_message_callback=callback)

    # print(' [*] Waiting for messages. To exit press CTRL+C')
    # channel.start_consuming()
