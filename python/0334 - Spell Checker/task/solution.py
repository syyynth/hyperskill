import nltk


def cmp(w: str) -> tuple[int, int]:
    """ Custom sort comparator to sort corpus based on Edit Distance and n-gram frequency. """
    ed = nltk.edit_distance(word, w)
    prev_word = freq_dist.get((user_tokens[i - 1], w), 0)
    next_word = freq_dist.get((w, user_tokens[i + 1]), 0)

    return ed, -(prev_word + next_word)


text = input('Hello! Please, enter a text here:\n')
user_tokens = nltk.word_tokenize(text)

with open('books.txt') as f:
    corpus = nltk.word_tokenize(f.read())

corpus_set = set(corpus)
freq_dist = nltk.FreqDist(nltk.ngrams(corpus, 2))

misspelled_words = [token for token in user_tokens if token not in corpus_set]
print(f'Misspelled words found in your text: {", ".join(misspelled_words)}')

grade = 'AABBCCDDE'[min(len(misspelled_words), 8)]
print(f'Your grade is {grade}. Errors found in the text: {len(misspelled_words)}.')

corrected_words = []
for i, word in enumerate(user_tokens):
    if word in misspelled_words:
        word = min(corpus_set, key=cmp)
    corrected_words.append(word)
print(' '.join(corrected_words))
