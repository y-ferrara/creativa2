import pathlib
import sys
from subprocess import call

# Comprobar argumento
if len(sys.argv) != 2 or sys.argv[1] not in ["v1", "v2", "v3"]:
    print("Uso: python3 switch_reviews_version.py v1|v2|v3")
    sys.exit(1)
    
VERSION = sys.argv[1]

path = pathlib.Path().resolve()
ruta_compose = path / "practica_creativa2/bookinfo/docker-compose.micro.yaml"

call(f"docker-compose -f {ruta_compose} down", shell=True)

lineas = []
with open(ruta_compose, "r") as file:
    for linea in file:
        if VERSION == "v1":
            if "SERVICE_VERSION" in linea:
                lineas.append('      - SERVICE_VERSION=v1\n')
            elif "ENABLE_RATINGS" in linea:
                lineas.append('      - ENABLE_RATINGS=false\n')
            else:
                lineas.append(linea)
        elif VERSION == "v2":
            if "SERVICE_VERSION" in linea:
                lineas.append('      - SERVICE_VERSION=v2\n')
            elif "ENABLE_RATINGS" in linea:
                lineas.append('      - ENABLE_RATINGS=true\n')
            elif "STAR_COLOR" in linea:
                lineas.append('      - STAR_COLOR=black\n')
            else:
                lineas.append(linea)
        elif VERSION == "v3":
            if "SERVICE_VERSION" in linea:
                lineas.append('      - SERVICE_VERSION=v3\n')
            elif "ENABLE_RATINGS" in linea:
                lineas.append('      - ENABLE_RATINGS=true\n')
            elif "STAR_COLOR" in linea:
                lineas.append('      - STAR_COLOR=red\n')
            else:
                lineas.append(linea)
        
with open(ruta_compose, "w") as file:
    file.writelines(lineas)

call(f"docker-compose -f {ruta_compose} up -d", shell=True)