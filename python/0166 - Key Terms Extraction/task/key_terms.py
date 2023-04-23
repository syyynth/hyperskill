from collections.abc import Iterator
from string import punctuation

from lxml import etree
from lxml.etree import _Element as xmlElement
from nltk import WordNetLemmatizer, word_tokenize, pos_tag
from nltk.corpus import stopwords
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer

WORDS_LIMIT: int = 5
XML_PATH: str = './news.xml'
wnl: WordNetLemmatizer = WordNetLemmatizer()
root: xmlElement = etree.parse(XML_PATH).getroot()
stopwords: set[str] = set(stopwords.words('english')) | set(punctuation)


def is_noun(w: str, pos: str) -> bool:
    """Check if a word is valid noun, if it's not in stopwords and not too short."""
    return (pos == 'NN'
            and len(w) > 1
            and w not in stopwords
            and not w.startswith("'"))


# tokenizing word by word even if it asked not to do it
def tokenizer(txt: str) -> list[str]:
    """Tokenize text and keep only valid nouns."""
    tokens: list[str] = word_tokenize(txt)
    tokens_lemma: Iterator[str] = (wnl.lemmatize(w) for w in tokens)
    tokens_nouns: list[str] = [
        t for t in tokens_lemma
        if is_noun(t, pos_tag([t])[0][1])
    ]
    return tokens_nouns


# probably how you should do it in real life 🤷🏼‍♂️🤷🏼‍♂️🤷🏼‍♂️
# def tokenizer(txt: str) -> list[str]:
#     # split text into sentences using nltk.sent_tokenize()
#     sentences = nltk.sent_tokenize(txt)
#     # tokenize each sentence into words using nltk.word_tokenize() for each sentence
#     sentences_tokens = [nltk.word_tokenize(sent) for sent in sentences]
#     # tag each tokenized sentence with nltk.pos_tag()
#     tagged = [nltk.pos_tag(sent) for sent in sentences_tokens]
#     # remove stopwords, etc. Lemmatize nouns
#     lemmas = [
#         wnl.lemmatize(w) for sent in tagged for (w, tag) in sent
#         if (tag == 'NN'
#             and w not in stopwords
#             and not w.startswith("'")
#             and len(wnl.lemmatize(w)) > 1)
#     ]
#     return lemmas


headings: list[str] = []
docs: list[str] = []
for news in root.iter('news'):
    headings.append(news.find("value[@name='head']").text)
    docs.append(news.find("value[@name='text']").text)

tfidf: TfidfVectorizer = TfidfVectorizer(tokenizer=tokenizer)
tfidf_vectors: csr_matrix = tfidf.fit_transform(docs)
features_idx: dict[int, str] = dict(enumerate(tfidf.get_feature_names_out()))

for doc_idx, score in enumerate(tfidf_vectors):
    words: list[tuple[float, str]] = sorted([
        (scr, features_idx[idx])
        for idx, scr in
        zip(score.indices, score.data)
    ], reverse=True)[:WORDS_LIMIT]
    print(headings[doc_idx] + ':')
    print(*[w for _, w in words])
    print()
