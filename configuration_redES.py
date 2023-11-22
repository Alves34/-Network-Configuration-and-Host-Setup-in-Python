import os
from colorama import Fore, Style, init
import ipaddress
import re

init()

def mostrar_opciones(opciones): 
    for idx, opcion in enumerate(opciones, start=1):
        print(f"{Fore.CYAN}{Style.BRIGHT}[{idx}] {opcion}")

opciones = [
    "Cambiar IP", "Cambiar hostname y host", "Instalar paquetes sLapd y ldap-utils", "Salir"
]

def validar_direccion_ip(direccion_ip):
    try:
        ipaddress.IPv4Address(direccion_ip)
        return True
    except ipaddress.AddressValueError:
        return False

def validar_nombre_host(nombre_host):
    patron_host = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9.-]{1,253}$')
    return bool(re.match(patron_host, nombre_host))

def modificar_configuracion_red():
    nueva_direccion_ip = input("Ingrese la nueva dirección IP: ")
    while not validar_direccion_ip(nueva_direccion_ip):
        print(f"{Fore.RED}Dirección IP no válida. Intente nuevamente.")
        nueva_direccion_ip = input("Ingrese la nueva dirección IP: ")

    nueva_mascara_red = input("Ingrese la máscara de red (p. ej. 24): ")
    nueva_puerta_enlace = input("Ingrese la puerta de enlace: ")

    nueva_configuracion = f'''
    network:
      version: 2
      renderer: NetworkManager
      ethernets:
        enp0s3:
          addresses: [{nueva_direccion_ip}/{nueva_mascara_red}]
          gateway4: {nueva_puerta_enlace}
          nameservers:
            addresses: [172.30.1.4] #DNS
    '''

    with open('/etc/netplan/01-network-manager-all.yaml', 'w') as file:
        file.write(nueva_configuracion)

    os.system("sudo netplan apply")

def modificar_hosts():
    Nombre_host = input("Ingrese el nuevo nombre de equipo: ")
    while not validar_nombre_host(Nombre_host):
        print(f"{Fore.RED}Nombre de host no válido. Intente nuevamente.")
        Nombre_host = input("Ingrese el nuevo nombre de equipo: ")

    nombre_dominio = input("Dime el nombre del dominio: ")
    config_hosts = f'''
    127.0.0.1       localhost
    127.0.1.1       {Nombre_host}.{nombre_dominio} {Nombre_host}
 
    # The following lines are desirable for IPv6 capable hosts
    ::1     ip6-localhost ip6-loopback
    fe00::0 ip6-localnet
    ff00::0 ip6-mcastprefix
    ff02::1 ip6-allnodes
    ff02::2 ip6-allrouters
    '''      
    with open('/etc/hosts', "w") as file:
        file.write(config_hosts)

def ejecutar_como_sudo():
    print(f"{Style.BRIGHT}{Fore.RED}ACUÉRDATE DE EJECUTAR ESTE PROGRAMA CON SUDO\n")
    input(f"{Fore.RED}Presiona una tecla para comenzar")

ejecutar_como_sudo()  # Alerta de ejecución con sudo

continuar = True
while continuar:
    os.system("clear")
    mostrar_opciones(opciones)
    seleccion = input(f"{Style.BRIGHT}{Fore.CYAN}Seleccione una opción (escriba el número): ")

    if seleccion == "1":
        modificar_configuracion_red()
        input(f"{Style.BRIGHT}{Fore.MAGENTA}Presione cualquier tecla para continuar...")
        os.system("clear")
    
    elif seleccion == "2":
        modificar_hosts()
        input(f"{Style.BRIGHT}{Fore.MAGENTA}Presione cualquier tecla para continuar...")
        os.system("clear")

    elif seleccion == "3":
        paquetes = ["slapd", "ldap-utils"]
        for paquete in paquetes:
            resultado = os.system(f"dpkg -s {paquete} > /dev/null 2>&1")
            if resultado != 0:
                print(f"{Fore.GREEN}El paquete {paquete} no está instalado. Instalándolo...")
                os.system(f"sudo apt-get install {paquete} -y")
                print(f"{Fore.CYAN}{paquete} instalado correctamente.")
            else:
                print(f"{Fore.GREEN}El paquete {paquete} ya está instalado.")

    elif seleccion == "4":
        continuar = False 
        
    input(f"{Fore.RED}Presione cualquier tecla para continuar")
