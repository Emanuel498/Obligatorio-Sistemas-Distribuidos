#!/usr/bin/env python
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn
import pika
import os

QUEUE_HOST = os.getenv('QUEUE_HOST', 'localhost')
QUEUE_NAME = os.getenv('QUEUE_NAME', 'test')

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

def create_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=QUEUE_HOST, port=5672))
    channel = connection.channel()
    #Declaramos la cola que va a utiliar
    channel.queue_declare(queue=QUEUE_NAME) 
    
    for message in MESSAGES:
        #Publico los mensajes en la cola
        channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)
        print("[x] Mensaje enviado: %s " % message)
    
    connection.close()

app = FastAPI()

endpoints = ["http://localhost:8000", "http://localhost:8001"]

endpoint_flag = True

@app.get("/measure")
def measure():
    try:
        create_queue()
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)

def balance_endpoints():
    global endpoint_flag
    if endpoint_flag:
        endpoint_flag = False
        return endpoints[0]
    endpoint_flag = True
    return endpoints[1]

if __name__ == '__main__':

    uvicorn.run(app, host="0.0.0.0", port=80)