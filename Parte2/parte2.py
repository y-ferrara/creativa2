import pathlib
from subprocess import call

call("git clone https://github.com/CDPS-ETSIT/practica_creativa2.git",shell=True)

path = pathlib.Path().resolve()
ruta = path / "practica_creativa2/bookinfo/src/productpage"

call(f"mv Dockerfile {ruta}/Dockerfile", shell=True)

HTML_FILE = ruta /"templates/productpage.html"
PY_FILE = ruta / "productpage_monolith.py"

NEW_TITLE = "{% block title %}{{ app_owner }} - Group {{ team_id }}{% endblock %}\n"
NEW_ROUTE = """        'productpage.html',
        app_owner=os.environ.get("APP_OWNER", "unknown"),
        team_id=os.environ.get("TEAM_ID", "0"),
"""

lineas = []
with open(HTML_FILE, "r") as file:
    for linea in file:
        if "{% block title %}" in linea:
            lineas.append(NEW_TITLE)
        else:
            lineas.append(linea)
            
with open(HTML_FILE, "w") as file:
    for linea in lineas:
        file.write(linea)
        
lineas = []
with open(PY_FILE, "r") as file:
    for linea in file:
        if "productpage.html" in linea:
            lineas.append(NEW_ROUTE)
        else:
            lineas.append(linea)
with open(PY_FILE, "w") as file:
    for linea in lineas:
        file.write(linea)
        
print("")
print("Instrucciones para construir y ejecutar la imagen Docker:")
print(f"cd {ruta}")
print("docker build -t cdps-productpage:g18 .")
print("docker run --name productpage_cdps_18 -p 9095:8080 -e TEAM_ID=18 -e APP_OWNER=Ferrara-et-al -d cdps-productpage:g18")
print("")