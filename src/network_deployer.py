from netmiko import ConnectHandler
def deploy_configuration(device_info, commands):
    print("connecting to the network device...")
    connection = ConnectHandler(**device_info)
    print ("sending configuration commands...")
    cli_outpout = connection.send_config_set(commands)
    print("saving configuration to startup-config...")
    connection.save_config()
    connection.disconnect
    print("configuration deployed successfully!")
    return cli_outpout