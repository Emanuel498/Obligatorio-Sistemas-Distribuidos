from django.core import management
from django.core.management.base import BaseCommand
from django.core import serializers
from ose_app.models import Meassure
import pika, sys, os, threading


QUEUE_NAME = os.getenv('QUEUE_NAME', 'test_queue')
ALERTS_QUEUE_PRIMARY = os.getenv('ALERTS_QUEUE_PRIMARY', 'alerts-queue-1')
ALERTS_QUEUE_SECONDARY = os.getenv('ALERTS_QUEUE_SECONDARY', 'alerts-queue-2')

class Command(BaseCommand):
    help = 'Save a new messasure from one of the queues'

    def consumer(queueName, host):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=5672))
        
        channel = connection.channel()
        
        channel.queue_declare(queue=queueName)

        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)

        channel.basic_consume(queue=queueName, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def handle(self, *args, **options):
        print('TEST')
        thread1 = threading.Thread(target=consumer, args=(QUEUE_NAME, ALERTS_QUEUE_PRIMARY))
        thread2 = threading.Thread(target=consumer, args=(QUEUE_NAME, ALERTS_QUEUE_SECONDARY))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()
        # # Retrieve the object you want to save
        # meassure = Meassure(name= , flow= , location=)

        # # Save the object
        # meassure.save()

        # # Serialize the object to JSON
        # serialized_data = serializers.serialize('json', [obj])

        # # Save the serialized data to a file
        # filename = 'mymodel.json'
        # with open(filename, 'w') as f:
        #     f.write(serialized_data)

        # self.stdout.write(self.style.SUCCESS(f"Model saved to {filename}"))

# Register the command with Django's management system
management.commands['save_meassure'] = Command()