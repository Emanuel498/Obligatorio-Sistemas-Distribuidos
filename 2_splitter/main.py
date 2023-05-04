from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import uvicorn

class Measure(BaseModel):
    name: str


app = FastAPI()

@app.post("/ping")
def ping(measure: Measure):
    return JSONResponse(
            status_code=200,
            content=Measure,
        )

@app.get("/forward")
def forward(url):
    try:
        response = requests.get(url)
        return response.json()
    except: 
        return JSONResponse(
            status_code=500,
            content={"message": "Error executing request"},
        )

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)