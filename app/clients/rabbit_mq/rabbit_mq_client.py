import pika
from pika.channel import Channel

from app.config import settings


class RabbitMQ:
    def __init__(self, config: str):
        self._settings_rabbit = config
        self._channel: Channel = None
        self.connection = None

    def connect(self):
        parameters = pika.URLParameters(self._settings_rabbit)
        self.connection = pika.BlockingConnection(parameters=parameters)
        self._channel = self.connection.channel()

    def queue_declare(self, queue='upload_in', durable=True):
        self._channel.queue_declare(queue=queue, durable=durable)

    def publish(self, data, routing_key: str):
        if not self.connection:
            return

        self._channel.basic_publish(
            exchange="",
            routing_key=routing_key,
            body=data
        )

    def close(self):
        if not self.connection:
            return

        self._channel.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._channel.close()


def get_rabbit_client() -> RabbitMQ:
    return RabbitMQ(settings.get_connection_rabbit())
