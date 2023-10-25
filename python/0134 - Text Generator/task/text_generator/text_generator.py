import random
import string
from collections import Counter

with open(input(), encoding='utf-8') as f:
    corpus = f.read().split()


def get_random_word(corpus: list[str], weights: list[int] = None) -> str:
    return random.choices(corpus, weights)[0]


corpus_set = [*set(corpus)]
trigrams_counts = Counter(zip(corpus, corpus[1:], corpus[2:]))
banned_chars = tuple(string.punctuation + string.digits)

grouped_data = {}
for (head1, head2, tail), count in trigrams_counts.items():
    grouped_data.setdefault((head1, head2), []).append((tail, count))

for _ in range(10):
    while True:
        word1, word2 = random.choices(list(grouped_data))[0]
        if (word1.endswith(banned_chars)
                or word1.startswith(banned_chars)
                or word1[0] != word1[0].upper()
                or word2.endswith(banned_chars)
                or word2.startswith(banned_chars)):
            continue
        break

    sent: list[str] = [word1, word2]

    while len(sent) < 5 or not sent[-1].endswith(tuple('.!?')):
        word = get_random_word(*zip(*grouped_data[(sent[-2], sent[-1])]))
        sent.append(word)

    print(' '.join(sent))
