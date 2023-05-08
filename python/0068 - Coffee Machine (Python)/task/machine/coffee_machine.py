import enum

import pandas as pd


class Names(enum.Enum):
    WATER = 'water'
    BEANS = 'beans'
    MONEY = 'money'
    CUPS = 'cups'
    MILK = 'milk'
    AMOUNT = 'has'
    UNIT = 'unit'
    RESOURCE = 'resource'


def cost(name: str) -> dict:
    match name:
        case 'espresso':
            return {Names.WATER: 250, Names.BEANS: 16, Names.MONEY: -4, Names.CUPS: 1}
        case 'latte':
            return {Names.WATER: 350, Names.MILK: 75, Names.BEANS: 20, Names.MONEY: -7, Names.CUPS: 1}
        case 'cappuccino':
            return {Names.WATER: 200, Names.MILK: 100, Names.BEANS: 12, Names.MONEY: -6, Names.CUPS: 1}


machine = pd.DataFrame([
    {Names.RESOURCE: Names.WATER, Names.MONEY: 200, Names.AMOUNT: 400, Names.UNIT: 'ml'},
    {Names.RESOURCE: Names.MILK, Names.MONEY: 50, Names.AMOUNT: 540, Names.UNIT: 'ml'},
    {Names.RESOURCE: Names.BEANS, Names.MONEY: 15, Names.AMOUNT: 120, Names.UNIT: 'gr'},
    {Names.RESOURCE: Names.CUPS, Names.MONEY: 1, Names.AMOUNT: 9, Names.UNIT: 'units'},
    {Names.RESOURCE: Names.MONEY, Names.MONEY: cost, Names.AMOUNT: 550, Names.UNIT: '$'},
])


def add() -> None:
    resource = [Names.WATER, Names.MILK, Names.BEANS, Names.CUPS]
    for res in resource:
        r = machine[Names.RESOURCE] == res
        print(f'Write how many {machine.loc[r, Names.UNIT].values[0]} of {res.value} you want to add:')
        machine.loc[r, Names.AMOUNT] += int(input())


def charge(flavor: str) -> None:
    after = (machine[Names.AMOUNT] - machine[Names.RESOURCE].map(cost(flavor))).fillna(machine[Names.AMOUNT])
    if (after < 0).any():
        print('Sorry, not enough resources!')
    else:
        print('I have enough resources, making you a coffee!')
        machine[Names.AMOUNT] = after


def buy() -> None:
    print('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')
    match input():
        case '1':
            charge('espresso')
        case '2':
            charge('latte')
        case '3':
            charge('cappuccino')
        case 'back':
            pass


def info() -> None:
    print('\nThe coffee machine has:')
    for resource in machine[Names.RESOURCE]:
        res = machine.loc[machine[Names.RESOURCE] == resource]
        print(f'{int(res[Names.AMOUNT].values[0])} {res[Names.UNIT].values[0]} of {resource.value}')
    print()


def take() -> None:
    query = machine[Names.RESOURCE] == Names.MONEY, Names.AMOUNT
    value = machine.loc[query].values[0]
    machine.loc[query] = 0
    print(f'I gave you ${value}')


if __name__ == '__main__':
    while True:
        print('Write action (buy, fill, take, remaining, exit):')
        action = input()
        match action:
            case 'buy':
                buy()
            case 'fill':
                add()
            case 'take':
                take()
            case 'remaining':
                info()
            case 'exit':
                break
