#export TEAM_ID="XX"
#sudo -E python3 parte1.py

from subprocess import call
import pathlib
import os
import subprocess

TEAM_ID = os.environ.get('TEAM_ID', 00)
print(f"Usando TEAM_ID={TEAM_ID}")

call("sudo apt update",shell=True)
call("sudo apt install -y python3-pip",shell=True)

call("git clone https://github.com/CDPS-ETSIT/practica_creativa2.git",shell=True)

path = pathlib.Path().resolve()
ruta = path / "practica_creativa2/bookinfo/src/productpage"

call(f"pip3 install -r {ruta}/requirements.txt",shell=True)

archivo = ruta / "templates/productpage.html"

lineas = []
with archivo.open('r') as f:
    for line in f:
        if "{% block title %}Simple Bookstore App{% endblock %}" in line:
            lineas.append("{% block title %}" + str(TEAM_ID) + "{% endblock %}\n")
        else:
            lineas.append(line)
            
archivo.write_text(''.join(lineas))

print("")
ip = subprocess.check_output("ifconfig eth0 | grep 'inet ' | awk '{print $2}'", shell=True).decode().strip()
print(f"Poner en el navegador{ip}:9090/productpage")

call(f"sudo python3 {ruta}/productpage_monolith.py 9090 -y",shell=True)

# En el navegador
#http://<ip-externa>:9090/productpage


