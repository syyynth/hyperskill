from hstest import StageTest, TestCase, CheckResult

PATH = 'SAR14.txt'


class PrepareDataForML(StageTest):

    def generate(self):
        return [TestCase(stdin=PATH, time_limit=900000, attach=[0.18])]

    def check(self, rep, attach):
        if len(rep.splitlines()) != 3:
            return CheckResult.wrong('Make sure you provided the answer for all three questions.')
        elif 'SGDClassifier' not in rep.splitlines()[0]:
            return CheckResult.wrong('The answer to the 1st question is wrong.')
        elif 'negative' not in rep.splitlines()[1].lower():
            return CheckResult.wrong('The answer to the 2nd question is wrong.')
        elif attach[0] > float(rep.splitlines()[2].split()[-1]):
            return CheckResult.wrong('The answer to the 3rd question is wrong.')

        return CheckResult.correct()


if __name__ == '__main__':
    PrepareDataForML().run_tests()
