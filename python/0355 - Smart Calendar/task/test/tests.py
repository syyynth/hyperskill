import os

from hstest import StageTest, TestedProgram, dynamic_test, WrongAnswer, TestPassed
import datetime
import os

class CalendarTest(StageTest):
    @dynamic_test
    def test_add(self):
        pr = TestedProgram()
        curr_path = os.getcwd()
        files = os.listdir(curr_path)
        for file in files:
            if file.endswith(".txt"):
                file_path = curr_path + '/' + file
                text = open(file_path, 'w')
                text.close()
        output = pr.start().lower()
        date = datetime.datetime.now()
        date_str = str(date)
        date_str = date_str[:-11]
        if 'current date and time' not in output:
            raise WrongAnswer("Your program should print: 'Current date and time:'")
        elif date_str not in output:
            raise WrongAnswer("It's not current date and time.")
        elif "enter the command (add, view, delete, exit)" not in output:
            raise WrongAnswer("Your program should print: 'Enter the command (add, view, delete, exit)'")
        sec_output = pr.execute('add').lower()
        if "what do you want to add (note, birthday)?" not in sec_output:
            raise WrongAnswer("Your program should print: 'What do you want to add (note, birthday)?'")
        third_output = pr.execute('note').lower()
        if "how many notes do you want to add?" not in third_output:
            raise WrongAnswer("Your program should print: 'How many notes do you want to add?'")
        fourth_output = pr.execute('3').lower()
        if "enter date and time of note #1 (in format «yyyy-mm-dd hh:mm»):" not in fourth_output:
            raise WrongAnswer("Your program should ask date and time of first note")
        first_date = date + datetime.timedelta(days=15)
        f_date = str(first_date)
        f_date = f_date[:-10]
        fifth_output = pr.execute(f_date).lower()
        if "enter text of note #1" not in fifth_output:
            raise WrongAnswer("Your program should print: 'Enter text of note #1'")
        first_note = 'Visit a doctor'
        sixth_output = pr.execute(first_note).lower()
        if "enter date and time of note #2 (in format «yyyy-mm-dd hh:mm»):" not in sixth_output:
            raise WrongAnswer("Your program should ask date and time of first note")
        second_date = date + datetime.timedelta(days=30)
        s_date = str(second_date)
        s_date = s_date[:-10]
        seventh_output = pr.execute(s_date).lower()
        if "enter text of note #2" not in seventh_output:
            raise WrongAnswer("Your program should print: 'Enter text of note #2'")
        second_note = 'Visit granny'
        eighth_output = pr.execute(second_note).lower()
        if "enter date and time of note #3 (in format «yyyy-mm-dd hh:mm»):" not in eighth_output:
            raise WrongAnswer("Your program should ask date and time of first note")
        third_date = date + datetime.timedelta(days=2)
        t_date = str(third_date)
        t_date = t_date[:-10]
        next_output = pr.execute(t_date).lower()
        if "enter text of note #3" not in next_output:
            raise WrongAnswer("Your program should print: 'Enter text of note #3'")
        third_note = 'Go to the cinema'
        one_more_output = pr.execute(third_note).lower()
        if 'notes added' not in one_more_output:
            raise WrongAnswer("Your program should print 'Notes added!'")
        elif "enter the command (add, view, delete, exit)" not in one_more_output:
            raise WrongAnswer("Your program should print: 'Enter the command (add, view, delete, exit)'")
        ninth_output = pr.execute('add').lower()
        if "what do you want to add (note, birthday)?" not in ninth_output:
            raise WrongAnswer("Your program should print: 'What do you want to add (note, birthday)?'")
        tenth_output = pr.execute('birthday').lower()
        if "how many dates of birth do you want to add?" not in tenth_output:
            raise WrongAnswer("Your program should print: 'How many dates of birth do you want to add?'")
        fnb_output = pr.execute('2').lower()
        if "enter the name of #1" not in fnb_output:
            raise WrongAnswer("Your program should print: 'Enter the name of #1'")
        fdb_output = pr.execute('Dave Smith').lower()
        if "enter the date of birth of #1 (in format «yyyy-mm-dd»):" not in fdb_output:
            raise WrongAnswer("Your program should print: 'Enter the date of birth of #1 (in format «YYYY-MM-DD»):'")
        current_date = datetime.date.today()
        f_year = date.year - 33
        today_birthday = datetime.date(f_year, current_date.month, current_date.day)
        t_birthday = str(today_birthday)
        snb_output = pr.execute(t_birthday).lower()
        if "enter the name of #2" not in snb_output:
            raise WrongAnswer("Your program should print: 'Enter the name of #2'")
        sdb_output = pr.execute('Mike Baker').lower()
        if "enter the date of birth of #2 (in format «yyyy-mm-dd»):" not in sdb_output:
            raise WrongAnswer("Your program should print: 'Enter the date of birth of #2 (in format «YYYY-MM-DD»):'")
        second_birthday = current_date - datetime.timedelta(days=13134)
        s_birthday = str(second_birthday)
        tnb_output = pr.execute(s_birthday).lower()
        if 'birthdates added' not in tnb_output:
            raise WrongAnswer("Your program should print 'Birthdates added'")
        elif "enter the command (add, view, delete, exit)" not in tnb_output:
            raise WrongAnswer("Your program should print: 'Enter the command (add, view, delete, exit)'")
        eleventh_output = pr.execute('view').lower()
        if 'what do you want to view (date, note, name)?' not in eleventh_output:
            raise WrongAnswer("Your program should print 'What do you want to view (date, note, name)?'")
        twelfth_output = pr.execute('date').lower()
        if 'enter date (in format «yyyy-mm-dd»):' not in twelfth_output:
            raise WrongAnswer("Your program should print 'Enter date (in format «YYYY-MM-DD»):'")
        date = f_date[:10]
        fourteenth_output = pr.execute(date).lower()
        if '1 note(s)' not in fourteenth_output:
            raise WrongAnswer("Incorrect number of events specified in search by date")
        elif '1 date(s) of birth' not in fourteenth_output:
            raise WrongAnswer("Incorrect number of dates of birth specified in search by date")
        elif 'before the event note' not in fourteenth_output:
            raise WrongAnswer("Your program should print 'Before the event note...'")
        elif 'visit a doctor' not in fourteenth_output:
            raise WrongAnswer("Your program should print the note found by date")
        elif '14 day(s), 23 hour(s)' not in fourteenth_output:
            raise WrongAnswer("Wrong number of days of note found by date")
        elif 'mike baker' not in fourteenth_output:
            raise WrongAnswer("Your program should print the name of the person who will have a birthday found by date")
        elif 'in 15 days' not in fourteenth_output:
            raise WrongAnswer("Your program should print the number of days left until birthday")
        elif '36 years old' not in fourteenth_output:
            raise WrongAnswer("Wrong number of years")
        elif "enter the command (add, view, delete, exit)" not in fourteenth_output:
            raise WrongAnswer("Your program should print: 'Enter the command (add, view, delete, exit)'")
        output15 = pr.execute('delete').lower()
        if "what do you want to delete (date, note, name)" not in output15:
            raise WrongAnswer("Your program should print: 'What do you want to delete (date, note, name)?'")
        output16 = pr.execute('name').lower()
        if "enter name" not in output16:
            raise WrongAnswer("Your program should print: 'Enter name'")
        output17 = pr.execute('Dave Smith').lower()
        if "dave smith" not in output17:
            raise WrongAnswer("Your program should print the name of the person who will have a birthday found by date")
        elif 'today' not in output17:
            raise WrongAnswer("Your program should print the number of days left until birthday")
        elif '33 years old' not in output17:
            raise WrongAnswer("Wrong number of years")
        elif 'are you sure you want to delete "dave smith"' not in output17:
            raise WrongAnswer("Your program should print 'Are you sure you want to delete' and a name of the person you want to delete")
        output18 = pr.execute('yes').lower()
        if 'birthdate deleted' not in output18:
            raise WrongAnswer(
                "Your program should print 'Birthdate deleted!'")
        elif "enter the command (add, view, delete, exit)" not in output18:
            raise WrongAnswer("Your program should print: 'Enter the command (add, view, delete, exit)'")
        output19 = pr.execute('view').lower()
        if 'what do you want to view (date, note, name)?' not in output19:
            raise WrongAnswer("Your program should print 'What do you want to view (date, note, name)?'")
        output19 = pr.execute('name').lower()
        if "enter name" not in output19:
            raise WrongAnswer("Your program should print: 'Enter name'")
        output19 = pr.execute('Dave Smith').lower()
        if "no such person found. try again" not in output19:
            raise WrongAnswer("Your program should print: 'No such person found. Try again:'")
        output20 = pr.execute('Mike Baker').lower()
        if 'mike baker' not in output20:
            raise WrongAnswer("Your program should print the name of the person who will have a birthday found by date")
        elif 'in 15 days' not in output20:
            raise WrongAnswer("Your program should print the number of days left until birthday")
        elif '36 years old' not in output20:
            raise WrongAnswer("Wrong number of years")
        elif "enter the command (add, view, delete, exit)" not in output20:
            raise WrongAnswer("Your program should print: 'Enter the command (add, view, delete, exit)'")
        output21 = pr.execute('view').lower()
        if 'what do you want to view (date, note, name)?' not in output21:
            raise WrongAnswer("Your program should print 'What do you want to view (date, note, name)?'")
        output22 = pr.execute('note').lower()
        if 'enter text of note' not in output22:
            raise WrongAnswer("Your program should print 'Enter text of note:'")
        output23 = pr.execute('Visit').lower()
        if 'found 2 note(s)' not in output23:
            raise WrongAnswer("Wrong number of events found by note")
        elif 'contain "visit":' not in output23:
            raise WrongAnswer("Your program should print text of note founded by note")
        elif 'before the event note' not in output23:
            raise WrongAnswer("Your program should print 'Before the event note...'")
        elif 'visit a doctor' not in output23:
            raise WrongAnswer("Your program should print the note found by note")
        elif '14 day(s), 23 hour(s)' not in output23:
            raise WrongAnswer("Wrong number of days of note found by note")
        elif 'visit granny' not in output23:
            raise WrongAnswer("Your program should print the note found by note")
        elif '29 day(s), 23 hour(s)' not in output23:
            raise WrongAnswer("Wrong number of days of note found by note")
        elif "enter the command (add, view, delete, exit)" not in output23:
            raise WrongAnswer("Your program should print: 'Enter the command (add, view, delete, exit)'")
        output24 = pr.execute('delete').lower()
        if "what do you want to delete (date, note, name)" not in output24:
            raise WrongAnswer("Your program should print: 'What do you want to delete (date, note, name)?'")
        output25 = pr.execute('date').lower()
        if 'enter date (in format «yyyy-mm-dd»):' not in output25:
            raise WrongAnswer("Your program should print 'Enter date (in format «YYYY-MM-DD»):'")
        output26 = pr.execute(date).lower()
        if '1 note(s)' not in output26:
            raise WrongAnswer("Incorrect number of events specified in search by date")
        elif '1 date(s) of birth' not in output26:
            raise WrongAnswer("Incorrect number of dates of birth specified in search by date")
        elif 'before the event note' not in output26:
            raise WrongAnswer("Your program should print 'Before the event note...'")
        elif 'visit a doctor' not in output26:
            raise WrongAnswer("Your program should print the note found by date")
        elif '14 day(s), 23 hour(s)' not in output26:
            raise WrongAnswer("Wrong number of days of note found by date")
        elif 'mike baker' not in output26:
            raise WrongAnswer("Your program should print the name of the person who will have a birthday found by date")
        elif 'in 15 days' not in output26:
            raise WrongAnswer("Your program should print the number of days left until birthday")
        elif '36 years old' not in output26:
            raise WrongAnswer("Wrong number of years")
        elif 'are you sure you want to delete "visit a doctor"' not in output26:
            raise WrongAnswer("Your program should print 'Are you sure you want to delete' and a note you want to delete")
        output27 = pr.execute('yes').lower()
        if 'note deleted' not in output27:
            raise WrongAnswer(
                "Your program should print 'Note deleted!'")
        elif 'are you sure you want to delete "mike baker"' not in output27:
            raise WrongAnswer("Your program should print 'Are you sure you want to delete' and a name of the person you want to delete")
        output28 = pr.execute('no').lower()
        if 'deletion canceled' not in output28:
            raise WrongAnswer(
                "Your program should print 'Deletion canceled'")
        elif "enter the command (add, view, delete, exit)" not in output28:
            raise WrongAnswer("Your program should print: 'Enter the command (add, view, delete, exit)'")
        output29 = pr.execute('delete').lower()
        if "what do you want to delete (date, note, name)" not in output29:
            raise WrongAnswer("Your program should print: 'What do you want to delete (date, note, name)?'")
        output30 = pr.execute('note').lower()
        if 'enter text of note' not in output30:
            raise WrongAnswer("Your program should print 'Enter text of note:'")
        output31 = pr.execute('Visit a doctor').lower()
        if 'no such note found. try again' not in output31:
            raise WrongAnswer("Your program should print 'No such note found. Try again'")
        output32 = pr.execute('Visit granny').lower()
        if 'are you sure you want to delete "visit granny"' not in output32:
            raise WrongAnswer("Your program should print 'Are you sure you want to delete' and a note you want to delete")
        output33 = pr.execute('yes').lower()
        if 'note deleted' not in output33:
            raise WrongAnswer(
                "Your program should print 'Note deleted!'")
        elif "enter the command (add, view, delete, exit)" not in output33:
            raise WrongAnswer("Your program should print: 'Enter the command (add, view, delete, exit)'")
        output34 = pr.execute('view').lower()
        if 'what do you want to view (date, note, name)?' not in output34:
            raise WrongAnswer("Your program should print 'What do you want to view (date, note, name)?'")
        output35 = pr.execute('note').lower()
        if 'enter text of note' not in output35:
            raise WrongAnswer("Your program should print 'Enter text of note:'")
        output36 = pr.execute('Visit granny').lower()
        if 'no such note found. try again' not in output36:
            raise WrongAnswer("Your program did not remove the note that should have been removed '")
        output37 = pr.execute('cinema').lower()
        if '1 note(s)' not in output37:
            raise WrongAnswer("Incorrect number of events specified in search by note")
        elif 'before the event note' not in output37:
            raise WrongAnswer("Your program should print 'Before the event note...'")
        elif 'go to the cinema' not in output37:
            raise WrongAnswer("Your program should print the note found by note")
        elif '1 day(s), 23 hour(s)' not in output37:
            raise WrongAnswer("Wrong number of days of note found by note")
        elif "enter the command (add, view, delete, exit)" not in output37:
            raise WrongAnswer("Your program should print: 'Enter the command (add, view, delete, exit)'")
        output38 = pr.execute('view').lower()
        if 'what do you want to view (date, note, name)?' not in output38:
            raise WrongAnswer("Your program should print 'What do you want to view (date, note, name)?'")
        output39 = pr.execute('name').lower()
        if "enter name" not in output39:
            raise WrongAnswer("Your program should print: 'Enter name'")
        output40 = pr.execute('Mike Baker').lower()
        if 'mike baker' not in output40:
            raise WrongAnswer("Your program should print the name of the person who will have a birthday found by date")
        elif 'in 15 days' not in output40:
            raise WrongAnswer("Your program should print the number of days left until birthday")
        elif '36 years old' not in output40:
            raise WrongAnswer("Wrong number of years")
        elif "enter the command (add, view, delete, exit)" not in output40:
            raise WrongAnswer("Your program should print: 'Enter the command (add, view, delete, exit)'")
        pr.execute('exit').lower()
        raise TestPassed()
