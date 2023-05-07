from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

class Measure(BaseModel):
    name: str
    flow: float
    location: str


app = FastAPI()

@app.post("/measure")
def ping(measure: Measure):
    return measure

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)