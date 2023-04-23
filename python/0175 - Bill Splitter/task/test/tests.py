from hstest.stage_test import *
from hstest.test_case import TestCase
import ast, math

END_RESULT = "No one is going to be lucky"
INVALID_RESULT = "No one is joining for the party"


class BillSplitterTest(StageTest):
    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin=["5", "Marc", "Jem", "Monica", "Anna", "Jason", "100", "Yes"],
                     attach=["5", "100", "Yes", ["Marc", "Jem", "Monica", "Anna", "Jason"]]),
            TestCase(stdin=["3", "Jake", "Sam", "Irina", "109", "No"],
                     attach=["3", "109", "No", ["Jake", "Sam", "Irina"]]),
            TestCase(stdin=["2", "Jake", "Sam", "109", "No"],
                     attach=["2", "109", "No", ["Jake", "Sam"]]),
            TestCase(stdin=["0", "100"], attach=["0", "100"]),
            TestCase(stdin=["-1", "-5"], attach=["-1", "-5"])
        ]

    def check(self, reply: str, attach: Any) -> CheckResult:
        strings = [s for s in reply.split('\n') if s != '']
        if int(attach[0]) <= 0:
            if len(strings) != 2:
                return CheckResult.wrong("Your code is not printing expected number of lines of output")
            elif strings[1] != INVALID_RESULT:
                return CheckResult.wrong("Expected output is - No one is joining for the party")
            return CheckResult.correct()
        elif int(attach[0]) > 0 and len(strings) != 6:
            return CheckResult.wrong("Your code is not printing expected number of lines of output, check examples")
        if (attach[2] == "Yes"):
            lucky_string = strings[4].split(" ")
            name = lucky_string[0]
            if (name not in attach[3]):
                return CheckResult.wrong("Expected output is a random name from dictionary keys")
        elif (attach[2] == "No"):
            if strings[4] != END_RESULT:
                return CheckResult.wrong("Output should be - No one is going to be lucky")
        try:
            output = ast.literal_eval(strings[5])
        except ValueError:
            return CheckResult.wrong("Please check your last output, it should be a dictionary")
        except IndentationError:
            return CheckResult.wrong("There should not be any leading whitespace before your last output")
        except Exception:
            return CheckResult.wrong('Something wrong with your output. '
                                     'Make sure you print the dictionary like in examples!\n'
                                     f'Found dict: \n{strings[5]}')

        if (not isinstance(output, dict)):
            return CheckResult.wrong("Please check, your last output should be a dictionary")
        elif (len(output) != int(attach[0])):
            return CheckResult.wrong(
                "Please check if you have added all your friends to dictionary after taking the user input")
        try:
            bill_list = list(output.values())
            bill = sum(bill_list)
        except TypeError:
            return CheckResult.wrong("Dictionary Values should be of integer type")
        if (attach[2] == "Yes"):
            name = lucky_string[0]

            if name not in output:
                return CheckResult.wrong(f"Can't find '{name}' key in the dictionary!")

            if (len(output) != 0 and output[name] != 0):
                return CheckResult.wrong("Bill value for lucky person should be 0")
            elif (len(output) != 0 and (math.ceil(bill) != float(attach[1]) and math.floor(bill) != float(attach[1]))):
                return CheckResult.wrong("Please update dictionary with correct split values")
            elif (len(output) != 0 and round(int(attach[1]) / (int(attach[0]) - 1), 2) not in bill_list):
                return CheckResult.wrong("Please round off split values to two decimal places")
        else:
            if (len(output) != 0 and (math.ceil(bill) != float(attach[1]) and math.floor(bill) != float(attach[1]))):
                return CheckResult.wrong("Please update dictionary with correct split values")
            elif (len(output) != 0 and bill_list[0] != round(int(attach[1]) / int(attach[0]), 2)):
                return CheckResult.wrong("Please round off split values to two decimal places")

        return CheckResult.correct()


if __name__ == '__main__':
    BillSplitterTest().run_tests()
