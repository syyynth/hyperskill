items: dict[str, int] = {
    'Bubblegum': 202,
    'Toffee': 118,
    'Ice cream': 2250,
    'Milk chocolate': 1680,
    'Doughnut': 1075,
    'Pancake': 80
}

print('Earned amount:')
for k, v in items.items():
    print(f'{k}: ${v}')

income: int = sum(items.values())
print(f'Income: ${income}')

sx: float = float(input('Staff expenses:'))
ox: float = float(input('Other expenses:'))
print(f'Net income: ${income - (sx + ox)}')
