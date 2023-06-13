from django.core import management
from django.core.management.base import BaseCommand
from django.core import serializers
from ine_app.models import Data
import pika, sys, os, threading


QUEUE_DATA = os.getenv('QUEUE_DATA', 'data_queue')
DATA_QUEUE_PRIMARY = os.getenv('DATA_QUEUE_PRIMARY', 'data-queue-1')
DATA_QUEUE_SECONDARY = os.getenv('DATA_QUEUE_SECONDARY', 'data-queue-2')

class Command(BaseCommand):
    help = 'Save a new messasure from one of the queues'

    def consumer(queueName, host):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=5673))
        
        channel = connection.channel()
        
        channel.queue_declare(queue=queueName)

        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)

        channel.basic_consume(queue=queueName, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def handle(self, *args, **options):
        print('TEST')
        thread1 = threading.Thread(target=consumer, args=(QUEUE_DATA, DATA_QUEUE_PRIMARY))
        thread2 = threading.Thread(target=consumer, args=(QUEUE_DATA, DATA_QUEUE_SECONDARY))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

# Register the command with Django's management system
management.commands['save_meassure'] = Command()