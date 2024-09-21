from typing import Optional

from hstest import StageTest, TestedProgram, CheckResult, dynamic_test, WrongAnswer
import os

operations = ["+", "-", "*"]
wrong_format_msg = 'The task should have the following format: "number operation number"\n' \
                   '(e.g. "4 + 2", without quotes).\n' \
                   'However, the following output was found: '
corr_as_incorr_msg = 'The correct answer was given to the equation.\n' \
                     'The app should print \'Right!\'. \n' \
                     'However, this word was not found in the output.'
incorr_as_corr_msg = 'An incorrect answer was given to the equation.\n' \
                     'The app should print \'Wrong!\'. \n' \
                     'However, this word was not found in the output.'
typo_msg = "The app should inform the user that there's a typo in the answer by outputting a message: \'Wrong format\'."
wrong_n_lines = "The number of lines in the output is less than expected.\n" \
                "Please make sure you output the result of the task and the new task on separate lines."


def calc(task: str) -> Optional[int]:
    original_task = task
    task = task.strip()
    op = None
    for i in operations:
        if i in task:
            op = i
            break

    if op is None:
        return None
    try:
        task = task.split(op)
        f = int(task[0].strip())
        s = int(task[1].strip())
    except ValueError:
        return None
    except IndexError:
        raise WrongAnswer(f"The format of the task {original_task} does not follow the required format.\n"
                          f"Please, print two numbers and an operation sign between them.")

    if op == "+":
        ans = f + s
    elif op == "-":
        ans = f - s
    else:
        ans = f * s
    return ans


def check_and_solve_task(task):
    if not any([i in task for i in operations]):
        raise WrongAnswer(wrong_format_msg + task)

    correct_ans = calc(task)

    if correct_ans is None:
        raise WrongAnswer(wrong_format_msg + task)

    return correct_ans


class ExamTest(StageTest):
    @dynamic_test
    def test_level_1(self):

        filepath = 'results.txt'
        file = open(filepath, 'w+')
        file.write("The quick brown fox jumps over a lazy dog\n")
        file = open(filepath, 'r')
        text_from_file = file.read()
        file.close()

        pr = TestedProgram()
        first = pr.start()

        # 1 - ok
        task = pr.execute("1")
        correct_ans = str(check_and_solve_task(task))
        result = pr.execute(correct_ans).strip().lower()
        if "right" not in result:
            raise WrongAnswer(corr_as_incorr_msg + "\nTask: " + task + '\nTested answer: ' + str(correct_ans))

        # 2 - wrong format + ok
        task = result.split('\n')
        if len(task) < 2:
            raise WrongAnswer(wrong_n_lines)
        task = task[1].strip()
        correct_ans = check_and_solve_task(task)

        result = pr.execute("11r").strip().lower()
        if "format" not in result:
            raise WrongAnswer(typo_msg)

        result = pr.execute("").strip().lower()
        if "format" not in result:
            raise WrongAnswer(typo_msg)

        result = pr.execute(str(correct_ans)).strip().lower()
        if "right" not in result:
            raise WrongAnswer(corr_as_incorr_msg + "\nThe task: " + task + '\nThe answer: ' + str(correct_ans))

        # 3 - wrong answer
        task = result.split('\n')
        if len(task) < 2:
            raise WrongAnswer(wrong_n_lines)
        task = task[1].strip()
        incorrect_ans = check_and_solve_task(task) + 3
        result = pr.execute(str(incorrect_ans)).strip().lower()
        if "wrong" not in result:
            raise WrongAnswer(incorr_as_corr_msg + "\nThe task: " + task + '\nThe answer: ' + str(incorrect_ans))

        # 4 - ok
        task = result.split('\n')
        if len(task) < 2:
            raise WrongAnswer(wrong_n_lines)
        task = task[1].strip()
        correct_ans = check_and_solve_task(task)
        result = pr.execute(str(correct_ans)).strip().lower()
        if "right" not in result:
            raise WrongAnswer(corr_as_incorr_msg + "\nThe task: " + task + '\nThe answer: ' + str(correct_ans))

        # 5 - wrong
        task = result.split('\n')
        if len(task) < 2:
            raise WrongAnswer(wrong_n_lines)
        task = task[1].strip()
        incorrect_ans = check_and_solve_task(task) + 3
        result = pr.execute(str(incorrect_ans)).strip().lower()
        if "wrong" not in result:
            raise WrongAnswer(incorr_as_corr_msg + "\nThe task:  " + task + '\nThe answer: ' + str(incorrect_ans))
        final_output = result
        result = result.replace(' ', '')

        if "3/5" in result:
            pass
        elif "/5" in result:
            return CheckResult.wrong("The number of correct answers is calculated incorrectly: \n" + final_output +
                                     "\nShould be \'3/5\'.")
        else:
            return CheckResult.wrong("The final output doesn't contain count of correct answers: " + final_output)

        if "save" not in result:
            return CheckResult.wrong("Your app should ask if the user want to save results in file.")

        result = pr.execute("Yes")
        if "name" not in result.lower():
            return CheckResult.wrong("The app should ask for the user's name.")
        result = pr.execute("Tester")
        if "saved" not in result.lower():
            return CheckResult.wrong("The app should inform the user that the results were saved in the file.")

        if not os.path.exists(filepath):
            return CheckResult.wrong(f"The file {filepath} is not found.")

        file = open(filepath, 'r')
        text_from_file_after_saving = file.read()
        file.close()

        if text_from_file not in text_from_file_after_saving:
            return CheckResult.wrong("Your application shouldn't remove any information from the file with results "
                                     "if it already exists.")

        if all([i in text_from_file_after_saving for i in ["Tester", '3/5', '1', '2', '9']]):
            return CheckResult.correct()
        else:
            return CheckResult.wrong("The application didn't save the result in the needed format.\n"
                                     "The last lines written in the file: \n" +
                                     text_from_file_after_saving.replace(text_from_file, ''))

    @dynamic_test
    def test_level_2_numbers(self):
        start = 11
        finish = 29

        numbers = []

        for i in range(200):
            pr = TestedProgram()
            pr.start()
            task = pr.execute("2")
            try:
                numbers.append(int(task.strip()))
            except ValueError:
                return CheckResult.wrong("Please, make sure that in level 2 your task is about integral squares:\n"
                                         "the task should only contain a single integer in the range from 11 to 29.")

        numbers = set(numbers)
        if numbers == set(range(start, finish + 1)):
            return CheckResult.correct()
        else:
            return CheckResult.wrong(
                'If the user chooses level 2 training, the app should use all numbers from 11 to 29\n'
                'and shouldn\'t use any other numbers.\n'
                'The following numbers were found:\n' + str(numbers) +
                '\nMake sure you use all numbers from 11 to 29. \n'
                'If you are sure that your program works correctly, re-run the tests.')

    @dynamic_test
    def test_level_2_correct(self):
        filepath = 'results.txt'
        file = open(filepath, 'w')
        file.write("The quick brown fox jumps over a lazy dog\n")
        file.close()
        file = open(filepath, 'r')
        text_from_file = file.read()
        file.close()

        pr = TestedProgram()
        first = pr.start()

        # 1 - ok
        task = pr.execute("2")
        correct_ans = str(int(task) ** 2)
        result = pr.execute(correct_ans).strip().lower()
        if "right" not in result:
            raise WrongAnswer(corr_as_incorr_msg + "\nThe task: " + task + '\nThe answer: ' + str(correct_ans))

        # 2 - wrong format + ok
        task = result.split('\n')
        if len(task) < 2:
            raise WrongAnswer(wrong_n_lines)
        task = task[1].strip()
        try:
            correct_ans = int(task) ** 2
        except ValueError:
            raise WrongAnswer("The task for level 2 should contain one number that the user should square.\n"
                              "It seems that your task either doesn't follow the required format, or doesn't contain a number.")

        result = pr.execute("11r").strip().lower()
        if "format" not in result:
            raise WrongAnswer(typo_msg)

        result = pr.execute("").strip().lower()
        if "format" not in result:
            raise WrongAnswer(typo_msg)

        result = pr.execute(str(correct_ans)).strip().lower()
        if "right" not in result:
            raise WrongAnswer(corr_as_incorr_msg + "\nThe task: " + task + '\nThe answer: ' + str(correct_ans))

        # 3 - wrong answer
        task = result.split('\n')
        if len(task) < 2:
            raise WrongAnswer(wrong_n_lines)
        task = task[1].strip()
        try:
            incorrect_ans = int(task) ** 2 + 3
        except ValueError:
            return CheckResult.wrong('Something is wrong with the output. '
                                     'Perhaps your program should have taken more input than it did')
        result = pr.execute(str(incorrect_ans)).strip().lower()
        if "wrong" not in result:
            raise WrongAnswer(incorr_as_corr_msg + "\nThe task: " + task + '\nThe answer: ' + str(incorrect_ans))

        # 4 - wrong answer
        task = result.split('\n')
        if len(task) < 2:
            raise WrongAnswer(wrong_n_lines)
        task = task[1].strip()
        try:
            incorrect_ans = int(task) ** 2 + 2
        except ValueError:
            return CheckResult.wrong('Something is wrong with the output. '
                                     'Perhaps your program should have taken more input than it did')
        result = pr.execute(str(incorrect_ans)).strip().lower()
        if "wrong" not in result:
            raise WrongAnswer(corr_as_incorr_msg + "\nThe task: " + task + 'The answer: ' + str(incorrect_ans))

        # 5 - wrong
        task = result.split('\n')
        if len(task) < 2:
            raise WrongAnswer(wrong_n_lines)
        task = task[1].strip()
        try:
            incorrect_ans = int(task) ** 2 + 3
        except ValueError:
            return CheckResult.wrong('Something is wrong with the output. '
                                     'Perhaps your program should have taken more input than it did')
        result = pr.execute(str(incorrect_ans)).strip().lower()
        if "wrong" not in result:
            raise WrongAnswer(incorr_as_corr_msg + "\nThe task:  " + task + '\nThe answer: ' + str(incorrect_ans))
        final_output = result
        result = result.replace(' ', '')

        if "2/5" in result:
            pass
        elif "/5" in result:
            return CheckResult.wrong("The number of correct answers is calculated incorrectly: \n" + final_output)
        else:
            return CheckResult.wrong("The final output doesn't contain count of correct answers: " + final_output)

        if "save" not in result:
            return CheckResult.wrong("Your app should ask if the user want to save results in file.")

        result = pr.execute("Yes").lower()
        if "name" not in result:
            return CheckResult.wrong("Your app should ask for the user's name.")
        result = pr.execute("Tester")
        if "saved" not in result:
            return CheckResult.wrong("The app should inform the user that the results were saved in the file.")

        if not os.path.exists(filepath):
            return CheckResult.wrong(f"The file {filepath} is not found.")
        file = open(filepath, 'r')
        text_from_file_after_saving = file.read()
        file.close()

        if text_from_file not in text_from_file_after_saving:
            return CheckResult.wrong("Your application shouldn't remove any information from the file with results "
                                     "if it already exists.")

        if all([i in text_from_file_after_saving for i in ["Tester", '2/5', '2', '11', '29']]):
            return CheckResult.correct()
        else:
            return CheckResult.wrong("The application didn't save the result in the needed format.\n"
                                     "The last lines written in the file: \n" +
                                     text_from_file_after_saving.replace(text_from_file, ''))

    @dynamic_test
    def test_no_file(self):
        self.remove_safely("results.txt")

        pr = TestedProgram()
        pr.start()
        pr.execute("1")
        # 5 tasks without checking
        pr.execute("1")
        pr.execute("1")
        pr.execute("1")
        pr.execute("1")
        pr.execute("1")
        pr.execute("y")
        pr.execute("nofile")

        if not os.path.exists("results.txt"):
            return CheckResult.wrong("Your app doesn't create the file \'results.txt\' when it doesn't exist.")

        file = open('results.txt', 'r')
        text = file.read().lower()
        file.close()

        if 'nofile' not in text:
            return CheckResult.wrong("The application didn't save the result in the needed format.")

        return CheckResult.correct()

    @dynamic_test
    def test_no_saving(self):
        self.remove_safely("results.txt")

        pr = TestedProgram()
        pr.start()
        pr.execute("1")
        # 5 tasks without checking
        pr.execute("1")
        pr.execute("1")
        pr.execute("1")
        pr.execute("1")
        pr.execute("1")
        pr.execute("y some text with y")

        if os.path.exists("results.txt"):
            self.remove_safely("results.txt")
            return CheckResult.wrong(
                'The app created the file for results, even though user hasn\'t answered "yes" or "y" (in any register).')

        if not pr.is_waiting_input():
            return CheckResult.correct()
        else:
            return CheckResult.wrong(
                'The app is waiting for the input after the user answered that the results shouldn\'t be saved to the file.\n'
                'Make sure your program stops running after the user answers whether the results should be saved.')

    def remove_safely(self, filename):
        import os
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                return CheckResult.wrong(
                    f"Can't delete the test file named '{filename}'. Make sure you close it.")


if __name__ == '__main__':
    ExamTest().run_tests()
