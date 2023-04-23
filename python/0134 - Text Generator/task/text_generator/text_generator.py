import random
import string
from collections import Counter

with open(input(), encoding='utf-8') as f:
    corpus = f.read().split()


def get_random_word(corpus: list[str], weights: list[int] = None) -> str:
    return random.choices(corpus, weights)[0]


corpus_set = [*set(corpus)]
bigrams_counts = Counter(zip(corpus, corpus[1:]))
banned_chars = tuple(string.punctuation + string.digits)

grouped_data = {}
for (head, tail), count in bigrams_counts.items():
    grouped_data.setdefault(head, []).append((tail, count))

for _ in range(10):
    while ((word := get_random_word(corpus)).endswith(banned_chars)
           or word.startswith(banned_chars)
           or word[0] != word[0].upper()):
        word = random.choices(corpus_set)

    sent: list[str] = [word]

    while len(sent) < 5 or not sent[-1].endswith(tuple('.!?')):
        word = get_random_word(*zip(*grouped_data[word]))
        sent.append(word)

    print(' '.join(sent))
