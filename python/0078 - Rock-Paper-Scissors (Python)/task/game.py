import random

name = input('Enter your name: ')
print('Hello,', name)

options = {
    entity: ind
    for ind, entity
    in enumerate((input() or 'scissors,rock,paper').split(','))
}

print("Okay, let's start")

score_board = {name: 0}
with open('rating.txt', encoding='U8') as f:
    for rating in f:
        nick, score = rating.split()
        score_board[nick] = int(score)

while (user := input()) != '!exit':
    if user == '!rating':
        print('Your rating:', score_board[name])
        continue
    if user not in options:
        print('Invalid input')
        continue

    pc = random.choice(list(options))

    if user == pc:
        print(f'There is a draw ({user})')
        score_board[name] += 50
    elif (options[pc] - options[user]) % len(options) > len(options) // 2:
        print(f'Well done. The pc chose {pc} and failed')
        score_board[name] += 100
    else:
        print(f'Sorry, but the computer chose {pc}')

print('Bye!')
