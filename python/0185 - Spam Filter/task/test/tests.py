from hstest.stage_test import List
from hstest import StageTest, CheckResult, TestCase


class NaiveBayesClassifier(StageTest):

    def generate(self) -> List[TestCase]:
        return [
            TestCase(stdin="", attach=("", ""), time_limit=900000)
        ]

    def check(self, reply: str, attach):

        if "{" not in reply or "}" not in reply:
            return CheckResult.wrong("Output a dictionary")

        df = reply.replace("{", "").replace("}", "").split(",")
        metrics = {}

        for oneVal in df:
            try:
                metric, score = oneVal.strip().split(":")
                metrics[metric.replace("'", "").lower()] = float(score.strip()[:4])
            except ValueError:
                return CheckResult.wrong("Not all the metrics are present "
                                         "or something is wrong with the output format: "
                                         "you need to print only the dictionary")

        if 'accuracy' not in metrics or 'recall' not in metrics or 'precision' not in metrics or 'f1' not in metrics:
            return CheckResult.wrong("Incorrect dictionary key")

        if metrics['accuracy'] < 0.95 or metrics['recall'] < 0.90 or metrics['precision'] < 0.90 or metrics[
            'f1'] < 0.90:
            return CheckResult.wrong("Poor metrics. The scores can be improved upon")

        return CheckResult.correct()


if __name__ == '__main__':
    NaiveBayesClassifier().run_tests()
