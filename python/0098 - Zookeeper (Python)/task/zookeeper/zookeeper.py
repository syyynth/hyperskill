from animals import *

animals = [camel, lion, deer, goose, bat, rabbit]

MSG = 'Please enter the number of the habitat you would like to view:'

while (cam := input(MSG)) != 'exit':
    print(animals[int(cam)])

print('See you later!')
