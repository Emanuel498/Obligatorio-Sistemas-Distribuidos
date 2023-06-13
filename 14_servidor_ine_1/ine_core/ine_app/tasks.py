#!/usr/bin/env python
import pika, sys, os, threading
from celery import shared_task

QUEUE_DATA = os.getenv('QUEUE_DATA', 'data_queue')
DATA_QUEUE_PRIMARY = os.getenv('DATA_QUEUE_PRIMARY', 'data-queue-1')
DATA_QUEUE_SECONDARY = os.getenv('DATA_QUEUE_SECONDARY', 'data-queue-2')


@shared_task
def consume_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=DATA_QUEUE_PRIMARY, port=5673))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_DATA)

    def callback(ch, method, properties, body):
        print('HOLA')
        print(" [x] Received %r" % body)
        #process_queue_item.delay(body.decode())

    channel.basic_consume(queue=QUEUE_DATA, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()