This is the *Smart Calendar* project I made myself.


<p>The pace of life is quite high these days. The number of tasks that a person performs every day is huge. Everyone once forgot about an important meeting, a phone call, or even to wish a friend or relative a happy birthday. Let's try to solve this problem! In this project, we will develop a simple reminder calendar that will be able to save notes and dates of birthdays and remind us about them. If you want to learn how to work with the date and time format and create a calendar assistant, this project is for you!</p><br/><br/>Learn more at <a href="https://hyperskill.org/projects/355?utm_source=ide&utm_medium=ide&utm_campaign=ide&utm_content=project-card">https://hyperskill.org/projects/355</a>

Here's the link to the project: https://hyperskill.org/projects/355

Check out my profile: https://hyperskill.org/profile/1254124

The flow of the program:
```
Current date and time: 2023-08-08 11:11:11.111111
Enter the command (add, view, delete, exit):
> add
What do you want to add (note, birthday)?
> note
How many notes do you want to add?
> 3
Enter date and time of note #1 (in format «YYYY-MM-DD HH:MM»): 
> 2023-08-23 17:34
Enter text of note #1: 
> Visit a doctor
Enter date and time of note #2 (in format «YYYY-MM-DD HH:MM»): 
> 2023-09-07 17:34
Enter text of note #2: 
> Visit granny
Enter date and time of note #3 (in format «YYYY-MM-DD HH:MM»): 
> 2023-08-10 17:34
Enter text of note #3: 
> Go to the cinema
Notes added!
Enter the command (add, view, delete, exit):
> add
What do you want to add (note, birthday)?
> birthday
How many dates of birth do you want to add?
> 2
Enter the name of #1: 
> Dave Smith
Enter the date of birth of #1 (in format «YYYY-MM-DD»): 
> 1990-08-08
Enter the name of #2: 
> Mike Baker
Enter the date of birth of #2 (in format «YYYY-MM-DD»): 
> 1987-08-23
Birthdates added!
Enter the command (add, view, delete, exit):
> view
What do you want to view (date, note, name)?
> date
Enter date (in format «YYYY-MM-DD»):
> 2023-08-23
Found 1 note(s) and 1 date(s) of birth on this date:
Before the event note "Visit a doctor" remained: 14 day(s), 23 hour(s) and 59 minute(s).
Mike Baker's birthday is in 15 days. They turn 36 years old.
Enter the command (add, view, delete, exit):
> delete
What do you want to delete (date, note, name)?
> name
Enter name
> Dave Smith
Found 0 note and 1 dates of birth:
Dave Smith's birthday is today. They turn 33 years old.
Are you sure you want to delete "Dave Smith"?
> yes
Birthdate deleted!
Enter the command (add, view, delete, exit):
> view
What do you want to view (date, note, name)?
> name
Enter name:
> Dave Smith
No such person found. Try again:
Enter name:
> Mike Baker
Found 1 date of birth:
Mike Baker's birthday is in 15 days. They turn 36 years old.
Enter the command (add, view, delete, exit):
> view
What do you want to view (date, note, name)?
> note
Enter text of note:
> Visit
Found 2 note(s) that contain "Visit":
Before the event note "Visit a doctor" remained: 14 day(s), 23 hour(s) and 59 minute(s).
Before the event note "Visit granny" remained: 29 day(s), 23 hour(s) and 59 minute(s).
Enter the command (add, view, delete, exit):
> delete
What do you want to delete (date, note, name)?
> date
Enter date (in format «YYYY-MM-DD»):
> 2023-08-23
Found 1 note(s) and 1 date(s) of birth on this date:
Before the event note "Visit a doctor" remained: 14 day(s), 23 hour(s) and 59 minute(s).
Mike Baker's birthday is in 15 days. They turn 36 years old.
Are you sure you want to delete "Visit a doctor"?
> yes
Note deleted!
Are you sure you want to delete "Mike Baker"?
> no
Deletion canceled.
Enter the command (add, view, delete, exit):
> delete
What do you want to delete (date, note, name)?
> note
Enter text of note:
> Visit a doctor
No such note found. Try again:
Enter text of note:
> Visit granny
Found 1 note(s):
Are you sure you want to delete "Visit granny"?
> yes
Note deleted!
Enter the command (add, view, delete, exit):
> view
What do you want to view (date, note, name)?
> note
Enter text of note:
> Visit granny
No such note found. Try again:
Enter text of note:
> cinema
Found 1 note(s) that contain "cinema":
Before the event note "Go to the cinema" remained: 1 day(s), 23 hour(s) and 59 minute(s).
Enter the command (add, view, delete, exit):
> view
What do you want to view (date, note, name)?
> name
Enter name:
> Mike Baker
Found 1 date of birth:
Mike Baker's birthday is in 15 days. They turn 36 years old.
Enter the command (add, view, delete, exit):
> exit
```