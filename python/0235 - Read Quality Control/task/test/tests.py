from hstest import *
import re


class BestArchive(StageTest):

    def common_test(self, *files, **point_values):
        reply = None
        program = TestedProgram()
        program.start()

        if not program.is_waiting_input():
            raise WrongAnswer("You program should input the path to the file")

        for data in files:
            reply = program.execute(data)

        # if the reply is empty
        if not reply:
            raise WrongAnswer("You gave an empty answer")
        reply_low = reply.replace(" ", "").lower()

        # dict of correct points
        point2value_correct = {}
        for param_name, value in point_values.items():
            point2value_correct[param_name] = value

        # if each point presents only once
        def check_format(line, substring):
            substring_low = substring.replace(" ", "").lower()
            if line.count(substring_low) != 1:
                raise WrongAnswer(f"Substring \"{substring}\" should occur once in the output.\n"
                                  f"Found {line.count(substring_low)} occurrence(s).\n"
                                  f"Check the output format in the Examples section.\n"
                                  f"Make sure there is no typos in the output of your program.")

        # check values
        def check_number(total_reply, substring, correct_number):
            float_lines = ["gccontentaverage=", "nsperreadsequence="]
            substring_low = substring.replace(" ", "").lower()
            pattern = f"{substring_low}([0-9]+)"

            if substring_low in float_lines:
                pattern = pattern[:-1] + "\.[0-9]+)"
            number_search = re.search(pattern=pattern, string=total_reply)

            if number_search is None:
                raise WrongAnswer(f"Didn't find numerical answer in the \"{substring}\" line. Please, check if the answer format is correct")
            number = float(number_search.group(1))
            if number != correct_number:
                raise WrongAnswer(f"The value of \"{substring}\" is incorrect")

        # dict of points for checking + correct values
        substr2point = {"Reads in the file =": 'AMOUNT',
                        "Reads sequence average length =": 'AVERAGE',
                        "Repeats =": 'REPEATS',
                        "GC content average =": 'GC',
                        "Reads with Ns =": 'READSN',
                        "Ns per read sequence =": 'NSPER'}

        # run checking!
        for substr in substr2point.keys():
            check_format(reply_low, substr)
        for substr, point in substr2point.items():
            check_number(reply_low, substr, point2value_correct[point])
        return CheckResult.correct()

    @dynamic_test
    def test1(self):
        return self.common_test("test/data1.gz", "test/data2.gz", "test/data3.gz",
                                AMOUNT=10, AVERAGE=100, REPEATS=0,
                                READSN=10, GC=41.4, NSPER=22.0)


if __name__ == '__main__':
    BestArchive().run_tests()
