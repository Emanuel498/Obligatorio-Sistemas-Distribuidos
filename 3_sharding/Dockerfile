FROM python:3.8-slim-buster

WORKDIR .

#Copiamos los archivos de la carpeta actual hacia docker
COPY . .

#Descargamos las dependencias
RUN pip3 install -r requirements.txt
RUN python -m pip install pika --upgrade

#Ejecutamos nuestra app en docker
ENTRYPOINT ["python3", "main.py"]