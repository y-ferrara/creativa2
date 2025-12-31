import pathlib
import sys
from subprocess import call

path = pathlib.Path().resolve()
ruta = path / "docker-compose.micro.yaml"

TEAM_ID = "18"

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

with open(ruta, "w") as file:
    file.write(docker_compose_content)  