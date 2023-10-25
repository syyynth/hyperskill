from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.check_result import CheckResult

PATH = "test/corpus.txt"

def preprocess():
    with open(PATH, "r", encoding="utf-8") as f:
        return f.read().split()


class TextGeneratorTests(StageTest):
    def generate(self):
        return [
            TestCase(stdin=PATH, time_limit=30000),
            TestCase(stdin=PATH, time_limit=30000),
            TestCase(stdin=PATH, time_limit=30000)
        ]

    def check(self, reply, attach):
        punct = {".", "?", "!"}

        try:
            corpus = preprocess()
        except FileNotFoundError:
            return CheckResult.wrong("File not found at {}. Make sure the file "
                                     "has not been deleted or moved.".format(PATH))

        trigrams = {" ".join(corpus[i:i+3]) for i in range(len(corpus)-2)}
        sentences = [sentence for sentence in reply.split('\n') if len(sentence)]

        if len(sentences) != 10:
            return CheckResult.wrong(
                "You should output exactly 10 sentences! Every "
                "sentence should be in a new line.")

        for sentence in sentences:
            sent = sentence.split()
            if len(sent) < 5:
                return CheckResult.wrong(
                    "A pseudo-sentence should not be shorter than 5 tokens.")
            if len(set(sent)) == 1:
                return CheckResult.wrong(
                    "Invalid output. All words of a sentence are identical.")
            if not sent[0][0].isupper():
                return CheckResult.wrong(
                    "Every pseudo-sentence should start with a capitalized word.")
            if sent[0][-1] in punct:
                return CheckResult.wrong(
                    "The first token of a pseudo-sentence should not "
                    "end with sentence-ending punctuation.")
            if sent[-1][-1] not in punct:
                return CheckResult.wrong(
                    "Every pseudo-sentence should end with a "
                    "sentence-ending punctuation mark.")
            for i, token in enumerate(sent):
                if token not in corpus:
                    return CheckResult.wrong(
                        "Sentences should contain only words from the corpus!")
                if token[-1] in punct and 4 < i+1 < len(sent):
                    return CheckResult.wrong(
                        "If a sentence is longer than 5 tokens, it "
                        "should end at the first sentence ending punctuation.")
            for i in range(len(sent)-2):
                trigram = " ".join(sent[i:i+3])
                if trigram not in trigrams:
                    return CheckResult.wrong(
                        "Pseudo-sentences should entirely consist of "
                        "trigrams from the corpus.")
        return CheckResult.correct()


if __name__ == '__main__':
    TextGeneratorTests().run_tests()
