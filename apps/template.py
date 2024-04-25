from jinja2 import Environment, FileSystemLoader

template_env = Environment(loader=FileSystemLoader('template/'))
notes_env = Environment(loader=FileSystemLoader('notes/'))

def generate_from_template(template_file, **kwargs):
    template = template_env.get_template(template_file)
    return template.render(**kwargs)

