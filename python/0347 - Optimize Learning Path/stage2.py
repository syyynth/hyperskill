from collections import defaultdict

with open('./dependencies.txt') as f:
    data = [line.strip().split(' -> ') for line in f.readlines()]

G = defaultdict(list)
indegree = defaultdict(int)

for u, v in data:
    G[u].append(v)
    indegree[u] += 0
    indegree[v] += 1

level = 0
ans = []

queue = [(level, i) for i in indegree if not indegree[i]]

while queue:
    if queue[0][0] == level:
        level += 1
        queue.sort()
    _, vertex = queue.pop(0)
    for v in G[vertex]:
        indegree[v] -= 1
        if indegree[v] == 0:
            queue.append((level, v))
    ans.append(vertex)

for index, line in enumerate(ans, start=1):
    print(f'{index}. {line}')
