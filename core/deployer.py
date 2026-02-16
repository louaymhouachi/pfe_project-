import os
import yaml

def deploy_configs(configs):
    # Création inventaire dynamique
    inventory = {'all': {'hosts': {}}}
    for key in configs:
        inventory['all']['hosts'][key] = {
            'ansible_host': key,
            'ansible_user': 'SSH_USER',  # Remplacer par site['ssh_user'] si besoin
            'ansible_password': 'SSH_PASS',  # idem
            'ansible_network_os': 'ios'
        }

    with open("inventory.yml", "w") as f:
        yaml.dump(inventory, f)

    # Création playbook dynamique
    playbook = []
    for key, cfg in configs.items():
        playbook.append({
            'name': f"Déploiement config {key}",
            'hosts': key,
            'gather_facts': False,
            'tasks': [
                {'name': 'Déployer configuration',
                 'cisco.ios.ios_config': {'lines': cfg.splitlines()}}
            ]
        })

    with open("playbook.yml", "w") as f:
        yaml.dump(playbook, f)

    # Lancer le playbook
    os.system("ansible-playbook -i inventory.yml playbook.yml")
