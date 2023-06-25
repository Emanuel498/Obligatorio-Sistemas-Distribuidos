from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sqlite3
import uvicorn

app = FastAPI()

@app.get('/api/datos')
def obtener_datos():
    try:
        conn = sqlite3.connect('db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) AS cantidad, location FROM Alert GROUP BY location;')
        response = cursor.fetchall()
        conn.close()
        return response.json()
    except: 
        return JSONResponse(
            status_code=500,
            content={"message": "Error executing request"},
        )

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=80)