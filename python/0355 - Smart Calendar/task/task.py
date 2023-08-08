from pathlib import Path

import pandas as pd


def load_data(path: Path) -> pd.DataFrame:
    column_names = ['time', 'type', 'desc']
    path.unlink(missing_ok=True)
    path.touch()
    return pd.read_csv(path, names=column_names, header=0)


def save_data(path: Path) -> None:
    dataframe.to_csv(path, index=False)


def _next_birthday(bd: pd.Timestamp, date: pd.Timestamp) -> tuple[int, int]:
    is_next_year = bd.month < date.month or (bd.month == date.month and bd.day < date.day)
    next_bd = bd.replace(year=date.year + is_next_year)
    days_to_bd = (next_bd - date).days
    age = next_bd.year - bd.year
    return age, days_to_bd


def print_birthdays(birthdays: pd.DataFrame) -> None:
    current_date = pd.Timestamp('today').normalize()

    for row in birthdays.itertuples():
        birthday = pd.to_datetime(row.time)
        age, days = _next_birthday(birthday, current_date)
        print(f"{row.desc}'s birthday is in {days} days. They turn {age} years old." if days
              else f"{row.desc}'s birthday is today. They turn {age} years old.")


def get_time_difference(event_time: pd.Timestamp, current_time: pd.Timestamp) -> tuple[int, int, int]:
    time_difference = event_time - current_time
    days = time_difference.days
    hours = time_difference.seconds // 3600
    minutes = (time_difference.seconds % 3600) // 60
    return days, hours, minutes


def print_notes(notes_df: pd.DataFrame) -> None:
    current_time = pd.Timestamp('today')
    for row in notes_df.itertuples():
        event_time = pd.to_datetime(row.time)
        days, hours, minutes = get_time_difference(event_time, current_time)
        note = row.desc
        print(f'Before the event note "{note}" remained: {days} day(s), {hours} hour(s) and {minutes} minute(s).')


def search_date():
    d_note = input('Enter date (in format «YYYY-MM-DD»):\n')
    d_birth = d_note[-6:]
    notes = dataframe.query('time.str.contains(@d_note) & type == "note"')
    births = dataframe.query('time.str.contains(@d_birth) & type == "birth"')
    if len(notes) or len(births):
        print(f'Found {len(notes)} note(s) and {len(births)} date(s) of birth on this date:')
        print_notes(notes)
        print_birthdays(births)


def search_note():
    while True:
        note = input('Enter text of note:\n')
        notes = dataframe.query('desc.str.contains(@note) & type == "note"')
        if len(notes):
            print(f'Found {len(notes)} note(s) that contain "{note}":')
            print_notes(notes)
            break
        else:
            print('No such note found. Try again:')


def search_name():
    while True:
        name = input('Enter name:\n')
        names = dataframe.query('desc.str.contains(@name) & type == "birth"')
        if len(names):
            print(f'Found {len(names)} date of birth:')
            print_birthdays(names)
            break
        else:
            print('No such person found. Try again:')


def delete_entries(entries_df: pd.DataFrame, entry_type: str) -> None:
    for row in entries_df.itertuples():
        print(f'Are you sure you want to delete "{row.desc}"?')
        match input():
            case 'yes':
                dataframe.drop(row[0], inplace=True)
                print(f'{entry_type} deleted!')
            case 'no':
                print('Deletion canceled.')


def delete_date() -> None:
    print('Enter date (in format «YYYY-MM-DD»):')
    remove_date = input()
    remove_birth = remove_date[-6:]

    notes = dataframe.query('time.str.contains(@remove_date) & type == "note"')
    births = dataframe.query('time.str.contains(@remove_birth) & type == "birth"')
    print(f'Found {len(notes)} note(s) and {len(births)} date(s) of birth on this date:')

    print_notes(notes)
    print_birthdays(births)

    delete_entries(notes, 'Note')
    delete_entries(births, 'Birthdate')


def delete_note() -> None:
    while True:
        print('Enter text of note:')
        text = input()
        notes = dataframe.query('desc.str.contains(@text) & type == "note"')
        if len(notes):
            print(f'Found {len(notes)} note(s):')
            delete_entries(notes, 'Note')
            break
        else:
            print('No such note found. Try again:')


def delete_name() -> None:
    print('Enter name')
    name = input()

    notes = dataframe.query('desc.str.contains(@name) & type == "note"')
    births = dataframe.query('desc.str.contains(@name) & type == "birth"')

    print(f'Found {len(notes)} note and {len(births)} dates of birth:')

    print_notes(notes)
    print_birthdays(births)

    delete_entries(notes, 'Note')
    delete_entries(births, 'Birthdate')


def create_event(data1: str, data2: str, event_type: str) -> dict[str, str]:
    return {
        'time': data2 if event_type == 'birth' else data1,
        'type': event_type,
        'desc': data2 if event_type == 'note' else data1
    }


def append_to_dataframe(event: dict[str, str]) -> None:
    global dataframe
    dataframe = pd.concat([dataframe, pd.DataFrame([event])], ignore_index=True)


def add_events(number_of_events: int, prompt_1: str, prompt_2: str, event_type: str) -> None:
    for i in range(1, number_of_events + 1):
        append_to_dataframe(create_event(input(prompt_1 % i + '\n'),
                                         input(prompt_2 % i + '\n'),
                                         event_type))


def add_notes() -> None:
    count = int(input(f'How many notes do you want to add?\n'))
    add_events(count,
               'Enter date and time of note #%s (in format «YYYY-MM-DD HH:MM»): ',
               'Enter text of note #%s: ',
               'note')
    print('Notes added!')


def add_birthdays() -> None:
    count = int(input(f'How many dates of birth do you want to add?\n'))
    add_events(count,
               'Enter the name of #%s: ',
               'Enter the date of birth of #%s (in format «YYYY-MM-DD»): ',
               'birth')
    print('Birthdates added!')


ACTION_FUNCTIONS = {
    'add': {
        'note': add_notes,
        'birthday': add_birthdays
    }, 'view': {
        'date': search_date,
        'note': search_note,
        'name': search_name
    }, 'delete': {
        'date': delete_date,
        'note': delete_note,
        'name': delete_name
    }
}


def main() -> None:
    while True:
        command = input('Enter the command (add, view, delete, exit):\n')
        if command in ['add', 'view', 'delete']:
            huh = 'date, note, name' if command != 'add' else 'note, birthday'
            command_type = input(f'What do you want to {command} ({huh})?\n')
            ACTION_FUNCTIONS[command][command_type]()
        elif command == 'exit':
            return save_data(DATA_FILE_PATH)
        else:
            print('This command is not in the menu.')


if __name__ == '__main__':
    print('Current date and time:', pd.Timestamp('today'))
    DATA_FILE_PATH = Path('../notes.txt')
    dataframe = load_data(DATA_FILE_PATH)
    main()
