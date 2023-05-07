# Obligatorio-Sistemas-Distribuidos

## ¿Cómo probamos el splitter por separado?

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

## ¿Cómo probamos el sharding por separado?
1. Nos posicionamos en la carpeta 2_sharding y tiramops el comando ```docker build --tag server_sharding .```
2. Ejecutamos ``` ocker run -p 80:80 server_sharding ```
3. Vamos a postman y tiramos lo siguiente (en un POST): 
``` 
{
    "name": "data1",
    "flow": 12.4,
    "location": "Malvín Norte"
} 
```


