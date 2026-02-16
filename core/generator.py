from jinja2 import Environment, FileSystemLoader
def generate_configs(sites):
    env = Environment(loader=FileSystemLoader("templates"))
    configs = {}
    for site in sites:
        for device in site ['device']:
            template_file = "core.j2" if device['type'] == "core" else "access.j2"
            template = env.get_template(template_file)
            config = template.render(
                device=device,
                site=site
            )
            key = f"{site['name']}_{device['name']}"
            configs[key] = config
    return configs        