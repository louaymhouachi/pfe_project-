from config_generator import generate_networks
from jinja2 import Environment, FileSystemLoader
from network_deployer import deploy_configuration 

#============saisie du nombre de sites=================
nb_sites = int(input("How many sites do you want to configure?"))
env = Environment(loader=FileSystemLoader("templates"))
for s in range(nb_sites):
    print (f"\n=========SITE {s+1} CONFIGURATION ==========")
    #=============Paramètres réseau====================
    principal_network = input("Main Network (ex: 192.168.0.0/16):")
    nb_zones = int(input("How many VLAN in this sites?"))
    zones = {}
    for i in range (nb_zones):
     zone_name = input(f"zone {i+1} name:") 
     prefix = int(input(f"prefix for {zone_name} (ex:24):"))
     zones[zone_name] = prefix
#===========génération des réseaux========================
networks = generate_networks(principal_network, zones)  
#===========choix tupe équipement========================
device_type = input("device type (core/access):")
if device_type== "core":
    template = env.get_template("core_switch.j2")
else :
    template = env.get_template("access_switch.j2")
hostname = input("Hostname of the device:")
access_input = input("access interfaces (ex: g0/1,g0/2):")
access_interfaces = [i.strip() for i in access_input.split(",")]
trunk_input = input("trunk interfaces (ex: g0/23/g0/24):")
trunk_interfaces = [i.strip() for i in trunk_input.split(",")]
#==================préparer les ports d'acces=====================
access_ports = []
trunk_port = []
for i, (zones, data) in enumerate(networks.items()):
    if i< len(access_interfaces):
        access_ports.append({"interface":access_interfaces[i], "vlan": data["vlan_id"]})
#===================IP pour la route par defaut========================
firewall_ip= input("IP firewall for default route:")
management_zone = list(networks.keys())[0]
default_gateway= networks[management_zone]["gateway"]
print("\n======GENERATED CONFIG =========") 
#================rendu de template=========================
allowed_vlans =",".join(str(data["vlan_id"]) for data in networks.values())
config = template.render(hostname=hostname , zones= networks,access_ports= access_ports ,trunk_port=trunk_port,allowed_vlans =allowed_vlans,firewall_ip=firewall_ip,default_gateway=default_gateway ) 
print("\n======GENERATED CONFIG =========") 
print(config)
#===============parametre du device==============
device_ip = input("Device IP: ")
username = input("Username: ") 
password = input("password: ") 
device ={
    "device_type": "cisco_ios" ,
    "host": device_ip,
    "username": username ,
    "password": password
}     
#============déploiment=============================
confirm = input("Deploy this configuration? (yes/no):")
if confirm.lower() == "yes":
    result = deploy_configuration(device, config.split("\n"))
    print("\nDeployment result:")
    print(result)
print("\nAll sites processed successfully!")

