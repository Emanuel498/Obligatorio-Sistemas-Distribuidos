import requests
import json

# Lista de las medidas que serán enviadas a nuestro Sistemas Distribuido
measures = [
    {"name": "dato 1", "flow": 10, "location": "Punta Carretas"},
    {"name": "dato 2", "flow": 15, "location": "Centro"},
    {"name": "dato 3", "flow": 12, "location": "Malvín"},
    {"name": "dato 4", "flow": 13, "location": "Tres Cruces"},
    {"name": "dato 5", "flow": 20, "location": "Blanqueada"},
    {"name": "dato 6", "flow": 22, "location": "Cerro Norte"},
    {"name": "dato 7", "flow": 4, "location": "Ciudad Vieja"},
    {"name": "dato 8", "flow": 4, "location": "Parque Batlle"},
    {"name": "dato 9", "flow": 6, "location": "Aguada"},
    {"name": "dato 10", "flow": 11, "location": "Goes"},
]

# Endpoint que le vamos a pegar para simular que son sensores.
url = "http://localhost:8080/measure"
def enviarDatos():
    for measure in measures:
        try:
            response = requests.post(url, json=measure)
            response.raise_for_status()
            print("Medida enviada:", measure)
        except requests.exceptions.RequestException as e:
            print("Error al enviar la medida:", e)
        
if __name__ == "__main__":
    enviarDatos()