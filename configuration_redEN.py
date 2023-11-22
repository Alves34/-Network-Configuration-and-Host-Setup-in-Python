import os
from colorama import Fore, Style, init
import ipaddress
import re

init()

def show_options(options):
    for idx, option in enumerate(options, start=1):
        print(f"{Fore.CYAN}{Style.BRIGHT}[{idx}] {option}")

options = [
    "Change IP", "Change hostname and host", "Install sLapd and ldap-utils packages", "Exit"
]

def validate_ip_address(ip_address):
    try:
        ipaddress.IPv4Address(ip_address)
        return True
    except ipaddress.AddressValueError:
        return False

def validate_host_name(host_name):
    host_pattern = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9.-]{1,253}$')
    return bool(re.match(host_pattern, host_name))

def modify_network_configuration():
    new_ip_address = input("Enter the new IP address: ")
    while not validate_ip_address(new_ip_address):
        print(f"{Fore.RED}Invalid IP address. Please try again.")
        new_ip_address = input("Enter the new IP address: ")

    new_subnet_mask = input("Enter the subnet mask (e.g., 24): ")
    new_gateway = input("Enter the gateway: ")

    new_configuration = f'''
    network:
      version: 2
      renderer: NetworkManager
      ethernets:
        enp0s3:
          addresses: [{new_ip_address}/{new_subnet_mask}]
          gateway4: {new_gateway}
          nameservers:
            addresses: [172.30.1.4] #DNS
    '''

    with open('/etc/netplan/01-network-manager-all.yaml', 'w') as file:
        file.write(new_configuration)

    os.system("sudo netplan apply")

def modify_hosts():
    host_name = input("Enter the new host name: ")
    while not validate_host_name(host_name):
        print(f"{Fore.RED}Invalid host name. Please try again.")
        host_name = input("Enter the new host name: ")

    domain_name = input("Enter the domain name: ")
    hosts_config = f'''
    127.0.0.1       localhost
    127.0.1.1       {host_name}.{domain_name} {host_name}
 
    # The following lines are desirable for IPv6 capable hosts
    ::1     ip6-localhost ip6-loopback
    fe00::0 ip6-localnet
    ff00::0 ip6-mcastprefix
    ff02::1 ip6-allnodes
    ff02::2 ip6-allrouters
    '''      
    with open('/etc/hosts', "w") as file:
        file.write(hosts_config)

def run_as_sudo():
    print(f"{Style.BRIGHT}{Fore.RED}REMEMBER TO RUN THIS PROGRAM WITH SUDO\n")
    input(f"{Fore.RED}Press any key to start")

run_as_sudo()  # Sudo execution alert

continue_execution = True
while continue_execution:
    os.system("clear")
    show_options(options)
    selection = input(f"{Style.BRIGHT}{Fore.CYAN}Select an option (type the number): ")

    if selection == "1":
        modify_network_configuration()
        input(f"{Style.BRIGHT}{Fore.MAGENTA}Press any key to continue...")
        os.system("clear")
    
    elif selection == "2":
        modify_hosts()
        input(f"{Style.BRIGHT}{Fore.MAGENTA}Press any key to continue...")
        os.system("clear")

    elif selection == "3":
        packages = ["slapd", "ldap-utils"]
        for package in packages:
            result = os.system(f"dpkg -s {package} > /dev/null 2>&1")
            if result != 0:
                print(f"{Fore.GREEN}The package {package} is not installed. Installing...")
                os.system(f"sudo apt-get install {package} -y")
                print(f"{Fore.CYAN}{package} installed successfully.")
            else:
                print(f"{Fore.GREEN}The package {package} is already installed.")

    elif selection == "4":
        continue_execution = False 
        
    input(f"{Fore.RED}Press any key to continue")