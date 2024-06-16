from jinja2 import Environment, FileSystemLoader

template_env = Environment(loader=FileSystemLoader('template/'), trim_blocks=True, lstrip_blocks=True)
notes_env = Environment(loader=FileSystemLoader('notes/'), trim_blocks=True, lstrip_blocks=True)

def generate_from_template(template_file, **kwargs):
    template = template_env.get_template(template_file)
    return template.render(**kwargs)

