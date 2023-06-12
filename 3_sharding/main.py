#!/usr/bin/env python
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn
import pika
import json
import os

#QUEUE_HOST = os.getenv('QUEUE_HOST', 'localhost')
QUEUE_NAME = os.getenv('QUEUE_NAME', 'test_queue')
ALERTS_QUEUE_PRIMARY = os.getenv('ALERTS_QUEUE_PRIMARY', 'alerts-queue-1')
ALERTS_QUEUE_SECONDARY = os.getenv('ALERTS_QUEUE_SECONDARY', 'alerts-queue-2')

# Objeto alerta que vamos a obtener como request.
class Alert(BaseModel):
    name: str
    flow: float
    location: str

def execute_sendAlert(alert:Alert):
    hostSend = balance_endpoints()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostSend, port=5672))
    channel = connection.channel()
    #Declaramos la cola que va a utiliar
    channel.queue_declare(queue=QUEUE_NAME) 
    
    #Publico los mensajes en la cola
    jsonAlert = json.dumps(alert.__dict__)
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=jsonAlert)

    connection.close()
    # Realizamos un mensaje legible para el usuario final.
    responseFinal = "name:{}, flow:{}, location:{}".format(alert.__dict__['name'], alert.__dict__['flow'], alert.__dict__['location'])
    return ("Mensaje enviado: {} por la cola {} ".format(responseFinal, hostSend))

app = FastAPI()

# Flag que nos ayudará a equilibrar el envio a las colas de la función balance_endpoints()
endpoint_flag = True

@app.post("/sendAlert")
def sendAlert(alert:Alert):
    try:
        # Ejecutamos el envio de la alerta a la cola y además obtenemos el mensaje para enviar como response.
        sendResponse = execute_sendAlert(alert)
        return JSONResponse(sendResponse, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Realizamos un round robin básico para que vaya cambiando de queues.
def balance_endpoints():
    global endpoint_flag
    if endpoint_flag:
        endpoint_flag = False
        return ALERTS_QUEUE_PRIMARY
    endpoint_flag = True
    return ALERTS_QUEUE_SECONDARY

if __name__ == '__main__':

    uvicorn.run(app, host="0.0.0.0", port=80)