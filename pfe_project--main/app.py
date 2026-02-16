
from core.generator import generate_configs
from core.deployer import deploy_configs

def get_user_input():
    sites = []
    nb_sites = int(input("Combien de sites voulez-vous configurer ? "))
    
    for s in range(nb_sites):
        site_name = input(f"\nNom du site {s+1}: ")
        main_network = input(f"  Subnet principal (ex: 10.{s+1}.0.0/16): ")
        management_network = input(f"  Subnet management (ex: 192.168.{s+1}.0/24): ")
        
        # VLANs
        vlans = []
        nb_vlans = int(input(f"  Nombre de VLANs pour {site_name}: "))
        for v in range(nb_vlans):
            vlan_id = int(input(f"    ID du VLAN {v+1}: "))
            vlan_name = input(f"    Nom du VLAN {v+1}: ")
            vlans.append({"id": vlan_id, "name": vlan_name})
        
        # Switchs
        devices = []
        nb_switches = int(input(f"  Nombre de switchs pour {site_name}: "))
        for d in range(nb_switches):
            device_name = input(f"    Nom du switch {d+1}: ")
            device_type = input(f"    Type (core/access): ").lower()
            access_ports = []
            trunk_ports = []

            if device_type == "access":
                ports_access_input = input(f"      Ports access (séparés par , ou laisser vide pour auto): ")
                if ports_access_input.strip():
                    access_ports = ports_access_input.split(",")
                ports_trunk_input = input(f"      Ports trunk (séparés par , ou laisser vide pour auto): ")
                if ports_trunk_input.strip():
                    trunk_ports = ports_trunk_input.split(",")
            
            devices.append({
                "name": device_name,
                "type": device_type,
                "access_ports": access_ports,
                "trunk_ports": trunk_ports
            })

        # SSH
        ssh_user = input(f"  Nom utilisateur SSH pour {site_name}: ")
        ssh_pass = input(f"  Mot de passe SSH pour {site_name}: ")

        # Sécurité personnalisable
        enable_pass = input(f"  Mot de passe Enable pour {site_name}: ")
        console_pass = input(f"  Mot de passe Console pour {site_name}: ")
        vty_pass = input(f"  Mot de passe VTY pour {site_name}: ")

        sites.append({
            "name": site_name,
            "main_network": main_network,
            "management_network": management_network,
            "vlans": vlans,
            "devices": devices,
            "ssh_user": ssh_user,
            "ssh_pass": ssh_pass,
            "enable_pass": enable_pass,
            "console_pass": console_pass,
            "vty_pass": vty_pass
        })
    
    return sites

configs = generate_configs(get_user_input())
for key, config in configs.items():
    print(f"\nConfiguration pour {key}:")
    print(config)
deploy = input("voulez-vous déployer ces configurations? (oui/non):").lower()
if deploy == "oui":
    deploy_configs(configs)