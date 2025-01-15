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
    file_path = os.path.join('notes', 'activity', start_time + " " + name + '.md') 
    with open(file_path, 'w') as f:
        f.write(note)

    edit(args)

    note = notes.Note(file_path)
    taskdone(args, note)

def taskdone(args, note):
    if 'end_time' not in note.metadata:
        note.metadata['end_time'] = datetime.datetime.now().replace(microsecond = 0)
        note.save()


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
    subprocess.call(['nvim', str(file_dict[times[0]])])
   

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


def weekly_total(args, today  = None):
    if today is None:
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

        print(file)

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
    return time

def weekly_totals(args, start = None, end=None):
    import matplotlib.pyplot as plt
    
    if end is None:
        end = datetime.date.today()
    
    if start is None:
        start = end - datetime.timedelta(days=end.timetuple().tm_yday)

    days = (end - start).days
    weeks = []
    hours = []
    for i in range(0, days + 7, 7):
        week = start + datetime.timedelta(days = i)
        print(week)
        total = weekly_total(args, week)
        weeks.append(week)
        hours.append(total.days * 24 + total.seconds / (60 * 60))

    plt.bar(weeks, hours, width=datetime.timedelta(days=7) - datetime.timedelta(seconds=10000))
    plt.show()




