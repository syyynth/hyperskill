import numpy
import pandas
from hstest import PlottingTest, WrongAnswer, dynamic_test, TestedProgram, CheckResult

data_CORRECT = {
    "categories": ['Chemistry', 'Economics', 'Literature', 'Peace',
                   'Physics', 'Physiology or Medicine', 'All categories'],
}


class Box(PlottingTest):
    # hs-test-python is not able to test box plots properly yet
    # so for now this test program checks whether user showed one plot and whether its type == "box"

    @dynamic_test
    def test(self):
        pr = TestedProgram()
        pr.start()

        all_figures = self.all_figures()

        if len(all_figures) == 0:
            raise WrongAnswer("Looks like you didn't present any plots")
        if len(all_figures) != 1:
            raise WrongAnswer(f"Expected one box plot of age distribution across Nobel prize categories.\n"
                              f"Found {len(all_figures)} plots.")

        graph_type = all_figures[0].type
        if graph_type != "box":
            raise WrongAnswer(f"The type of the plot is wrong.\n"
                              f"The box plot is expected, found {graph_type} plot.")

        if all_figures[0].kwargs.get('labels') is None:
            raise WrongAnswer("Please define labels!")
        try:
            if not set(all_figures[0].kwargs.get("labels")) == set(data_CORRECT['categories']):
                raise WrongAnswer(
                    f"The labels for the 'categories' are wrong. They should be '{data_CORRECT['categories']}'!")
        except TypeError:
            raise WrongAnswer("The labels type is not hashable.")

        if not all_figures[0].kwargs.get("showmeans"):
            raise WrongAnswer("The 'showmeans' parameter is not defined or wrong!")

        return CheckResult.correct()


if __name__ == '__main__':
    Box().run_tests()
