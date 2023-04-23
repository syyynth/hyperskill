from typing import List, Any
from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.check_result import CheckResult
from hstest import WrongAnswer
import requests, json


class TestStage6(StageTest):

    def generate(self) -> List[TestCase]:
        inputs = [['usd', 'eur', '20', 'nok', '45', 'sek', '75', 'nok', '55', 'isk', '91', ''],
                  ['rub', 'jpy', '80', 'jpy', '95', ''],
                  ['ils', 'usd', '45', 'rsd', '57', 'eur', '33', ''],
                  ['cad', 'dkk', '15', 'gel', '35', 'mkd', '41', '']]

        list_tests = [
            TestCase(stdin=inputs[0], attach=[['EUR', 'is in the cache'], ['NOK', 'is not in the cache'],
                                              ['SEK', 'is not in the cache'], ['NOK', 'is in the cache'],
                                              ['ISK', 'is not in the cache']]),
            TestCase(stdin=inputs[1], attach=[['JPY', 'is not in the cache'], ['JPY', 'is in the cache']]),
            TestCase(stdin=inputs[2], attach=[['USD', 'is in the cache'], ['RSD', 'is not in the cache'],
                                              ['EUR', 'is in the cache']]),
            TestCase(stdin=inputs[3], attach=[['DKK', 'is not in the cache'], ['GEL', 'is not in the cache'],
                                              ['MKD', 'is not in the cache']])
        ]

        for i, test in enumerate(list_tests):
            try:
                zapros = requests.get(f"http://www.floatrates.com/daily/{inputs[i][0]}.json").text
            except TimeoutError:
                raise WrongAnswer("Check your internet connection.")
            except requests.exceptions.ConnectionError:
                raise WrongAnswer("Make sure that your Internet connection is fine, the URL "
                                  "is correct and floatrates.com is not down")

            n = 0
            for j in range(1, len(inputs[i]) - 1, 2):
                try:
                    rate = json.loads(zapros)[inputs[i][j]]['rate']
                except json.decoder.JSONDecodeError:
                    raise WrongAnswer("JSONDecodeError occurred when tests tried to get the data from FloatRates. \n"
                                      "Please, try running tests again.")
                test.attach[n].append(round(float(inputs[i][j + 1]) * float(rate), 2))
                n += 1

        return list_tests

    def check(self, reply: str, attach) -> CheckResult:
        reply = reply.replace('…', '...')
        repl_parsed = [i.strip() for i in reply.split('Checking the cache...') if i]
        if len(repl_parsed) != len(attach):
            return CheckResult.wrong("""
            Make sure your output is well-formatted and your program didn't stop after the first input.
            The program should process user input until there is no currency left to process.
            """)
        for i, curr in enumerate(repl_parsed):
            curr_split = curr.split('\n')
            if len(curr_split) != 2:
                return CheckResult.wrong("Make sure you output exactly three lines after each set of inputs.\n")
            curr0, curr1 = curr_split
            if attach[i][1] not in curr0:
                cur_cur = curr1.split()[-1][:-1]
                if cur_cur.lower() not in ("eur", "usd"):
                    return CheckResult.wrong(f"Check the data in your cache. It seems that {cur_cur} not in the "
                                             "cache though it should already be.")
                else:
                    return CheckResult.wrong(f"It seems that {cur_cur} not in the cache. Please, make sure you added "
                                             "the USD and EUR rates in the cache at the beginning of your program.")
            try:
                amount = float(curr1.split()[-2])
            except ValueError:
                return CheckResult.wrong("Your output is incorrectly formatted.")
            except IndexError:
                return CheckResult.wrong("The output of your program seems to be incorrectly formatted.\n"
                                         "Make sure you output the result in the format:\n"
                                         "\"You received {value} {currency}.\"")
            if abs(amount - attach[i][2]) > 0.2:
                return CheckResult.wrong(f"The amount of {attach[i][0]} is wrong")
        return CheckResult.correct()


if __name__ == '__main__':
    TestStage6("cconverter.cconverter").run_tests()
