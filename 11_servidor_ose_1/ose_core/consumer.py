#!/usr/bin/env python
import pika, sys, os, threading, django, json
django.setup()
from ose_app.models import Alerts
from ose_app.models import Data

QUEUE_ALERT = os.getenv('QUEUE_ALERT', 'alert_queue')
ALERTS_QUEUE_PRIMARY = os.getenv('ALERTS_QUEUE_PRIMARY', 'alerts-queue-1')
ALERTS_QUEUE_SECONDARY = os.getenv('ALERTS_QUEUE_SECONDARY', 'alerts-queue-2')
QUEUE_DATA = os.getenv('QUEUE_DATA', 'data_queue')
DATA_QUEUE_PRIMARY = os.getenv('DATA_QUEUE_PRIMARY', 'data-queue-1')
DATA_QUEUE_SECONDARY = os.getenv('DATA_QUEUE_SECONDARY', 'data-queue-2')

def populate(queueName, host, model):
    print(f'Starting consumer for queue {queueName} host {host} and model {model}')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=5672))
    channel = connection.channel()
    channel.queue_declare(queue=queueName)

    def callback(ch, method, properties, body):
        print('consumiendo')
        data = json.loads(body)
        print('data consumida', data)
        print(data['name'])
        model.objects.create(name=data['name'], flow=data['flow'], location=data['location'])

    channel.basic_consume(queue=queueName, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == '__main__':
    thread1 = threading.Thread(target=populate, args=(QUEUE_ALERT, ALERTS_QUEUE_PRIMARY, Alerts))
    thread2 = threading.Thread(target=populate, args=(QUEUE_ALERT, ALERTS_QUEUE_SECONDARY, Alerts))
    thread3 = threading.Thread(target=populate, args=(QUEUE_DATA, DATA_QUEUE_PRIMARY, Data))
    thread4 = threading.Thread(target=populate, args=(QUEUE_DATA, DATA_QUEUE_SECONDARY, Data))
    
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()