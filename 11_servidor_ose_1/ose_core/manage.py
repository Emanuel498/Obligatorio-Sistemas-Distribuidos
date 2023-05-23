#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os, sys, subprocess, threading, pika

QUEUE_NAME = os.getenv('QUEUE_NAME', 'test_queue')
ALERTS_QUEUE_PRIMARY = os.getenv('ALERTS_QUEUE_PRIMARY', 'alerts-queue-1')
ALERTS_QUEUE_SECONDARY = os.getenv('ALERTS_QUEUE_SECONDARY', 'alerts-queue-2')

def consumer(queueName, host):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=5672))
    
    channel = connection.channel()
    
    channel.queue_declare(queue=queueName)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue=queueName, on_message_callback=callback, auto_ack=True)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ose_core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    


if __name__ == '__main__':
    thread1 = threading.Thread(target=consumer, args=(QUEUE_NAME, ALERTS_QUEUE_PRIMARY))
    thread2 = threading.Thread(target=consumer, args=(QUEUE_NAME, ALERTS_QUEUE_SECONDARY))
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    main()
