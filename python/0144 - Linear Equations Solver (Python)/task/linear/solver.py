import argparse

import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--infile', required=True, type=str)
parser.add_argument('--outfile', required=True, type=str)
args = parser.parse_args()

with open(args.infile) as f:
    c, r = map(int, f.readline().split())
    data = np.array([
        [*map(complex if 'j' in line else float, line.split())]
        for line in (f.readline().strip() for _ in range(r))
    ])

X, x = data[:, :-1], data[:, -1]
rank = np.linalg.matrix_rank(X)
rank_augmented = np.linalg.matrix_rank(data)

with open(args.outfile, 'w') as f:
    if rank == rank_augmented:
        if rank == c:
            f.write('\n'.join(map(str, np.linalg.lstsq(X, x)[0])))
        else:
            f.write('Infinitely many solutions')
    else:
        f.write('No solutions')
