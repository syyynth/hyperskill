import random

ppl = int(input('Enter the number of friends joining (including you):\n'))

if ppl < 1:
    print('No one is joining for the party')
else:
    print('Enter the name of every friend (including you), each on a new line:')
    names = [input() for _ in range(ppl)]
    bill = float(input('Enter the total bill value:\n'))
    lucky = input('Do you want to use the "Who is lucky?" feature? Write Yes/No:\n')

    if lucky == 'Yes':
        name = random.choice(names)
        print(f'{name} is the lucky one!')
        print({n: 0 if n == name else round(bill / ~-len(names), 2) for n in names})
    else:
        print('No one is going to be lucky')
        print(dict.fromkeys(names, round(bill / len(names), 2)))
