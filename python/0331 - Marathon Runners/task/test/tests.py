import ast
from hstest.stage_test import List
from hstest import *
import re


correct_answer = [[1, 0, 0], [1, 0, 1], [1, 0, 1]]

class PredictTest(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase(time_limit=1000000)]

    def check(self, reply: str, attach):

        reply = reply.strip().replace(" ", "").lower()

        if len(reply) == 0:
            return CheckResult.wrong("No output was printed")

        if len(reply.split('\n')) != 3:
            return CheckResult.wrong('The number of answers supplied does not equal 3')

        if reply.count('[') != 3 or reply.count(']') != 3:
            return CheckResult.wrong('The output should contain three lists in total')


        answer_k1 = re.search(pattern="resultwithk=1:\[.*\]", string=reply)

        if answer_k1 is None:
            raise WrongAnswer(
                "Didn't find the answer for the 'Result with k = 1' case. Please, check if the answer format is correct.")
        list_k1 = answer_k1.group(0).split(':')[1]

        try:
            user_list_k1 = ast.literal_eval(list_k1)

        except Exception as e:
            return CheckResult.wrong(f"Seems that the answer for k = 1 is given in wrong format.\n"
                                     f"Make sure you use only the following Python structures in the output: string, int, float, list, dictionary")

        if not isinstance(user_list_k1, list):
            return CheckResult.wrong(f'The answer for k = 1 should contain a list')

        if len(user_list_k1) != len(correct_answer[0]):
            return CheckResult.wrong(
                f'Output for k = 1 case should contain {len(correct_answer[0])} values, found {len(user_list_k1)}')

        for i in range(len(user_list_k1)):
            if user_list_k1[i] != correct_answer[0][i]:
                return CheckResult.wrong(
                    f"Check element {i} in the answer list for k = 1 case..\n"
                    f"Note that numeration starts from 0.")

        answer_k3 = re.search(pattern="resultwithk=3:\[.*\]", string=reply)

        if answer_k3 is None:
            raise WrongAnswer(
                "Didn't find list answer for the 'Result with k = 3' case. Please, check if the answer format is correct.")
        list_k3 = answer_k3.group(0).split(':')[1]

        try:
            user_list_k3 = ast.literal_eval(list_k3)

        except Exception as e:
            return CheckResult.wrong(f"Seems that the answer for k =3 is given in wrong format.\n"
                                     f"Make sure you use only the following Python structures in the output: string, int, float, list, dictionary")

        if not isinstance(user_list_k3, list):
            return CheckResult.wrong(f'The answer for k = 3 should contain a list')

        if len(user_list_k3) != len(correct_answer[0]):
            return CheckResult.wrong(
                f'Output for k = 3 case should contain {len(correct_answer[1])} values, found {len(user_list_k3)}')

        for i in range(len(user_list_k3)):
            if user_list_k3[i] != correct_answer[1][i]:
                return CheckResult.wrong(
                    f"Check element {i} in the answer list for k = 3 case.\n"
                    f"Note that numeration starts from 0.")

        answer_k5 = re.search(pattern="resultwithk=5:\[.*\]", string=reply)

        if answer_k5 is None:
            raise WrongAnswer(
                "Didn't find the answer for the 'Result with k = 5' case. Please, check if the answer format is correct.")
        list_k5 = answer_k5.group(0).split(':')[1]

        try:
            user_list_k5 = ast.literal_eval(list_k5)

        except Exception as e:
            return CheckResult.wrong(f"Seems that the answer for k = 5 is given in wrong format.\n"
                                     f"Make sure you use only the following Python structures in the output: string, int, float, list, dictionary")

        if not isinstance(user_list_k5, list):
            return CheckResult.wrong(f'The answer for k = 5 should contain a list')

        if len(user_list_k5) != len(correct_answer[0]):
            return CheckResult.wrong(
                f'Output for k = 5 case should contain {len(correct_answer[2])} values, found {len(user_list_k5)}')

        for i in range(len(user_list_k5)):
            if user_list_k5[i] != correct_answer[2][i]:
                return CheckResult.wrong(f"Check element {i} in the answer list for k = 5 case.\n"
                                         f"Note that numeration starts from 0.")

        return CheckResult.correct()


if __name__ == '__main__':
    PredictTest().run_tests()
