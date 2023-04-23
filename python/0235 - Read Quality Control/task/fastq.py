from collections import defaultdict, Counter


class FastQ:
    fastq: list['FastQ'] = []

    def __init__(self,
                 identifier: str,
                 sequence: str,
                 separator: str,
                 score: str) -> None:
        self.identifier = identifier.strip()
        self.sequence = sequence.strip()
        self.separator = separator.strip()
        self.score = score.strip()
        self.fastq.append(self)

    def get_content(self) -> dict[str, float | int]:
        cnt: Counter[str] = Counter(self.sequence)

        return {
            'gc': (cnt['G'] + cnt['C']) / len(self.sequence) * 100,
            'n': cnt['N'] / len(self.sequence) * 100,
            'is_perfect': cnt['N'] == 0
        }

    @classmethod
    def summary(cls) -> dict[str, int | float]:
        lengths: defaultdict[int, int] = defaultdict(int)
        total_length: int = 0
        total_fastq: int = len(cls.fastq)
        total_gc_score: float = 0.0
        uniq_idents: set[str] = set()
        count_n: int = 0
        total_n: int = 0

        for fq in cls.fastq:
            seq: str = fq.sequence
            cont: dict[str, float | int] = fq.get_content()

            uniq_idents.add(seq)
            lengths[len(seq)] += 1
            total_length += len(seq)
            total_gc_score += cont['gc']
            total_n += cont['n']
            count_n += not cont['is_perfect']

        repeats: int = total_fastq - len(uniq_idents)
        seq_average: float = round(total_length / total_fastq)
        gc_avg: float = round(total_gc_score / total_fastq, 2)
        n_avg: float = round(total_n / total_fastq, 2)

        return {
            'reads': total_fastq,
            'seq_average': seq_average,
            'gc_avg': gc_avg,
            'repeats': repeats,
            'n': count_n,
            'n_avg': n_avg
        }

    @classmethod
    def reset(cls):
        cls.fastq = []
