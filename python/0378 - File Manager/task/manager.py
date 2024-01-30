import glob
import math
import os
import shutil

os.chdir('module/root_folder')


def pwd():
    return os.getcwd()


def cd():
    try:
        os.chdir(command[3:])
        return pwd().split(os.sep)[-1]
    except FileNotFoundError:
        return 'Invalid path'


def humanize(size):
    unit = 1024
    power = min(int(math.log(size, unit)), 3)
    units = ['B', 'KB', 'MB', 'GB']

    return f'{size // pow(unit, power)}{units[power]}'


def get_size(st_size, is_file):
    if not args or not is_file:
        return ''

    commands = {'-l': str(st_size),
                '-lh': humanize(st_size)}

    return ' ' + commands.get(args[0], '')


def ls():
    files: list[os.DirEntry] = sorted(os.scandir(),
                                      key=lambda x: not x.is_dir())

    return '\n'.join(
        file.name + get_size(file.stat().st_size, file.is_file())
        for file in files
    )


def get_files(ext):
    return [file for file in glob.glob(f'*{ext}') if os.path.isfile(file)]


def rm_ext(file):
    files = get_files(file)
    if not files:
        return f'File extension {file} not found in this directory'

    for f in files:
        os.remove(f)


def rm():
    if not args:
        return 'Specify the file or directory'
    file = args[0]

    try:
        if file.startswith('.'):
            return rm_ext(file)
        elif os.path.isfile(file):
            os.remove(file)
        else:
            shutil.rmtree(file)
    except FileNotFoundError:
        return 'No such file or directory'


def mv_ext(fr, to):
    files = get_files(fr)
    if not files:
        return f'File extension {fr} not found in this directory'

    for file in files:
        dest = os.path.join(to, os.path.basename(file))
        if os.path.exists(dest):
            if input(f'{file} already exists in this directory. Replace? (y/n)\n') == 'y':
                shutil.move(file, dest)
        else:
            shutil.move(file, dest)


def mv():
    if len(args) != 2:
        return 'Specify the current name of the file or directory and the new location and/or name'

    fr, to = args

    if fr.startswith('.'):
        return mv_ext(fr, to)

    if not os.path.exists(fr):
        return 'No such file or directory'

    if os.path.isdir(to):
        to = os.path.join(to, os.path.basename(fr))

    if os.path.exists(to):
        return 'The file or directory already exists'

    if os.path.isdir(fr) and os.path.commonpath([fr, to]) == fr:
        return 'The file or directory already exists'

    shutil.move(fr, to)


def mkdir():
    if len(args) != 1:
        return 'Specify the name of the directory to be made'
    name = args[0]

    if os.path.isdir(name):
        return 'The directory already exists'

    os.mkdir(name)


def cp_ext(fr, to):
    files = get_files(fr)
    if not files:
        return f'File extension {fr} not found in this directory'

    for file in files:
        destination = os.path.join(to, os.path.basename(file))
        if os.path.exists(destination):
            if input(f'{file} already exists in this directory. Replace? (y/n)\n') == 'y':
                shutil.copy(file, destination)
        else:
            shutil.copy(file, destination)


def cp():
    if len(args) < 1:
        return 'Specify the file'
    if len(args) != 2:
        return 'Specify the current name of the file or directory and the new location and/or name'

    fr, to = args

    if fr.startswith('.'):
        return cp_ext(fr, to)

    if not os.path.exists(fr):
        return 'No such file or directory'

    if os.path.isdir(to):
        to = os.path.join(to, os.path.basename(fr))

    if os.path.isfile(to):
        return f'{fr} already exists in this directory'

    shutil.copy(fr, to)


ACTIONS = {
    'pwd': pwd, 'cd': cd, 'ls': ls, 'mv': mv, 'rm': rm, 'mkdir': mkdir, 'cp': cp
}

while (command := input()) != 'quit':
    cmd, *args = command.split()
    if out := ACTIONS.get(cmd, lambda: 'Invalid command')():
        print(out)
