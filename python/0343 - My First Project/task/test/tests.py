from hstest import StageTest, TestedProgram, CheckResult, dynamic_test

# Bubblegum: $202.0
# Toffee: $118.0
# Ice cream: $2250.0
# Milk chocolate: $1680.0
# Doughnut: $1075.0
# Pancake: $80.0
#
# Income: $5405.0
# Staff expenses: $4170
# Other expenses: $220
# Net income: $1015


class PrintFirstProject(StageTest):
    @dynamic_test()
    def test_first_project(self):
        pr = TestedProgram()
        output = pr.start().lower().strip()
        output_length = len(list(filter(None, output.splitlines())))
        if not output:
            return CheckResult.wrong("Your program didn't print any output.")
        elif output_length != 9:
            return CheckResult.wrong(f'Your program should output 9 lines:\n'
                                     f'the earned amount for each item, income, and the "Staff expenses" line.\n'
                                     f'{output_length} lines were found.')

        elif 'bubblegum' not in output.lower():
            return CheckResult.wrong("Your program didn't print the 'Bubblegum' as an item")
        elif 'toffee' not in output.lower():
            return CheckResult.wrong("Your program should print the 'Toffee' as an item")
        elif 'ice cream' not in output.lower():
            return CheckResult.wrong("Your program should print the 'Ice Cream' as an item")
        elif 'milk chocolate' not in output.lower():
            return CheckResult.wrong("Your program should print the 'Milk Chocolate' as an item")
        elif 'doughnut' not in output.lower():
            return CheckResult.wrong("Your program should print the 'Doughnut' as an item")
        elif 'pancake' not in output.lower():
            return CheckResult.wrong("Your program should print the 'Pancake' as an item")
        elif 'income' not in output.lower():
            return CheckResult.wrong("Your program should print the 'Income' as an item")
        elif 'staff expenses' not in output:
            return CheckResult.wrong("Your program should print 'Staff expenses'")
        elif '202' not in output.lower():
            return CheckResult.wrong("Wrong earned amount for Bubblegum.")
        elif '118' not in output.lower():
            return CheckResult.wrong("Wrong earned amount for Toffee.")
        elif '2250' not in output.lower():
            return CheckResult.wrong("Wrong earned amount for Ice Cream.")
        elif '1680' not in output.lower():
            return CheckResult.wrong("Wrong earned amount for Milk Chocolate.")
        elif '1075' not in output.lower():
            return CheckResult.wrong("Wrong earned amount for Doughnut.")
        elif '80' not in output.lower():
            return CheckResult.wrong("Wrong earned amount for Pancake.")
        elif '5405' not in output.lower():
            return CheckResult.wrong("Incorrect income!")
        output1 = pr.execute('4170').lower().strip()
        if 'other expenses' not in output1:
            return CheckResult.wrong("Your program should print 'Other expenses'")
        output2 = pr.execute('220').lower().strip()
        if 'net income' not in output2:
            return CheckResult.wrong("Your program should print 'Net income'")
        elif '1015' not in output2.lower():
            return CheckResult.wrong("Incorrect net income!")
        else:
            return CheckResult.correct()


if __name__ == '__main__':
    PrintFirstProject().run_tests()
