import requests

cache = requests.get(f'http://www.floatrates.com/daily/{input()}.json').json()
seen = {'usd', 'eur'}

inp = []
for v in iter(input, ''):
    inp.append(v)
    if len(inp) == 2:
        curr, val = inp
        print('Checking the cache...')
        print('Oh, It is in the cache!' if curr in seen else 'Sorry, but it is not in the cache!')
        print(f'You received {cache[curr]["rate"] * float(val)} {curr.upper()}.')
        seen.add(curr)
        inp = []
