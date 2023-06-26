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

1. Hacemos un ``docker compose build`` dónde vamos a buildear todo el proyecto.
2. Ahora tendremos que levantar por separado las queue y el producer, del servidor de OSE (esto de momento es así porque el servidor de OSE no es capaz de esperar hasta que terminen de levantar las colas y tira un error):
  - Ejecutamos `` docker compose up`` y esperamos hasta que levante todo correctamente.
3. (Si es la primera vez que se corre la app) Vamos a la carpeta _11_servidor_ose_1/ose_core_ y ejecutamos los comandos en este orden:
  1. `docker ps` para poder obtener el ID del contenedor de *11_servidor_ose_1*
  2. Copiamos el ID y escribimos este comando: `docker exec -it <id> /bin/bash`
  3. Por ultimo, corremos `python3 manage.py migrate`
  4. Hacemos lo mismo para *14_servidor_ine_1*
4. Ahora podemos tirar las alertas por POSTMAN como describimos anteriormente.

### ¿Como crear un super user en Django (tiene acceso al admin)?
1. docker ps -> para obtener el ID del contenedor donde esta corriendo el servidor de Django
2. copiar el CONTAINER ID de la imagen obligatorio-sistemas-distribuidos_11_servidor_ose_1
3. docker exec -it {CONTAINER ID} bash
4. Ejecutar python manage.py createsuperuser

### ¿Como visualizar los datos del admin?
1. entrar en http://localhost:8000/admin/
2. Poner credenciales 




## 🏓🏓 Soluciones a implementar para algunos errores que se nos presentaron 🏓🏓
### ¿Qué hacemos si dentro de /3_sharding/main.py tenemos una advertencia al importar pika?

1. Confirmemos que tenemos la última versión de pip3 realizando: ``` pip install --upgrade pip ```
2. Luego tiremos el siguiente comando para que actualice la libreria de pika: ``` pip3 install pika ```

