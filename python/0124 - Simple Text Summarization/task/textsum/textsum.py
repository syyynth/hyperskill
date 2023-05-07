import math
import string

import nltk
from lxml import etree
from lxml.etree import _Element as xmlElement
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer

XML_PATH: str = 'news.xml'
STOPWORDS: set[str] = set(stopwords.words('english')) | set(string.punctuation)


def tokenizer(txt: str) -> list[str]:
    """ Tokenize a text by lemmatizing and removing stopwords and punctuation. """
    wnl: WordNetLemmatizer = WordNetLemmatizer()
    return [
        wnl.lemmatize(w.casefold())
        for w in nltk.word_tokenize(txt)
        if w.casefold() not in STOPWORDS
    ]


def boost_words(tfidf_vectors: csr_matrix, head_tokens: list[str], tfidf: TfidfVectorizer) -> None:
    """ Boost the words in the tfidf_vectors that are also in head_tokens by multiplying their values by 3. """
    vocab = tfidf.vocabulary_
    for word in head_tokens:
        if word in vocab:
            tfidf_vectors[:, vocab[word]] *= 3


def summarize_news(news: xmlElement) -> None:
    """ Summarize a news article using tf-idf. """
    head: str = news.find("value[@name='head']").text
    doc: str = news.find("value[@name='text']").text

    sentences: list[str] = nltk.sent_tokenize(doc)
    head_tokens: list[str] = tokenizer(head)

    tfidf: TfidfVectorizer = TfidfVectorizer(tokenizer=tokenizer)
    tfidf_vectors: csr_matrix = tfidf.fit_transform(sentences)

    boost_words(tfidf_vectors, head_tokens, tfidf)

    mean: list[float] = [r[r != 0].mean() for r in tfidf_vectors]
    sqrt_n: int = round(math.sqrt(len(sentences)))
    threshold: float = sorted(mean, reverse=True)[sqrt_n - 1]

    print('HEADER:', head)
    print('TEXT:', '\n'.join(s for s, m in zip(sentences, mean) if m >= threshold))
    print()


if __name__ == '__main__':
    root: xmlElement = etree.parse(XML_PATH).getroot()
    for art in root.iter('news'):
        summarize_news(art)
