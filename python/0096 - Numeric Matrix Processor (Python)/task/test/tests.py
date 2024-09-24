import string
from collections import namedtuple

from hstest.stage_test import *
from hstest.test_case import TestCase

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)

TestClue = namedtuple("TestClue", ["answer", "feedback"])


class CalcTest(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(
                stdin=
                '1\n'
                '3 3\n'
                '3 4 55\n'
                '4 1 1\n'
                '9 0 0\n'
                '3 3\n'
                '4 9 77\n'
                '13 22 44\n'
                '56 57 78\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '7 13 132\n'
                    '17 23 45\n'
                    '65 57 78\n'
                    ,
                    feedback=
                    'Probably, error in the matrix adding algorithm'
                )
            ),
            TestCase(
                stdin=
                '4\n'
                '1\n'
                '3 3\n'
                '1 7 7\n'
                '6 6 4\n'
                '4 2 1\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '1 6 4\n'
                    '7 6 2\n'
                    '7 4 1\n'
                    ,
                    feedback=
                    'Probably, error in the matrix transposition algorithm'
                )
            ),
            TestCase(
                stdin=
                '4\n'
                '1\n'
                '3 3\n'
                '1 7 7\n'
                '6 6 4\n'
                '4 5 1\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '1 6 4\n'
                    '7 6 5\n'
                    '7 4 1\n'
                    ,
                    feedback=
                    'Probably, error in the matrix transposition algorithm'
                )
            ),
            TestCase(
                stdin=
                '4\n'
                '2\n'
                '3 3\n'
                '1 2 4\n'
                '4 6 6\n'
                '7 7 1\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '1 6 4\n'
                    '7 6 2\n'
                    '7 4 1\n'
                    ,
                    feedback=
                    'Probably, error in the matrix transposition algorithm'
                )
            ),
            TestCase(
                stdin=
                '4\n'
                '2\n'
                '3 3\n'
                '1 5 4\n'
                '4 6 6\n'
                '7 7 1.0\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '1 6 4\n'
                    '7 6 5\n'
                    '7 4 1\n'
                    ,
                    feedback=
                    'Probably, error in the matrix transposition algorithm'
                )
            ),
            TestCase(
                stdin=
                '4\n'
                '3\n'
                '4 4\n'
                '6 5 4 2\n'
                '8 7 6 6\n'
                '1 0 0 5.0\n'
                '9 2 8 8\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '2 4 5 6\n'
                    '6 6 7 8\n'
                    '5 0 0 1\n'
                    '8 8 2 9\n'
                    ,
                    feedback=
                    'Probably, error in the matrix transposition algorithm'
                )
            ),
            TestCase(
                stdin=
                '4\n'
                '4\n'
                '4 4\n'
                '8 8 2 9\n'
                '5 0 0 1\n'
                '6 6 7 8.0\n'
                '2 4 5 6\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '2 4 5 6\n'
                    '6 6 7 8\n'
                    '5 0 0 1\n'
                    '8 8 2 9\n'
                    ,
                    feedback=
                    'Probably, error in the matrix transposition algorithm'
                )
            ),
            TestCase(
                stdin=
                '5\n'
                '3 3\n'
                '1 2 3\n'
                '4 5 7\n'
                '10 22 23\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '31\n'
                    ,
                    feedback=
                    'Probably, error in the determinant algorithm'
                )
            ),
            TestCase(
                stdin=
                '5\n'
                '4 4\n'
                '2.65 3.54 3.88 8.99\n'
                '3.12 5.45 7.77 5.56\n'
                '5.31 2.23 2.33 9.81\n'
                '1.67 1.67 1.01 9.99\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '45.2197\n'
                    ,
                    feedback=
                    'Probably, error in the determinant algorithm'
                )
            ),
            TestCase(
                stdin=
                '5\n'
                '1 1\n'
                '17\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '17\n'
                    ,
                    feedback=
                    'Probably, error in the determinant algorithm'
                )
            ),
            TestCase(
                stdin=
                '5\n'
                '2 2\n'
                '5 6\n'
                '17 3\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '-87\n'
                    ,
                    feedback=
                    'Probably, error in the determinant algorithm'
                )
            ),
            TestCase(
                stdin=
                '1\n'
                '4 4\n'
                '-0.3 677.4 435.2 123.33\n'
                '1.3 141.4 0.11 1411.4\n'
                '231.33 113.4 99.9 999.9\n'
                '1002.22 123.44 55.66 13.3\n'
                '4 4\n'
                '43.43 234.22 876.6 13.2\n'
                '-5.5 -0.3 -1.2 10.2\n'
                '-1.0 0.8 0.8 -9.5\n'
                '-45.5 45.5 56.5 13.7\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '43.13 911.62 1311.8 136.53\n'
                    '-4.2 141.1 -1.09 1421.6\n'
                    '230.33 114.2 100.7 990.4\n'
                    '956.72 168.94 112.16 27.0\n'
                    ,
                    feedback=
                    'Probably, error in the matrix adding algorithm'
                )
            ),
            TestCase(
                stdin=
                '5\n'
                '3 3\n'
                '1 7 7\n'
                '6 6 4\n'
                '4 2 1\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '-16\n'
                    ,
                    feedback=
                    'Probably, error in the determinant algorithm'
                )
            ),
            TestCase(
                stdin=
                '5\n'
                '5 5\n'
                '1 2 3 4 5\n'
                '4 5 6 4 3\n'
                '0 0 0 1 5\n'
                '1 3 9 8 7\n'
                '5 8 4 7 11\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '191\n'
                    ,
                    feedback=
                    'Probably, error in the determinant algorithm'
                )
            ),
            TestCase(
                stdin=
                '6\n'
                '3 3\n'
                '2 -1 0\n'
                '0 1 2\n'
                '1 1 0\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '0.33 0 0.33\n'
                    '-0.33 0 0.66\n'
                    '0.16 0.5 -0.33\n'
                    ,
                    feedback=
                    'Probably, error in the matrix inversion algorithm'
                )
            ),
            TestCase(
                stdin=
                '6\n'
                '3 3\n'
                '0.396796 -0.214938 0.276735\n'
                '5.19655 -2.06983 -0.388886\n'
                '-3.3797 1.50219 0.159794\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '1.14717 2.03717 2.9711\n'
                    '2.19055 4.52055 7.20788\n'
                    '3.67009 0.590087 1.33819\n'
                    ,
                    feedback=
                    'Probably, error in the matrix inversion algorithm'
                )
            ),
            TestCase(
                stdin=
                '6\n'
                '4 4\n'
                '2.65 3.54 3.88 8.99\n'
                '3.12 5.45 7.77 5.56\n'
                '5.31 2.23 2.33 9.81\n'
                '1.67 1.67 1.01 9.99\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '0.396796 -0.214938 0.276735 -0.5092\n'
                    '5.19655 -2.06983 -0.388886 -3.14252\n'
                    '-3.3797 1.50219 0.159794 2.04842\n'
                    '-0.593332 0.230065 0.00259267 0.50345\n'
                    ,
                    feedback=
                    'Probably, error in the matrix inversion algorithm'
                )
            ),
            TestCase(
                stdin=
                '2\n'
                '3 3\n'
                '11 234 444\n'
                '456 343 222\n'
                '997 456 456\n'
                '17\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '187 3978 7548\n'
                    '7752 5831 3774\n'
                    '16949 7752 7752\n'
                    ,
                    feedback=
                    'Probably, error in the matrix multiplication algorithm'
                )
            ),
            TestCase(
                stdin=
                '2\n'
                '4 4\n'
                '10123 53455 999345 21312\n'
                '13559 77654 231221 34534\n'
                '12312 23412 342342 525255\n'
                '99713 88123 123123 121111\n'
                '111\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '1123653 5933505 110927295 2365632\n'
                    '1505049 8619594 25665531 3833274\n'
                    '1366632 2598732 37999962 58303305\n'
                    '11068143 9781653 13666653 13443321\n'
                    ,
                    feedback=
                    'Probably, error in the multiplication matrix on constant algorithm'
                )
            ),
            TestCase(
                stdin=
                '3\n'
                '4 4\n'
                '1 2 2 7\n'
                '3 3 4 5\n'
                '5 0 0 1\n'
                '0 1 0 8\n'
                '4 4\n'
                '9 8 7 13\n'
                '15 14 0 1\n'
                '3 7 2 3\n'
                '0 9 0 35\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '45 113 11 266\n'
                    '84 139 29 229\n'
                    '45 49 35 100\n'
                    '15 86 0 281\n'
                    ,
                    feedback=
                    'Probably, error in the matrix multiplication algorithm'
                )
            ),
            TestCase(
                stdin=
                '3\n'
                '2 3\n'
                '1 0 17\n'
                '15 19 7\n'
                '3 4\n'
                '5 6 78 9\n'
                '29 31 47 1\n'
                '14 17 0 3\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '243 295 78 60\n'
                    '724 798 2063 175\n'
                    ,
                    feedback=
                    'Probably, error in the matrix multiplication algorithm'
                )
            ),
            TestCase(
                stdin=
                '3\n'
                '3 5\n'
                '1 4 5 6 6\n'
                '7 8 9 0 0\n'
                '4 1 2 2 2\n'
                '5 2\n'
                '4 5\n'
                '6 1\n'
                '6 0\n'
                '0 9\n'
                '7 7\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '100 105\n'
                    '130 43\n'
                    '48 53\n'
                    ,
                    feedback=
                    'Probably, error in the matrix multiplication algorithm'
                )
            ),
            TestCase(
                stdin=
                '3\n'
                '4 4\n'
                '0.65 0.67 76.4 23.2\n'
                '-0.7 -13.1 -7.2 9.2\n'
                '-0.7 -5.5 -1.5 0.4\n'
                '-1.0 12.6 0.8 -0.4\n'
                '4 4\n'
                '-5.5 -0.3 -1.2 10.2\n'
                '-1.0 0.8 0.8 -9.5\n'
                '-45.5 45.5 56.5 13.7\n'
                '-10.7 11.9 2.2 1.2\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '-3728.685 3752.621 4367.396 1074.785\n'
                    '246.11 -228.39 -396.2 29.71\n'
                    '73.32 -67.679 -87.43 25.04\n'
                    '-39.22 42.02 55.6 -119.42\n'
                    ,
                    feedback=
                    'Probably, error in the matrix multiplication algorithm'
                )
            ),
            TestCase(
                stdin=
                '3\n'
                '4 4\n'
                '0.65 0.67 76.4 23.2\n'
                '-0.7 -13.1 -7.2 9.2\n'
                '-0.7 -5.5 -1.5 0.4\n'
                '-1.0 12.6 0.8 -0.4\n'
                '4 4\n'
                '-5.5 -0.3 -1.2 10.2\n'
                '-1.0 0.8 0.8 -9.5\n'
                '-45.5 45.5 56.5 13.7\n'
                '-10.7 11.9 2.2 1.2\n'
                '3\n'
                '3 5\n'
                '1 4 5 6 6\n'
                '7 8 9 0 0\n'
                '4 1 2 2 2\n'
                '5 2\n'
                '4 5\n'
                '6 1\n'
                '6 0\n'
                '0 9\n'
                '7 7\n'
                '0\n'
                ,
                attach=TestClue(
                    answer=
                    '-3728.685 3752.621 4367.396 1074.785\n'
                    '246.11 -228.39 -396.2 29.71\n'
                    '73.32 -67.679 -87.43 25.04\n'
                    '-39.22 42.02 55.6 -119.42\n'
                    '100 105\n'
                    '130 43\n'
                    '48 53\n'
                    ,
                    feedback=
                    'Probably, error in the operations loop'
                )
            ),
        ]

    def is_equal_matrices(self, actual: list, expected: list) -> bool:
        if len(actual) != len(expected):
            raise WrongAnswer("Make sure that the output format is the same as in the Examples section.\n"
                              "Your output should include only numbers.")
        for actual_line, expected_line in zip(actual, expected):
            if len(actual_line) != len(expected_line):
                raise WrongAnswer("Make sure that the output format is the same as in the Examples section.\n"
                                  "Your output should include only numbers.")
            else:
                for actual, expected in zip(actual_line, expected_line):
                    try:
                        if abs(float(actual) - float(expected)) > 0.1:
                            return False
                    except ValueError:
                        raise WrongAnswer("Looks like your matrix contains not only numbers!")
        return True

    def check(self, reply: str, attach) -> CheckResult:
        characters = set(string.ascii_lowercase)
        actual = [line.split() for line in reply.splitlines() if line and characters.isdisjoint(line)]
        expected = list(map(str.split, str(attach.answer).strip().split("\n")))
        return CheckResult(self.is_equal_matrices(expected, actual), attach.feedback)


if __name__ == '__main__':
    CalcTest("processor.processor").run_tests()
