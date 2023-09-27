from hstest.stage_test import *
from hstest.test_case import TestCase


class CalcTest(StageTest):
    on_exit = False

    def generate(self) -> List[TestCase]:
        return [TestCase(stdin=['/help', self.test_1_1, self.test_1_2, self.test_1_3, self.test_1_4, self.test_1_5,
                                self.test_1_6, self.test_1_7, self.test_1_9, self.test_1_10, self.test_1_11,
                                self.test_1_12, self.test_1_13]),
                TestCase(stdin=['variable = 777 \n Variable', self.test_2_1,
                                self.test_2_2, self.test_2_3, self.test_2_4]),
                TestCase(stdin=['8 * (2 + 3', self.test_3_1, self.test_3_2, self.test_3_3, self.test_3_4]),
                TestCase(stdin=['14       -   12', self.test_4_1, self.test_4_2])]

    # test of previous steps' functionality ####################################
    # help message test
    def test_1_1(self, output):
        output = str(output).lower().strip()
        if len(output.split(" ")) < 1:
            return CheckResult.wrong("It seems like there was no any \"help\" message.")
        return ""

    # empty string test
    def test_1_2(self, output):
        output = str(output)
        if len(output) != 0:
            return CheckResult.wrong("Incorrect response to an empty string. "
                                     "The program should not print anything.")
        return "n = 32"

    # assignment test
    def test_1_3(self, output):
        if len(output) != 0:
            return CheckResult.wrong("Unexpected reaction after assignment." +
                                     "The program should not print anything in this case.")
        return "33 + 20 + 11 + 49 - 32 - 9 + 1 - 80 + 4"

    # addition and subtraction test
    def test_1_4(self, output):
        output = str(output).lower().strip()
        if output != "-3":
            return CheckResult.wrong("The program cannot process addition and subtraction operations correctly.")
        return "33 + 20 + 11 + 49 - n - 9 + 1 - 80 + 4"

    # addition and subtraction with variables
    def test_1_5(self, output):
        output = str(output).lower().strip()
        if output != "-3":
            return CheckResult.wrong("The program cannot process addition and subtraction operations correctly.")
        return "c = n \nc = 2"

    # assignment by a variable and reassignment
    def test_1_6(self, output):
        if len(output) != 0:
            return CheckResult.wrong("Unexpected reaction after assignment."
                                     "The program should not print anything in this case.")
        return "  c   "

    # checking the value of variable
    def test_1_7(self, output):
        output = str(output).lower().strip()
        if output != "2":
            return CheckResult.wrong("The variable stores not a correct value."
                                     "May be the program could not assign the value of one variable to another one.")
        return "11 - 13 + c"

    # def test_8(self, output):
    #     output = str(output).lower().strip()
    #     if output != "0":
    #         return CheckResult.wrong("The problem when sum is equal to 0 has occurred.")
    #     return "5 --- 2 ++++++ 4 -- 2 ---- 1"  output = 10
    # multiple operations with several operators

    # zero sum test
    def test_1_9(self, output):
        output = str(output).lower().strip()
        if output != "0":
            return CheckResult.wrong("The program cannot process multiple operations with several operators.")
        return "/start"

    # nonexistent command
    def test_1_10(self, output):
        output = str(output).lower().strip()
        if "unknown" not in output:
            return CheckResult.wrong("The program should print \"Unknown command\" "
                                     "when a nonexistent command is entered.")
        return "var1 = 1"

    # invalid name of variable
    def test_1_11(self, output):
        output = str(output).lower().strip()
        if "invalid" not in output:
            return CheckResult.wrong("The value can be an integer number or a value of another variable")
        return "c = 7 - 1 = 5"

    # invalid assignment
    def test_1_12(self, output):
        output = str(output).lower().strip()
        if "invalid" not in output:
            return CheckResult.wrong("The program could not handle a invalid assignment.")
        return "variable = f"

    # assignment by unassigned variable
    def test_1_13(self, output):
        output = str(output).lower().strip()
        if "unknown" not in output and "invalid" not in output:
            return CheckResult.wrong("The program should not allow an assignment by unassigned variable.")
        self.on_exit = True
        return "/exit"

    # a test suit for the current stage ########################################
    # test of case sensitivity
    def test_2_1(self, output):
        output = str(output).lower().strip()
        if "unknown" not in output:
            return CheckResult.wrong("The program should be case sensitive.")
        return "4 * 3"

    # multiplication operation test
    def test_2_2(self, output):
        output = str(output).lower().strip()
        if output != "12":
            return CheckResult.wrong("The program has problems with multiplication operation.")
        return "91 / 13"

    # division operation test
    def test_2_3(self, output):
        output = str(output).lower().strip()
        if output != "7" and output != "7.0":
            return CheckResult.wrong("The program has problems with division operation.")
        return " a = 7 \n b = 2\na * 4 / b - (3 - 1)"

    # mixed operations
    def test_2_4(self, output):
        output = str(output).lower().strip()
        if output != "12":
            return CheckResult.wrong("The program cannot correctly process several operations.")
        self.on_exit = 1
        return "/exit"

    # test of an example from the task
    # def test_2_5(self, output):
    #     output = str(output).lower().strip()
    #     if output != "155":
    #         return CheckResult.wrong("The program cannot reproduce an example from the task.")
    #     return "3 + (9 + ( 68 * 3/9)) * ((7-2 * 5) / 2) * 6"
    #     output: -282 input: "7 + 3 * ((4 + 3) * 7 + 1) - 6 / (2 + 1)"

    # test of multi-level parentheses
    # def test_2_6(self, output):
    #     output = str(output).replace(".", " ").split()[0].strip()
    #     if output != "-282":
    #         return CheckResult.wrong("Program incorrectly solves expressions with multi-level parentheses")
    #     self.on_exit = True
    #     return "/exit"

    # negative tests for this stage ############################################
    # unclosed brackets from the right
    def test_3_1(self, output):
        output = str(output).lower().strip()
        if "invalid" not in output:
            return CheckResult.wrong("The program could not handle an invalid expression.")
        return "4 + 5)"

    # unclosed brackets from the left
    def test_3_2(self, output):
        output = str(output).lower().strip()
        if "invalid" not in output:
            return CheckResult.wrong("The program could not handle an invalid expression.")
        return "2 ************ 2"

    # sequence of "*"
    def test_3_3(self, output):
        output = str(output).lower().strip()
        if "invalid" not in output:
            return CheckResult.wrong("A sequence of \"*\" should return \"Invalid expression\".")
        return "2 // 2"

    # sequence of "/"
    def test_3_4(self, output):
        output = str(output).lower().strip()
        if "invalid" not in output:
            return CheckResult.wrong("A sequence of \"/\" should return \"Invalid expression\".")
        self.on_exit = True
        return "/exit"

    # test input with lots of spaces
    def test_4_1(self, output):
        output = str(output).lower().strip()
        if output != "2":
            return CheckResult.wrong("The program cannot process several spaces in the operation.")
        return "5  +  2"

    # test with additional spaces
    def test_4_2(self, output):
        output = str(output).lower().strip()
        if output != "7":
            return CheckResult.wrong("The program cannot process several spaces in the operation.")
        self.on_exit = True
        return "/exit"

    def check(self, reply: str, attach) -> CheckResult:
        if self.on_exit:
            reply = reply.strip().lower().split('\n')
            self.on_exit = False
            if 'bye' not in reply[-1]:
                return CheckResult.wrong("Your program didn't print \"bye\" after entering \"/exit\".")
            else:
                return CheckResult.correct()
        else:
            return CheckResult.wrong("The program ended prematurely")


if __name__ == '__main__':
    CalcTest("calculator.calculator").run_tests()
