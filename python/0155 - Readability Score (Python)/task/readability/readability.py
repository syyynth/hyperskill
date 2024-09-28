import argparse
import math
import re

import nltk


def assess_text_difficulty(text):
    sentences = nltk.tokenize.sent_tokenize(text)
    is_hard = len(text) > 100 or len(sentences) > 3
    return 'HARD' if is_hard else 'EASY'


def assess_text_difficulty_regexp(text):
    data = [
        len(nltk.tokenize.regexp_tokenize(sentences, "[0-9A-z']+"))
        for sentences in nltk.tokenize.sent_tokenize(text)
    ]

    is_hard = data and (sum(data) / len(data) > 10)
    return 'HARD' if is_hard else 'EASY'


def score_to_age(score):
    return score + 4, score + (5 if score < 14 else 8)


def read_text(path):
    with open(path) as f:
        text = f.read()
        return text


def automated_readability_index(chars_count, sentences, words_count):
    # 4.71 * |characters| / |words| + 0.5 * |words| / |sentences| - 21.43
    return math.ceil(4.71 * chars_count / words_count + 0.5 * words_count / sentences - 21.43)


def flesh_kincaid_readability_index(words_count, sentences, syllables):
    # 0.39 * |words| / |sentences| + 11.8 * |syllables| / |words| - 15.59
    return math.ceil(0.39 * words_count / sentences + 11.8 * syllables / words_count - 15.59)


def count_syllables(text):
    word = text.lower()
    x = re.findall(r'[aeiouy]{2}|the|e\B|[aiouy]', word)
    return len(x) or 1


def count_difficult_words(text, most_frequent_words):
    words = nltk.tokenize.regexp_tokenize(text, "[0-9A-z']+")
    return sum(w not in most_frequent_words for w in words)


def stats(text, most_frequent_words):
    chars_count = count_characters(text)
    sentences = nltk.tokenize.sent_tokenize(text)
    words_count = count_words(sentences)
    syllables = count_syllables(text)
    difficult_words = count_difficult_words(text, most_frequent_words)
    return chars_count, len(sentences), words_count, syllables, difficult_words


def count_words(sentences):
    return sum(len(nltk.tokenize.regexp_tokenize(s, "[0-9A-z']+")) for s in sentences)


def count_characters(text):
    return sum(len(token) for token in nltk.tokenize.word_tokenize(text))


def get_age_avg(ages):
    return (min(ages) + max(ages)) / 2


def dale_chall_readability_index(difficult_words, words_count, sentences):
    # 0.1579 * |difficult_words| / |words| * 100 + 0.0496 * |words| / |sentences|
    score = 0.1579 * difficult_words / words_count * 100 + 0.0496 * words_count / sentences
    if score < 5:
        score += 3.6365
    return math.ceil(score)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('longman3000')
    args = parser.parse_args()

    text = read_text(args.path)
    longman = set(read_text(args.longman3000).split())
    print(f'Text: {text}')

    chars_count, sentences, words_count, syllables, difficult_words = stats(text, longman)

    ari_score = automated_readability_index(chars_count, sentences, words_count)
    ari_age_lo, ari_age_hi = score_to_age(ari_score)

    fkrt_score = flesh_kincaid_readability_index(words_count, sentences, syllables)
    fkrt_age_lo, fkrt_age_hi = score_to_age(math.ceil(fkrt_score))

    dcri_score = dale_chall_readability_index(difficult_words, words_count, sentences)
    dcri_age_lo, dcri_age_hi = score_to_age(math.ceil(dcri_score))

    avg_age = get_age_avg([ari_age_lo, ari_age_hi, fkrt_age_lo, fkrt_age_hi, dcri_age_lo, dcri_age_hi])

    print(f'Characters: {chars_count}\n'
          f'Sentences: {sentences}\n'
          f'Words: {words_count}\n'
          f'Difficult words: {difficult_words}\n'
          f'Syllables: {syllables}\n'
          f'Automated Readability Index: {ari_score} (about {ari_age_lo}-{ari_age_hi} year olds).\n'
          f'Flesch–Kincaid Readability Test: {fkrt_score} (about {fkrt_age_lo}-{fkrt_age_hi} year olds).\n'
          f'Dale-Chall Readability Index: {dcri_score} (about {dcri_age_lo}-{dcri_age_hi} year olds).\n'
          f'This text should be understood in average by {avg_age} year olds.')
