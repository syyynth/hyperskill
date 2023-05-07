import re
from hstest import StageTest, CheckResult, TestedProgram, dynamic_test
from .file_content import news_text, h_answers, tfidf_modified_answers


class TextSummarization(StageTest):

    @dynamic_test
    def test1(self):
        main = TestedProgram()
        output = main.start().splitlines()
        while '' in output:
            output.remove('')
        if len(output) < 48:
            return CheckResult.wrong('Your program printed less lines than expected.\n'
                                     'Please, make sure you printed all the headers and summaries and '
                                     'each sentence in the summary is on a new line.')
        elif len(output) > 48:
            return CheckResult.wrong('Your program printed more lines than expected.\n'
                                     'Make sure you followed the template given in the Examples section.')
        return CheckResult.correct()

    @dynamic_test
    def test2(self):
        main = TestedProgram()
        output = main.start()
        if not re.findall('HEADER:', output):
            return CheckResult.wrong("Each header should start with the 'HEADER' field.")
        elif not re.findall('TEXT:', output):
            return CheckResult.wrong("Each summary should start with the 'TEXT' field.")

        if len(re.findall('HEADER:', output)) != len(re.findall('TEXT:', output)):
            return CheckResult.wrong('The number of headers should correspond to the number of summaries')
        elif len(re.findall('HEADER:', output)) != 10:
            return CheckResult.wrong('Your program should print 10 headers')
        return CheckResult.correct()

    @dynamic_test
    def test3(self):
        main = TestedProgram()
        output = main.start().splitlines()
        headers = [header for header in output if header.startswith('HEADER:')]
        for standard, header in zip(h_answers, headers):
            if standard != header.strip():
                return CheckResult.wrong("Incorrect header is found in your program's output. "
                                         f"The following header is incorrect:\n{header}")

        texts = [header.replace('TEXT: ', '') for header in output
                 if not header.startswith('HEADER:') and not header == '']
        average_texts = [text.strip() for text in texts if texts.index(text) not in range(23, 31)]
        fluctuate_texts = [text.strip() for text in texts if texts.index(text) in range(23, 31)]
        obl_texts = ['Net income rose 19% to $8.8bn.',
                     'Stifel has raised its price target for Microsoft to $150 from $130.',
                     'Tears and everything.',
                     'X Factor, watch out.',
                     'This is not the first time Siri has taken to the mic though.']

        for standard, text in zip(tfidf_modified_answers, average_texts):
            if standard != text.strip():
                return CheckResult.wrong("Incorrect sentence is found in the summary. "
                                         f"The following sentence is incorrect:\n{text}")
        if not all(sentence in fluctuate_texts for sentence in obl_texts[:2]):
            wrong_sents = list(set(obl_texts) - set(fluctuate_texts))
            return CheckResult.wrong(f"The following sentence should be included in the 7th summary:\n{wrong_sents[0]}")
        elif not all(sentence in fluctuate_texts for sentence in obl_texts[2:]):
            wrong_sents = list(set(obl_texts) - set(fluctuate_texts))
            return CheckResult.wrong(f"The following sentence should be included in the 8th summary:\n{wrong_sents[0]}")
        return CheckResult.correct()


if __name__ == '__main__':
    with open('news.xml', 'w', encoding='utf-8') as f:
        f.write(news_text)
    TextSummarization().run_tests()
