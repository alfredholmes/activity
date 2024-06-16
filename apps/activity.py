import datetime, os 

from . import notes, template


def run(args):
    try: 
        func = args[2]
    except IndexError:
        name = input('Please enter the function name, i.e. new')


    method = globals().get(func)
    method(args)

def new(args):
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
                    start_time = datetime.datetime.strptime(start_time, "%d-%m-%y %H:%M:%S").time()
                    done = True
                except ValueError:
                    print('Please enter date/time format as either dd-mm-yy HH:MM:SS or HH:MM:SS, seconds are optional')

    start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")

    tags = input('Task tags (comma separated): ')
    if len(tags) > 0:
        tags = tags.split(',')

    note = template.generate_from_template('activity.md', name=name, start_time=start_time, tags=tags)
    with open(os.path.join('notes', 'activity', start_time + " " + name + '.md'), 'w') as f:
        f.write(note)

    edit(args)

def done(args):
    files = notes.get_files(os.path.join('notes', 'activity')) 
    if len(files) == 0:
        return
    file_dict = {}
    for file in files:
        file_dict[os.path.getmtime(file)] = file


    times = [t for t in file_dict]
    times.sort(reverse=True)

    for t in times:
        note = notes.Note(str(file_dict[t]))
        if 'end_time' not in note.metadata:
            finished = input(f'Task { note.metadata["name"] } finished? (y/n): ')
            if finished == 'y':
                note.metadata['end_time'] = datetime.datetime.now().replace(microsecond = 0)
                note.save()
                break


def edit(args):
    files = notes.get_files(os.path.join('notes', 'activity')) 
    if len(files) == 0:
        return
    file_dict = {}
    for file in files:
        file_dict[os.path.getmtime(file)] = file


    times = [t for t in file_dict]
    times.sort(reverse=True)
    import subprocess
    subprocess.call(['xdg-open', str(file_dict[times[0]])])
   

def time_spent(args):
    try:
        today = args[3]
    except IndexError:
        today = datetime.datetime.now().strftime('%Y-%m-%d')

    files = notes.get_files(os.path.join('notes', 'activity'))
    time = datetime.timedelta()

    for file in files:
        if today not in str(file):
            continue


        note = notes.Note(file)
        try:
            start_time = datetime.datetime.strptime(note.metadata['start_time'], "%Y-%m-%d %H:%M")
        except ValueError:
            start_time = datetime.datetime.strptime(note.metadata['start_time'], "%Y-%m-%d %H:%M:%S")
        except TypeError:
            start_time = note.metadata['start_time']
        if 'end_time' not in note.metadata:
            end_time = datetime.datetime.now()
            time += end_time - start_time
            continue
        try:
            end_time = datetime.datetime.strptime(note.metadata['end_time'], "%Y-%m-%d %H:%M")
        except ValueError:
            end_time = datetime.datetime.strptime(note.metadata['end_time'], "%Y-%m-%d %H:%M:%S")
        except TypeError:
            end_time = note.metadata['end_time']

        time += end_time - start_time

    print(time)


def weekly_total(args):
    today = datetime.date.today()
    start = today - datetime.timedelta(days = today.weekday())
    week_days = [(start + datetime.timedelta(days = i)).strftime('%Y-%m-%d') for i in range(7)]

    tags = args[3:]

    
    files = notes.get_files(os.path.join('notes', 'activity'))

    time = datetime.timedelta()

    for file in files:
        in_week = False
        for day in week_days:
            if day in str(file):
                in_week = True



        if not in_week:
            continue

        correct_tags = True

        note = notes.Note(file) 
        for tag in tags:
            if tag not in note.metadata['tags']:
                correct_tags = False

        if not correct_tags:
            continue

        try:
            end_time = note.metadata['end_time']
        except KeyError:
            end_time = datetime.datetime.now()
            
        start_time = note.metadata['start_time']
        time += end_time - start_time

    print(time) 



