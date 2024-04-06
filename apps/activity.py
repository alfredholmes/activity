import datetime, pathlib

from jinja2 import Environment, FileSystemLoader

def run(args):
    try: 
        func = args[2]
    except IndexError:
        name = input('Please enter the function name, i.e. new')


    method = globals().get(func)
    method(args)

def new(args):
    env = Environment(loader=FileSystemLoader('template/'),trim_blocks=True, lstrip_blocks=True)
    template = env.get_template("activity.md")
    try:
        name = args[3]
    except IndexError:
        name = input('Enter task name: ')
    
    start_time = input('Start time (HH:MM:SS or dd-mm-yy HH:MM:SS, Default now): ')
    if start_time == "": 
        start_time = datetime.datetime.now().replace(microsecond=0)
    else:
        done = False
        while not done:
            if len(start_time.split(':')) == 2:
                start_time += ':00'
            try:
                start_time = datetime.datetime.strptime(start_time, "%H:%M:%S").time()
                start_time = datetime.datetime.combine(datetime.datetime.now(), start_time)
                done = True
            except ValueError:
                try:
                    start_time = datetime.datetime.strptime(start_time, "%d-%m%y %H:%M:%S").time()
                    done = True
                except ValueError:
                    print('Please enter date/time format as either dd-mm-yy HH:MM:SS or HH:MM:SS, seconds are optional')

    tags = input('Task tags (comma separated): ')
    if len(tags) > 0:
        tags = tags.split(',')

    note = template.render(name=name, start_time=start_time, tags=tags)
    with open(pathlib.join('notes', str(start_time) + name + '.md'), 'w') as f:
        f.write(note)
        
