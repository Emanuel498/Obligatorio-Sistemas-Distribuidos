#!/usr/bin/env python
import pika, sys, os, threading

QUEUE_NAME = os.getenv('QUEUE_NAME', 'test_queue')
ALERTS_QUEUE_PRIMARY = os.getenv('ALERTS_QUEUE_PRIMARY', 'alerts-queue-1')
ALERTS_QUEUE_SECONDARY = os.getenv('ALERTS_QUEUE_SECONDARY', 'alerts-queue-2')

def main(queueName, host):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=5672))
    
    channel = connection.channel()
    
    channel.queue_declare(queue=queueName)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue=queueName, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    print('Test')
    thread1 = threading.Thread(target=main, args=(QUEUE_NAME, ALERTS_QUEUE_PRIMARY))
    thread2 = threading.Thread(target=main, args=(QUEUE_NAME, ALERTS_QUEUE_SECONDARY))
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()