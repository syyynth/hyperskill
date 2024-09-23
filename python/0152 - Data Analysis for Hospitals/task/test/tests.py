import re
from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.check_result import CheckResult


class EDATest(StageTest):
    def __init__(self, method: str):
        super().__init__(method)

        self.figures = []

        import matplotlib
        import matplotlib.pyplot as plt
        from matplotlib._pylab_helpers import Gcf
        matplotlib.use("agg")

        def custom_show_func(*args, **kwargs):
            managers = Gcf.get_all_fig_managers()
            for m in managers:
                self.figures.append(m.canvas.figure)
                Gcf.destroy(m.num)

        plt.show = custom_show_func

    def generate(self):
        return [
            TestCase()
        ]

    def check(self, reply, attach):
        if len(self.figures) == 0:
            return CheckResult.wrong(
                'Looks like you didn\'t present plots using "plt.show()" command')

        if len(self.figures) != 3:
            return CheckResult.wrong(
                'Looks like you didn\'t build all three plots using "plt.show()" command')

        lines = [line for line in reply.split('\n') if len(line) > 0]
        if len(lines) != 3:
            return CheckResult.wrong(
                'You should output exactly 3 lines with answer to each question in each line. '
                f'Found {len(lines)} lines')

        if 'answer' not in lines[0].lower() or 'question:' not in lines[0].lower()\
                or 'answer' not in lines[1].lower() or 'question:' not in lines[1].lower():
            return CheckResult.wrong(
                'Please follow the format of the answers given in the Example section')

        # 1st question
        answer_reply_str = lines[0].split('question:')[1]
        answer_reply_nums = re.findall(r'\d*\.\d+|\d+', answer_reply_str)
        if len(answer_reply_nums) != 2:
            return CheckResult.wrong(
                'The answer to 1st question is incorrect. You should choose one of the age ranges given in the question')
        answer_reply_nums = list(map(float, answer_reply_nums))
        if len(set([15, 35]) & set(answer_reply_nums)) != 2:
            return CheckResult.wrong(
                'The answer to the 1st question is incorrect')
        # 2nd question
        answer_reply_str = lines[1].split('question:')[1].replace(" ", "")
        if answer_reply_str != 'pregnancy':
            return CheckResult.wrong(f'Found "{answer_reply_str}", which is incorrect answer to the 2nd question')

        return CheckResult.correct()


if __name__ == '__main__':
    EDATest('analysis').run_tests()
