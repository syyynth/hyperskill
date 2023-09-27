import re
from pathlib import Path

import spacy
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_NAME = 'en_core_web_sm'
HIGHLIGHT_FORMAT = '<b>{}</b>'
CORPUS_PATH = './corpus'


class GooglePlusPlus:
    def __init__(self, path: str) -> None:
        self.path = path
        self.vectorizer = TfidfVectorizer()
        self.nlp = spacy.load(MODEL_NAME)
        self.documents = self._load_documents()
        self.tfidf_matrix = self._fit_transform()

    def _load_documents(self) -> dict:
        return {file.name: file.read_text().strip() for file in Path(self.path).iterdir()}

    def _fit_transform(self) -> csr_matrix:
        return self.vectorizer.fit_transform(self.documents.values())

    def calculate_similarity(self, query: str) -> list[tuple[str, float]]:
        vector_query = self.vectorizer.transform([query])
        similarity = cosine_similarity(vector_query, self.tfidf_matrix)[0]

        return sorted(
            ((doc, sim) for doc, sim in zip(self.documents, similarity) if sim),
            key=lambda x: (-x[1], x[0]),
        )

    def display(self, output: list[tuple[str, float]], query: str, limit: int, offset: int) -> None:
        if not output[offset:limit]:
            print('No results were found for your query')
            return

        query_tokens = set(token.text for token in self.nlp(query) if token.text.isalnum())

        for name, sim in output[offset:limit]:
            print(name)
            text = self.documents[name]
            for token in self.nlp(text):
                if token.text.isalnum() and token.text in query_tokens:
                    start = max(0, token.idx - 30)
                    end = token.idx + len(token.text) + 30
                    raw_text = text[start:end - 1]
                    highlight_re = '|'.join(query_tokens)
                    highlighted_text = re.sub(highlight_re, lambda m: HIGHLIGHT_FORMAT.format(m[0]), raw_text)
                    print('...' * (start > 0) + highlighted_text + '...' * (end < len(text)))
                    break


def main() -> None:
    gpp = GooglePlusPlus(CORPUS_PATH)
    while True:
        query = input('Enter your query, please:\n')
        output = gpp.calculate_similarity(query)
        limit = int(input('Enter limit:\n'))
        offset = int(input('Enter offset:\n'))
        gpp.display(output, query, limit, offset)
        if input('Do you want to make another request? (yes/no)\n').lower() == 'no':
            print('Bye!')
            break


if __name__ == '__main__':
    main()
