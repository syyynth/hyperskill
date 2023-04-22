limit = int(input())

deps = 'Biotech Chemistry Engineering Mathematics Physics'.split()
peers = {d: [] for d in deps}
mapping = {
    'Biotech': (2, 3),
    'Chemistry': (3,),
    'Engineering': (4, 5),
    'Mathematics': (4,),
    'Physics': (2, 4)
}

with open('applicants.txt', encoding='U8') as f:
    submissions = [tuple(sub.split()) for sub in f.readlines()]


def get_score(x: tuple[str]) -> float:
    deps = mapping[x[priority + 7]]
    total = sum(float(x[i]) for i in deps)
    return total / len(deps)


seen = set()
for priority in range(3):
    for info in sorted(submissions, key=lambda x: (-max(get_score(x), float(x[6])), x[0], x[1])):
        fullname = f'{info[0]} {info[1]}'
        dep = info[priority + 7]
        score = max(float(info[6]), get_score(info))
        peer = fullname, score
        if info not in seen and len(peers[dep]) < limit:
            peers[dep].append(peer)
            seen.add(info)

for dep in peers:
    with open(f'{dep.lower()}.txt', 'w') as f:
        for name, score in sorted(peers[dep], key=lambda x: (-x[-1], x[0])):
            f.write(f'{name} {score}\n')
