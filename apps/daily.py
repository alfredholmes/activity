import datetime
import os

import subprocess


from jinja2 import Environment, FileSystemLoader


def run(args):
    try: 
        func = args[2]
        method = globals().get(func)
    except IndexError:
        method = open_note

    method(args)

def open_note(args):
    try:
        day = args[3]
    except:
        day = datetime.datetime.now().strftime('%Y-%m-%d')

    
    file = os.path.join('notes', 'daily', day + '.md')
   
    try:
        with open(file, 'r') as f:
            pass
    except FileNotFoundError:
        env = Environment(loader=FileSystemLoader('template/'),trim_blocks=True, lstrip_blocks=True)
        template = env.get_template("daily.md")
        contents = template.render(date=day)
        with open(file, 'w') as f:
            f.write(contents)
 
    subprocess.call(['xdg-open', file])

    

