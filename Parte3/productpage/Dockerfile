FROM python:3.9-slim

#Copiamos los archivos necesarios
COPY . .

#Instalamos dependencias de requirements
RUN pip3 install -r requirements.txt

#Exponemos el puerto 9080
EXPOSE 9080

#Ejecutamos la aplicacion
CMD ["python3", "productpage.py", "9080"]