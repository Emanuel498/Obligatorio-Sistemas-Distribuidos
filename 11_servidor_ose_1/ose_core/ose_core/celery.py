import os
from celery import Celery
from kombu import Connection
from kombu.mixins import ConsumerMixin

# Set the default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ose_core.settings')

# Create the Celery app
app = Celery('ose_core')

# Configure Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

class QueueConsumer(ConsumerMixin):
    def __init__(self, connection, queue, callback):
        self.connection = connection
        self.queue = queue
        self.callback = callback

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queue, callbacks=[self.process_message])]

    def process_message(self, body, message):
        self.callback(body)
        message.ack()

    def on_connection_error(self, exc, interval):
        raise exc

    def run(self, **kwargs):
        with self.connection as connection:
            connection.register_with_event_loop(self)
            connection.drain_events()

@app.task
def process_queue_message(body):
    print(body)

@app.task
def consume_queue():
    with Connection('amqp://guest:guest@localhost:5672//') as connection:
        queue = connection.SimpleQueue('test_queue')
        consumer = QueueConsumer(connection, queue, process_queue_message)
        consumer.run()