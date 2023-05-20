# 📡📡 Obligatorio-Sistemas-Distribuidos 📡📡

## 🛂🛂 ¿Cómo probamos el splitter por separado? 🛂🛂
1. Nos posicionamos en la carpeta 2_splitter y tiramops el comando ```docker build --tag server_splitter .```
2. Ejecutamos ``` docker run -p 80:80 server_splitter ```
3. Vamos a postman y tiramos lo siguiente (en un POST): 
``` 
{
    "name": "data1",
    "flow": 12.4,
    "location": "Malvín Norte"
} 
```

## 🔀🔀 ¿Cómo probamos el sharding por separado? 🔀🔀
1. Nos posicionamos en la carpeta 2_sharding y tiramops el comando ```docker build --tag server_sharding .```
2. Ejecutamos ``` docker run -p 80:80 server_sharding ```
3. Vamos a postman y tiramos lo siguiente (en un POST): 
``` 
{
    "name": "data1",
    "flow": 12.4,
    "location": "Malvín Norte"
} 
```

## 🐳🐳 ¿Cómo ejecutamos docker-compose.yml 🐳🐳
- Nos posicionamos en la raíz del proyecto y ejecutamos: ``` docker compose build ```
- En la raíz, como estamos posicionados, luego de que haya buildeado el proyecto lanzamos: ``` docker compose up```

## 🚶🚶🚶🚶 ¿Cómo realizamos pruebas de las colas? 🚶🚶🚶🚶
1. Vamos a postman y seleccionamos un petición POST al siguiente edpoint: ``` localhost/measure ```
2. Dentro del body, seleccionamos ``` raw -> JSON ``` y colocamos el siguiente body:
``` 
{
    "name": "data1",
    "flow": 12.4,
    "location": "Malvin Norte"
}
```

## 🚶🚶🚶🚶 ¿Cómo ejecutar las colas y el servidor de OSE a la vez? 🚶🚶🚶🚶

1. Hacemos un ``` docker compose build ``` dónde vamos a buildear todo el proyecto.
2. Ahora tendremos que levantar por separado las queue y el producer, del servidor de OSE (esto de momento es así porque el servidor de OSE no es capaz de esperar hasta que terminen de levantar las colas y tira un error):
    - Ejecutamos ``` docker compose up  alerts-queue-1 alerts-queue-2 producer``` y esperamos hasta que levante todo correctamente.
    - Luego, en una nueva terminal, ejecutamos ``` docker compose up 11_servidor_ose_1 ``` y esperamos a que levante.
3. Ahora podemos tirar las alertas por POSTMAN como describimos anteriormente.


## 🏓🏓 Soluciones a implementar para algunos errores que se nos presentaron 🏓🏓
### ¿Qué hacemos si dentro de /3_sharding/main.py tenemos una advertencia al importar pika?

1. Confirmemos que tenemos la última versión de pip3 realizando: ``` pip install --upgrade pip ```
2. Luego tiremos el siguiente comando para que actualice la libreria de pika: ``` pip3 install pika ```