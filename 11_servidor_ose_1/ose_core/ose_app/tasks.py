#!/usr/bin/env python
import pika, sys, os, threading
from celery import shared_task

QUEUE_NAME = os.getenv('QUEUE_NAME', 'test_queue')
#ALERTS_QUEUE_PRIMARY = os.getenv('ALERTS_QUEUE_PRIMARY', 'alerts-queue-1')
ALERTS_QUEUE_PRIMARY ='localhost'
ALERTS_QUEUE_SECONDARY = os.getenv('ALERTS_QUEUE_SECONDARY', 'alerts-queue-2')


@shared_task
def consume_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=ALERTS_QUEUE_PRIMARY, port=5672))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        #process_queue_item.delay(body.decode())

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()