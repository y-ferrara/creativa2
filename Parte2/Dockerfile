FROM python:3.9-slim

#Variables de entonrno
ENV APP_OWNER=desconocido
ENV TEAM_ID=0

COPY . .
RUN pip3 install -r requirements.txt

#Exponemos el puerto 8080
EXPOSE 8080

#Ejecutamos la aplicacion
CMD ["python3", "productpage_monolith.py", "8080"]