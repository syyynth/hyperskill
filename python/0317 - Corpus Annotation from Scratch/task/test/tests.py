import os
from hstest import StageTest, TestedProgram, CheckResult, dynamic_test


class CorpusAnnotationTest(StageTest):

    @dynamic_test(time_limit=90000)
    def test_clockwork_orange(self):
        pr = TestedProgram()
        pr.start()
        output = pr.execute(f'test{os.sep}clockwork_orange.txt').lower().strip()
        if not output:
            return CheckResult.wrong("Your program didn't print any output.")

        output_list = list(filter(None, output.splitlines()))
        if len(output_list) < 7:
            return CheckResult.wrong("Your program printed less lines than expected.\n"
                                     "In this stage, you need to print the corpus statistics.")
        elif len(output_list) > 7:
            return CheckResult.wrong("Your program printed more lines than expected.\n"
                                     "In this stage, you need to print the corpus statistics.")

        for line in output_list:
            if "multi" in line and "named" in line and "entities" in line:
                if not line[-3:].isdigit():
                    return CheckResult.wrong("Can't parse the number of multi-word named entities.\n"
                                             "Make sure the answer format is the same as in the example.")
                expected = 120
                actual = int(line[-3:])
                if abs(actual - expected) > 10:
                    return CheckResult.wrong("Incorrect number of multi-word entities.")

            if "lemma" in line and "devotchka" in line:
                if not line[-2:].isdigit():
                    return CheckResult.wrong("Can't parse the number of lemmas 'devotchka'.\n"
                                             "Make sure the answer format is the same as in the example.")
                expected = 15
                actual = int(line[-2:])
                if abs(actual - expected) > 3:
                    return CheckResult.wrong("Incorrect number of lemmas 'devotchka'.")

            if "tokens" in line and "stem" in line and "milk" in line:
                if not line[-1:].isdigit():
                    return CheckResult.wrong("Can't parse the number of tokens with the stem 'milk'.\n"
                                             "Make sure the answer format is the same as in the example.")
                expected = 8
                actual = int(line[-2:])
                if abs(actual - expected) > 3:
                    return CheckResult.wrong("Incorrect number of tokens with the stem 'milk'.")

            if "frequent" in line and "entity" in line and "type" in line:
                if 'person' not in output:
                    return CheckResult.wrong("Incorrect most frequent named entity type.")

            if "frequent" in line and "entity" in line and "token" in line:
                if 'one' not in output and 'dim' not in output:
                    return CheckResult.wrong("Incorrect most frequent named entity token.")
                elif 'cardinal' not in output and 'person' not in output:
                    return CheckResult.wrong("The token should be printed along with its named entity type.")

            if "common" in line and "non-english" in line and "words" in line:
                words = ['horrorshow', 'malenky', 'viddy', 'goloss', 'droog', 'viddie']
                for word in words:
                    if word not in line:
                        return CheckResult.wrong(f"The following word should be "
                                                 f"in a list of most common non-English words: '{word}'")

            if "correlation" in line and "noun" in line:
                try:
                    expected = 0.22
                    actual = float(line[-4:])
                    if abs(actual - expected) > 0.1:
                        return CheckResult.wrong("Incorrect correlation value.")
                except ValueError:
                    return CheckResult.wrong("Can't parse the correlation result.\n"
                                             "Make sure the answer format is the same as in the example.")

        if "multi" not in output:
            return CheckResult.wrong("Can't parse the number of multi-word named entities.\n"
                                     "Please format the answer as shown in the examples.")
        elif "devotchka" not in output:
            return CheckResult.wrong("Can't parse the number of lemmas 'devotchka'.\n"
                                     "Please format the answer as shown in the examples.")
        elif "milk" not in output:
            return CheckResult.wrong("Can't parse the number of tokens with the stem 'milk'.\n"
                                     "Please format the answer as shown in the examples")
        elif "type" not in output:
            return CheckResult.wrong("Can't parse the most frequent entity type.\n"
                                     "Please format the answer as shown in the examples.")
        elif "entity token" not in output:
            return CheckResult.wrong("Can't parse the most frequent named entity token.\n"
                                     "Please format the answer as shown in the examples.")
        elif "non-english" not in output:
            return CheckResult.wrong("Can't parse the most common non-English words.\n"
                                     "Please format the answer as shown in the examples.")
        elif "correlation" not in output:
            return CheckResult.wrong("Can't parse the correlation between NOUN and PROPN and named entities.\n"
                                     "Please format the answer as shown in the examples.")

        return CheckResult.correct()


if __name__ == '__main__':
    CorpusAnnotationTest().run_tests()
