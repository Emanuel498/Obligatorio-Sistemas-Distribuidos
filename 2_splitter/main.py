from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import requests
import uvicorn

# Clase que simula los datos que van a ser enviados por sensores.
class Measure(BaseModel):
    name: str
    flow: float
    location: str

# Difine la app
app = FastAPI()

"""
Endpoint que recibe una medida y ... .

Attributes:
    measure (Measure): Medidas tomadas por los sensores.
"""
@app.post("/measure")
def postMeasure(measure: Measure):
    """
        Si la medida de flujo de agua, reportado por el sensor, 
        es menor a 12.8 litros se considera como alerta.
    """
    # Enviamos el dato al endpoint del Spliter del datos.
    requests.post("http://producer-data/sendData", json.dumps(measure.__dict__))
    response = JSONResponse(
        status_code=200,
        content="Se envio dato al Splitter de datos.",
    )
    if(measure.flow < 12.8):
        # Enviamos la medida al endpoint del Spliter del alert
        requests.post("http://producer-alerts/sendAlert", json.dumps(measure.__dict__))
        response =  JSONResponse(
            status_code=200,
            content="Se envio alerta al Splitter de alertas.",
        )
    return response
        

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)