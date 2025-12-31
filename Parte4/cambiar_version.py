from subprocess import call
import sys

if len(sys.argv) != 3 or sys.argv[1] not in ["v1", "v2", "v3"] or sys.argv[2] not in ["v1", "v2", "v3"]:
    print("Uso: python3 cambiar_version.py v1|v2|v3 NUEVA_VERSION")
    sys.exit(1) 

VERSION_ANTERIOR = sys.argv[1]
VERSION_NUEVA = sys.argv[2]

call(f"kubectl delete deployment reviews-{VERSION_ANTERIOR} -n cdps-18", shell=True)
call(f"kubectl apply -f reviews-{VERSION_NUEVA}-deployment.yaml -n cdps-18", shell=True)