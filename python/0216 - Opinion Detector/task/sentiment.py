import nltk


class SentimentAnalysis:
    def __init__(self):
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r'[a-z_]+')
        self.lemmatizer = nltk.WordNetLemmatizer()
        self.stopwords = nltk.corpus.stopwords.words('english') + ['ie', 'de', 'co', 'un', 'wa']
        self.positive_words = self.read_words('../positive_words.txt')
        self.negative_words = self.read_words('../negative_words.txt')

    @staticmethod
    def read_words(filename):
        with open(filename, encoding='U8') as f:
            return set(f.read().split())

    def preprocess(self, text):
        tokens = self.tokenizer.tokenize(text.lower())
        lemmas = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stopwords]
        return [lemma for lemma in lemmas if lemma not in self.stopwords]

    def classify_review(self, review):
        sentiment_score = (sum(word in self.positive_words for word in review)
                           - sum(word in self.negative_words for word in review))
        return 'Positive' if sentiment_score > 0 else 'Negative'
