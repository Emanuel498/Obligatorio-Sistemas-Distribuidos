#!/usr/bin/env python
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn
import pika
import json
import os

#QUEUE_HOST = os.getenv('QUEUE_HOST', 'localhost')
QUEUE_NAME = os.getenv('QUEUE_NAME', 'test')
ALERTS_QUEUE_PRIMARY = os.getenv('ALERTS_QUEUE_PRIMARY', 'alerts-queue-1')
ALERTS_QUEUE_SECONDARY = os.getenv('ALERTS_QUEUE_SECONDARY', 'alerts-queue-2')

class Alert(BaseModel):
    name: str
    flow: float
    location: str

MESSAGES=[
    "TEST 1",
    "TEST 2",
    "TEST 3",
    "TEST 4",
    "TEST 5"
]

def create_queue(alert:Alert):
    hostSend = balance_endpoints()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostSend, port=5672))
    channel = connection.channel()
    #Declaramos la cola que va a utiliar
    channel.queue_declare(queue=QUEUE_NAME) 
    
    #Publico los mensajes en la cola
    jsonAlert = json.dumps(alert.__dict__)
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=jsonAlert)

    connection.close()
    return ("Mensaje enviado: {} por la cola {} ".format(jsonAlert, hostSend))

app = FastAPI()

endpoint_flag = True

@app.post("/measure")
def measure(alert:Alert):
    try:
        return JSONResponse(content={create_queue(alert)}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)

def balance_endpoints():
    global endpoint_flag
    if endpoint_flag:
        endpoint_flag = False
        return ALERTS_QUEUE_PRIMARY
    endpoint_flag = True
    return ALERTS_QUEUE_SECONDARY

if __name__ == '__main__':

    uvicorn.run(app, host="0.0.0.0", port=80)