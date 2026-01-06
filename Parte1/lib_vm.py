import logging, subprocess, os

from lxml import etree

log = logging.getLogger('auto_p2')

class VM: 
  def __init__(self, name):
    self.name = name

  def define_vm (self, image):
    log.debug("create_vm " + self.name + " (image: " + image + ")")
    subprocess.call([f"qemu-img create -F qcow2 -f qcow2 -b {image} {self.name}.qcow2"], shell=True)
    
    plantilla = "plantilla-vm-pc1.xml"
    xml_output = f"{self.name}.xml"
    tree = etree.parse(plantilla)
    root = tree.getroot()

    name = root.find("name")
    name.text = self.name
    log.debug(f"Cambiado nombre VM a: {self.name}")

    sourceDisk = root.find("./devices/disk/source")
    sourceDisk.set("file", os.path.abspath(f"{self.name}.qcow2"))
    log.debug(f"Ruta del disco actualizada a: {os.path.abspath(f'{self.name}.qcow2')}")

    sourceBridge = root.find("./devices/interface/source")  
    sourceBridge.set("bridge", "virbr0")
    log.debug(f"Puente de red actualizado a: virbr0")
    
    virtualport = root.find("./devices/interface/virtualport")
    if virtualport is not None:
      virtualport.getparent().remove(virtualport)
      log.debug("Etiqueta <virtualport> eliminada")
    
    tree.write(xml_output, pretty_print=True)
    log.debug(f"XML generado: {xml_output}")
    
    subprocess.call([f"sudo virsh define {self.name}.xml"], shell=True)
    log.debug(f"Definimos la maquina virtual {self.name}")
    
    subprocess.call([f"sudo virt-copy-in -a {self.name}.qcow2 parte1.py /home/cdps"], shell=True)
    log.debug("Copiamos el fichero parte1.py")

  def start_vm (self):
    subprocess.call([f"sudo virsh start {self.name}"], shell=True)
    log.debug("start_vm " + self.name)

  def show_console_vm (self):
    subprocess.call([f'xterm -e "sudo virsh console {self.name}" &'], shell=True)
    log.debug("show_console_vm " + self.name)

  def stop_vm (self):
    subprocess.call([f"sudo virsh shutdown {self.name}"], shell=True)
    log.debug("stop_vm " + self.name)

  def undefine_vm (self):
    subprocess.call([f"sudo virsh undefine {self.name}"], shell=True)
    subprocess.call([f"rm {self.name}.qcow2 -f"], shell=True)
    subprocess.call([f"rm {self.name}.xml"], shell=True)
    log.debug("destroy_vm " + self.name)
    
  def cmd_vm (self, cmd):
    log.debug("cmd_vm " + self.name + ": " + cmd)
    subprocess.call([f'virt-customize -a "{self.name}.qcow2" --run-command "{cmd}"'], shell=True)
