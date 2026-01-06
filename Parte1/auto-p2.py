#!/usr/bin/env python

from lib_vm import VM
import logging, sys, subprocess, json

def call(cmd):
    print(f"Comando: {cmd}")
    subprocess.call([cmd], shell=True)  

def init_log(debug):
    # Creacion y configuracion del logger
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=log_level)
    log = logging.getLogger('auto_p2')
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.propagate = False

def pause():
    programPause = input("-- Press <ENTER> to continue...")
    

# Main
if len(sys.argv) < 2:
    print("Uso: auto-p2.py <define|start|stop|undefine>")
    sys.exit(1)
    
    
init_log(True)

argumento = sys.argv[1]

if argumento == "define":
    BASE_IMAGE = "cdps-vm-base-pc1.qcow2"
    s0 = VM("s0")
    s0.define_vm(BASE_IMAGE)
    s0.cmd_vm(f"sudo bash -c 'echo s0 > /etc/hostname'") # Asignar nombre de host
    s0.cmd_vm(f"sudo sed -i 's/cdps/s0/' /etc/hosts") # Actualizar /etc/hosts
    
elif argumento == "start":
    s0 = VM("s0")
    s0.start_vm()
    s0.show_console_vm()

elif argumento == "stop":
    s0 = VM("s0")
    s0.stop_vm()

elif argumento == "undefine":
    s0 = VM("s0")
    s0.stop_vm()
    s0.undefine_vm()
    
else:
    print("Uso: auto-p2.py <define|start|stop|undefine>")
    sys.exit(1)

