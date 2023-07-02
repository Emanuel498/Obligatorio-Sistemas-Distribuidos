#!/usr/bin/env python
import pika, sys, os, threading, django, json

QUEUE_NAME = os.getenv('QUEUE_NAME', 'data_queue')
DATA_QUEUE_PRIMARY = os.getenv('DATA_QUEUE_PRIMARY', 'data-queue-1')
DATA_QUEUE_SECONDARY = os.getenv('DATA_QUEUE_SECONDARY', 'data-queue-2')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ine1_core.settings")
django.setup()
from ine1_app.models import Data

def data(exchangeName, host):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=5672))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchangeName, exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=exchangeName, queue=queue_name)

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(data['name'])
        Data.objects.create(name=data['name'], flow=data['flow'], location=data['location'])

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == '__main__':
    thread1 = threading.Thread(target=data, args=(QUEUE_NAME, DATA_QUEUE_PRIMARY))
    thread2 = threading.Thread(target=data, args=(QUEUE_NAME, DATA_QUEUE_SECONDARY))
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()