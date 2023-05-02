import numpy
import pandas
import spacy
from nltk.corpus import words
from scipy.stats import pearsonr
from spacy.tokens.token import Token

with open(input(), encoding='U8') as f:
    corpus = f.read()

nlp = spacy.load('en_core_web_sm')
doc = nlp(corpus)


def is_valid(token: Token) -> bool:
    invalid_chars = {'>', '\\', '*', '<', '/', '_'}
    return (token.pos_ != 'SPACE'
            and not any(c in invalid_chars for c in token.text))


headings = ['token', 'lemma', 'POS', 'entity_type', 'IOB']
tokens = numpy.vstack([
    (token.text, token.lemma_, token.pos_, token.ent_type_, token.ent_iob_)
    for token in doc
    if is_valid(token)
])
df = pandas.DataFrame(tokens, columns=headings)

num_multiword_entities = len([w for w in doc.ents if len(w) > 1])
num_devotchka_lemmas = df.query('lemma == "devotchka"').shape[0]
num_milk_stem_tokens = df.query('lemma == "milk"').shape[0]
freq_entity_type = df.entity_type.value_counts().index[1]
freq_entity_token = df.query('entity_type != ""').token.value_counts().index[0]
english_words = words.words()
valid_pos_tags = {'ADJ', 'ADV', 'NOUN', 'VERB'}
non_english_query = 'lemma not in @english_words and POS in @valid_pos_tags and lemma.str.len() > 4'
top_non_english_tokens = df.query(non_english_query).value_counts('token').head(10).to_dict()
noun_or_propn = df.POS.isin(['NOUN', 'PROPN'])
num_ner = df['entity_type'].str.len() != 0
correlation, pvalue = pearsonr(noun_or_propn, num_ner)

ans = f"""
Number of multi-word named entities: {num_multiword_entities}
Number of lemmas 'devotchka': {num_devotchka_lemmas}
Number of tokens with the stem 'milk': {num_milk_stem_tokens}
Most frequent entity type: {freq_entity_type}
Most frequent named entity token: {freq_entity_token}
Most common non-English words: {top_non_english_tokens}
Correlation between NOUN and PROPN and named entities: {correlation:.2f}
"""
print(ans)
