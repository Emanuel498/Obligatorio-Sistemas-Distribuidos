#!/usr/bin/env python
import pika, sys, os, threading, django, json

QUEUE_NAME = os.getenv('QUEUE_NAME', 'test_queue')
ALERTS_QUEUE_PRIMARY = os.getenv('ALERTS_QUEUE_PRIMARY', 'alerts-queue-1')
ALERTS_QUEUE_SECONDARY = os.getenv('ALERTS_QUEUE_SECONDARY', 'alerts-queue-2')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ose_core.settings")
django.setup()
from ose_app.models import Meassure

def main(queueName, host):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=5672))
    channel = connection.channel()
    channel.queue_declare(queue=queueName)

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(data['name'])
        Meassure.objects.create(name=data['name'], flow=data['flow'], location=data['location'])

    channel.basic_consume(queue=queueName, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    thread1 = threading.Thread(target=main, args=(QUEUE_NAME, ALERTS_QUEUE_PRIMARY))
    thread2 = threading.Thread(target=main, args=(QUEUE_NAME, ALERTS_QUEUE_SECONDARY))
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()