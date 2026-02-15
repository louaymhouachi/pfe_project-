import ipaddress
import random
def generate_networks(principal_network, zone_names):
    networks = {}
    vlan_pool = list(range(10, 100, 10))
    random.shuffle(vlan_pool)
    
    
    
#transformer le réseau principal (texte) en objet réseau
    main_network = ipaddress.ip_network(principal_network)
    
#Découper le réseau principal en sous-réseau 
    subnets = list(main_network.subnets(new_prefix=24))
    
#Parcourir les zones , associer un sous-réseau à chaque zone et stocker les informations réseau de la zone 
    for i, zone_name in enumerate(zone_names):
        subnet = subnets[i]
        hosts = list(subnet.hosts())
        networks[zone_name] = {
            "vlan_id": vlan_pool[i],
             "netwrok": subnet,
             "gateway" : hosts[0],
             "switch_ip": hosts [1]
        }
    return networks   

