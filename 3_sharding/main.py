from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import uvicorn
import pika

class Alert(BaseModel):
    name: str
    flow: float
    location: str

credentials = pika.PlainCredentials('guest', 'guest')

def create_queue(queue_name: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    connection.close()

def publish_message_to_rabbitmq(queue_name: str, message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    connection.close()

def consume_messages_from_rabbitmq(queue_name: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', port=5672, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
    if method_frame:
        print("Mensaje recibido: ", body)
    else:
        print("No hay mensajes en la cola.")
    connection.close()


app = FastAPI()

endpoints = ["http://localhost:8000", "http://localhost:8001"]

endpoint_flag = True

def balance_endpoints():
    global endpoint_flag
    if endpoint_flag:
        endpoint_flag = False
        return endpoints[0]
    endpoint_flag = True
    return endpoints[1]

@app.post("/enqueue")
def post_message_to_rabbitmq():
    try:
        publish_message_to_rabbitmq("alertas", "alerta")
        return {"message": "Mensaje enviado correctamente a la cola."}
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/measure")
def measure():
    try:
        return JSONResponse(content={"message": consume_messages_from_rabbitmq("alertas")}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1', 5672, '/', pika.credentials.PlainCredentials('guest', 'guest')))
    channel = connection.channel()

    channel.queue_declare(queue='mi_cola')

    channel.basic_publish(exchange='', routing_key='mi_cola', body='Hola, mundo!')
    print("Mensaje enviado")

    connection.close()
    uvicorn.run(app, host="0.0.0.0", port=80)