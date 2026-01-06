import pathlib
from subprocess import call

call("git clone https://github.com/CDPS-ETSIT/practica_creativa2.git",shell=True)

path = pathlib.Path().resolve()
ruta1 = path / "practica_creativa2/bookinfo/src/productpage"
ruta2 = path / "practica_creativa2/bookinfo/src/details"
ruta3 = path / "practica_creativa2/bookinfo/src/reviews"
ruta3_docker = ruta3 / "reviews-wlpcfg"
ruta4 = path / "practica_creativa2/bookinfo/src/ratings"

productpage_dockerfile ="""
FROM python:3.9-slim

#Copiamos los archivos necesarios
COPY . .

#Instalamos dependencias de requirements
RUN pip3 install -r requirements.txt

#Exponemos el puerto 9080
EXPOSE 9080

#Ejecutamos la aplicacion
CMD ["python3", "productpage.py", "9080"]
"""

details_dockerfile ="""
FROM ruby:2.7.1-slim

WORKDIR /opt/microservices

COPY details.rb .

ENV ENABLE_EXTERNAL_BOOK_SERVICE=true

EXPOSE 7070

CMD ["ruby", "details.rb", "7070"]
"""

ratings_dockerfile ="""
FROM node:24-slim

WORKDIR /opt/microservices

COPY package.json .
COPY ratings.js .

ENV APP_VERSION=v1

RUN npm install

EXPOSE 9080

CMD ["node", "ratings.js", "9080"]
"""

with open(ruta1 / "Dockerfile", "w") as file:
    file.write(productpage_dockerfile)
    
with open(ruta2 / "Dockerfile", "w") as file:
    file.write(details_dockerfile)

with open(ruta4 / "Dockerfile", "w") as file:
    file.write(ratings_dockerfile)
    
call(f'docker run --rm -u root -v "{ruta3}":/home/gradle/project 'f'-w /home/gradle/project gradle:4.8.1 gradle clean build', shell=True)

TEAM_ID = "18"

call(f"docker build -t cdps-productpage:g{TEAM_ID} {ruta1}", shell=True)
call(f"docker build -t cdps-details:g{TEAM_ID} {ruta2}", shell=True)
call(f"docker build -t cdps-ratings:g{TEAM_ID} {ruta4}", shell=True)
call(f"docker build -t cdps-reviews:g{TEAM_ID} {ruta3_docker}", shell=True)

docker_compose_content = f"""
networks:
  cdps-net:
    driver: bridge

services:

  productpage:
    image: cdps-productpage:g{TEAM_ID}
    container_name: productpage_cdps_{TEAM_ID}
    ports:
      - "9090:9080"
    depends_on:
      - details
      - reviews
    networks:
      - cdps-net

  details:
    image: cdps-details:g{TEAM_ID}
    container_name: details_cdps_{TEAM_ID}
    networks:
      - cdps-net

  ratings:
    image: cdps-ratings:g{TEAM_ID}
    container_name: ratings_cdps_{TEAM_ID}
    networks:
      - cdps-net

  reviews:
    image: cdps-reviews:g{TEAM_ID}
    container_name: reviews_cdps_{TEAM_ID}
    environment:
      - SERVICE_VERSION=v2   # cambiar a v1 o v3
      - ENABLE_RATINGS=true
      - STAR_COLOR=black
    depends_on:
      - ratings
    networks:
      - cdps-net

"""

ruta_compose = path / "practica_creativa2/bookinfo/docker-compose.micro.yaml"
with open(ruta_compose, "w") as file:
    file.write(docker_compose_content)  

call(f"docker-compose -f {ruta_compose} up -d", shell=True)

