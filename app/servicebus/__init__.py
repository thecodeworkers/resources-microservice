from pika import BlockingConnection, ConnectionParameters, BasicProperties
import uuid
import json

class ServiceBus():
    def __init__(self):
        self.__connection = BlockingConnection(ConnectionParameters(host='localhost'))
        self.__channel = self.__connection.channel()

    def __start_channel(self, channel_type, on_event):
        exclusive = False
        auto_ack = False
        queue = ''

        if channel_type == 'receive':
            exclusive = True
            auto_ack = True

        if channel_type == 'send':
            self.__channel.basic_qos(prefetch_count=1)
            queue = self.__channel_name

        result = self.__channel.queue_declare(queue=queue, exclusive=exclusive)
        self.callback_queue = result.method.queue

        self.__channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=on_event,
            auto_ack=auto_ack
        )

    def __on_request(self, ch, method, props, body):
        request = self.travel_event()

        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=BasicProperties(
                correlation_id = props.correlation_id, 
                content_type='application/json'
            ),
            body=json.dumps(request)
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body.decode('utf8'))

    def receive(self, channel_name, send=''):
        self.__channel_name = channel_name
        self.__start_channel('receive', self.__on_response)

        self.response = None
        self.corr_id = str(uuid.uuid4())
        
        self.__channel.basic_publish(
            exchange='',
            routing_key=self.__channel_name,
            properties=BasicProperties(
                reply_to=self.callback_queue, 
                correlation_id=self.corr_id,
                content_type='application/json'
            ),
            body=json.dumps(send)
        )
        
        while self.response is None:
            self.__connection.process_data_events()

        return self.response

    def send(self, channel_name, receive=None):
        self.__channel_name = channel_name
        self.travel_event = receive
        self.__start_channel('send', self.__on_request)

    def start_connection(self):
        self.__channel.start_consuming()

    def close_connection(self):
        self.__connection.close()
