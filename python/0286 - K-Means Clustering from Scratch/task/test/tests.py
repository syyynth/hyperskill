from hstest import StageTest, TestCase, CheckResult
from hstest.stage_test import List
from utils.utils import full_check, get_list

# The source data I will test on
true_data = [1, 1, 2, 1, 0, 1, 0, 2, 0, 2, 1, 2, 1, 2, 1, 0, 0, 0, 1, 0]


class Tests6(StageTest):

    def generate(self) -> List[TestCase]:
        return [TestCase(time_limit=1000000)]

    def check(self, reply: str, attach):
        reply = reply.strip().lower()

        if len(reply) == 0:
            return CheckResult.wrong("No output was printed!")

        if reply.count('[') != 1 or reply.count(']') != 1:
            return CheckResult.wrong('No expected list was found in output!')

        # Getting the student's results from the reply

        try:
            student, _ = get_list(reply)
        except Exception:
            return CheckResult.wrong('Seems that data output is in wrong format!')

        error = 'Incorrect cluster labels.'
        check_result = full_check(student, true_data, '', tolerance=0, error_str=error)
        if check_result:
            return check_result

        return CheckResult.correct()


if __name__ == '__main__':
    Tests6().run_tests()
