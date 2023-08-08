import re

from hstest import StageTest, CheckResult, TestedProgram, dynamic_test


def get_number(string):
    return list(map(float, re.findall(r'-*\d*\.\d+e-\d+|-*\d*\.\d+|-*\d+', string)))


class LinearRegression(StageTest):

    @dynamic_test()
    def test_1(self):
        t = TestedProgram()
        reply = t.start()

        if len(reply) == 0:
            return CheckResult.wrong("No output was printed. Print output in the right format.")

        if '{' not in reply or '}' not in reply or ":" not in reply or "," not in reply:
            return CheckResult.wrong("Print output in dictionary format")

        if 'array' not in reply:
            return CheckResult.wrong("Return coefficient(s) in numpy array")

        if reply.count(',') != 5 or reply.count(':') != 4 or reply.count('}') != reply.count('{'):
            return CheckResult.wrong('The dictionary output is not properly constructed.')

        output = reply.replace("{", "").replace("}", "").lower().split(", '")

        if len(output) != 4:
            return CheckResult.wrong(f"Number of items in dictionary should be 4, {len(output)} present")

        output = [j.replace("'", "") for j in output]
        output1, output2, output3, output4 = output

        name1, answer1 = output1.strip().split(':')
        name2, answer2 = output2.strip().split(':')
        name3, answer3 = output3.strip().split(':')
        name4, answer4 = output4.strip().split(':')

        answers = {
            name1.strip(): answer1, name2.strip(): answer2,
            name3.strip(): answer3, name4.strip(): answer4}

        intercept = answers.get('intercept', '0000000')
        coefficient = answers.get('coefficient', '0000000')
        coefficient = re.sub('array', '', coefficient)
        r2 = answers.get('r2', '0000000')
        rmse = answers.get('rmse', '0000000')

        if intercept == '0000000' or coefficient == '0000000' or len(intercept) == 0 or len(coefficient) == 0:
            return CheckResult.wrong("Print values for both Intercept and Coefficient")

        if r2 == '0000000' or rmse == '0000000' or len(r2) == 0 or len(rmse) == 0:
            return CheckResult.wrong("Print values for both R2 and RMSE")

        intercept = get_number(intercept)
        if len(intercept) != 1:
            return CheckResult.wrong(f"Intercept should contain a single value, found {len(intercept)}")
        intercept = intercept[0]
        if not abs(intercept) < 10 ** (-10):
            return CheckResult.wrong(
                "Wrong value for difference between Intercepts of sklearn LinearRegression and CustomLinearRegression")

        coefficient = get_number(coefficient)
        if len(coefficient) != 3:
            return CheckResult.wrong(f"Coefficient should contain three values, found {len(coefficient)}")
        if not abs(coefficient[0]) < 10 ** (-10):
            return CheckResult.wrong(
                "Wrong value for difference between beta1 of sklearn LinearRegression and beta1 of CustomLinearRegression")
        if not abs(coefficient[1]) < 10 ** (-10):
            return CheckResult.wrong(
                "Wrong value for difference between beta2 of sklearn LinearRegression and beta2 of CustomLinearRegression")
        if not abs(coefficient[2]) < 10 ** (-10):
            return CheckResult.wrong(
                "Wrong value for difference between beta3 of sklearn LinearRegression and beta3 of CustomLinearRegression")

        r2 = get_number(r2)
        if len(r2) != 1:
            return CheckResult.wrong(f"R2 should contain a single value, found {len(r2)}")
        r2 = r2[0]
        if not abs(r2) < 10 ** (-10):
            return CheckResult.wrong("Wrong value for difference between sklearn R2 and custom R2")

        rmse = get_number(rmse)
        if len(rmse) != 1:
            return CheckResult.wrong(f"RMSE should contain a single value, found {len(rmse)}")
        rmse = rmse[0]
        if not abs(rmse) < 10 ** (-10):
            return CheckResult.wrong("Wrong value for difference between sklearn RMSE and custom RMSE.\n"
                                     "Did you take the square root of mean squared error?")

        return CheckResult.correct()


if __name__ == '__main__':
    LinearRegression().run_tests()
