import gzip

from fastq import FastQ

if __name__ == '__main__':
    stats = {}
    best: int = 0

    for n in [0, 1, 2]:
        with gzip.open(input(), 'rt') as f:
            data: list[str] = f.readlines()
            for i in range(0, len(data), 4):
                FastQ(*data[i: i + 4])
        stats[n] = FastQ.summary()

        if (stats[n]['n'] < stats[best]['n']) \
                and (stats[n]['repeats'] < stats[best]['repeats']):
            best = n

        FastQ.reset()

    print(
        "Reads in the file = {reads}\n"
        "Reads sequence average length = {seq_average}\n"
        "Repeats = {repeats}\n"
        "Reads with Ns = {n}\n"
        "GC content average = {gc_avg}%\n"
        "Ns per read sequence = {n_avg}%".format(**stats[best])
    )
