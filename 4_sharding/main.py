#!/usr/bin/env python
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn
import pika
import json
import os

QUEUE_DATA = os.getenv('QUEUE_DATA', 'data_queue')
DATA_QUEUE_PRIMARY = os.getenv('DATA_QUEUE_PRIMARY', 'data-queue-1')
DATA_QUEUE_SECONDARY = os.getenv('DATA_QUEUE_SECONDARY', 'data-queue-2')

# Objeto alerta que vamos a obtener como request.
class Data(BaseModel):
    name: str
    flow: float
    location: str

def execute_sendData(data:Data):
    hostSend = balance_endpoints()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostSend, port=5673))
    channel = connection.channel()
    #Declaramos la cola que va a utiliar
    channel.queue_declare(queue=QUEUE_DATA) 
    
    #Publico los mensajes en la cola
    jsonData = json.dumps(data.__dict__)
    channel.basic_publish(exchange='', routing_key=QUEUE_DATA, body=jsonData)

    connection.close()
    # Realizamos un mensaje legible para el usuario final.
    responseFinal = "name:{}, flow:{}, location:{}".format(data.__dict__['name'], data.__dict__['flow'], data.__dict__['location'])
    return ("Mensaje enviado: {} por la cola {} ".format(responseFinal, hostSend))

app = FastAPI()

# Flag que nos ayudará a equilibrar el envio a las colas de la función balance_endpoints()
endpoint_flag = True

@app.post("/sendData")
def sendData(data:Data):
    try:
        # Ejecutamos el envio de la alerta a la cola y además obtenemos el mensaje para enviar como response.
        sendResponse = execute_sendData(data)
        return JSONResponse(sendResponse, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Realizamos un round robin básico para que vaya cambiando de queues.
def balance_endpoints():
    global endpoint_flag
    if endpoint_flag:
        endpoint_flag = False
        return DATA_QUEUE_PRIMARY
    endpoint_flag = True
    return DATA_QUEUE_SECONDARY

if __name__ == '__main__':

    uvicorn.run(app, host="0.0.0.0", port=80)