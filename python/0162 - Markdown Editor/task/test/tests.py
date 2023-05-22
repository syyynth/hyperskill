from hstest import StageTest, TestedProgram, CheckResult, dynamic_test


class Test(StageTest):

    answers = [
        '#### Hello World!\n',
        'plain text**bold text**',
        '*italic text*`code.work()`',
        '[google](https://www.google.com)\n',
        '1. first\n2. second\n3. third\n4. fourth\n'
    ]

    def check_result_in_file(self, attach):
        try:
            with open('output.md', 'r') as outfile:
                output = outfile.read()
                if output != self.answers[attach]:
                    return CheckResult.wrong('The result written to the output file is wrong.')
        except IOError:
            return CheckResult.wrong('The output file is not found.')
        return CheckResult.correct()


    @dynamic_test
    def test1(self):
        pr = TestedProgram()
        pr.start()

        output = pr.execute('header').strip().lower()
        if 'level' not in output:
            return CheckResult.wrong('Header formatter should prompt a user for both level and text, i.e "- Level: > "')

        output = pr.execute('4').strip().lower()
        if 'text' not in output.strip().lower():
            return CheckResult.wrong('Header formatter should prompt a user for both level and text, i.e "- Text: > "')

        output = list(map(lambda item: item.lower(), pr.execute('Hello World!').split('\n')))
        if len(output) != 3:
            return CheckResult.wrong('Please remember that header formatter switches to a new line automatically')

        if output[0].strip().split() != ['####', 'hello', 'world!']:
            return CheckResult.wrong('Level 4 for header denotes as #### in markdown')

        if output[1]:
            return CheckResult.wrong('Please check whether some redundant data is printed after a header')

        if 'formatter' not in output[2].strip():
            return CheckResult.wrong('A user should be prompted for input again, i.e  "- Choose a formatter: > "')

        pr.execute('!done')
        if not pr.is_finished():
            return CheckResult.wrong('Your program should finish its execution whenever !done is an input')

        return self.check_result_in_file(attach=0)

    @dynamic_test
    def test2(self):
        pr = TestedProgram()
        pr.start()

        output = pr.execute('plain').strip().lower()
        if 'text' not in output.strip().lower():
            return CheckResult.wrong('Plain formatter should prompt a user for text, i.e "- Text: > "')

        output = list(map(lambda item: item.lower(), pr.execute('plain text').split('\n')))
        if len(output) != 2:
            return CheckResult.wrong("Plain formatter should only return the given text as is, and prompt a user for a new formatter")

        if output[0] != 'plain text':
            return CheckResult.wrong('Plain formatter returns the given text as is, without any extra symbols or tags')

        if 'formatter' not in output[1].strip():
            return CheckResult.wrong('A user should be prompted for input again, i.e  "- Choose a formatter: > "')

        output = pr.execute('bold').strip().lower()
        if 'text' not in output:
            return CheckResult.wrong('Bold formatter should prompt a user for text, i.e "- Text: > "')

        output = list(map(lambda item: item.lower(), pr.execute('bold text').split('\n')))
        if len(output) != 2:
            return CheckResult.wrong("Bold formatter should only return the given text enclosed with '**' symbols, and prompt a user for a new formatter")

        if output[0] != 'plain text**bold text**':
            return CheckResult.wrong('Plain formatter returns the given text as is, and does not switch to a new line')

        if 'formatter' not in output[1].strip():
            return CheckResult.wrong('A user should be prompted for input again, i.e  "- Choose a formatter: > "')

        pr.execute('!done')
        if not pr.is_finished():
            return CheckResult.wrong('Your program should finish its execution whenever !done is an input')

        return self.check_result_in_file(attach=1)

    @dynamic_test
    def test3(self):
        pr = TestedProgram()
        pr.start()

        output = pr.execute('italic').strip().lower()
        if 'text' not in output.strip().lower():
            return CheckResult.wrong('Italic formatter should prompt a user for text, i.e "- Text: > "')

        output = list(map(lambda item: item.lower(), pr.execute('italic text').split('\n')))
        if len(output) != 2 or output[0] != '*italic text*':
            return CheckResult.wrong("Bold formatter should only return the given text enclosed with '*' symbols, and prompt a user for a new formatter")

        if 'formatter' not in output[1].strip():
            return CheckResult.wrong('A user should be prompted for input again, i.e  "- Choose a formatter: > "')

        output = pr.execute('inline-code').strip().lower()
        if 'text' not in output:
            return CheckResult.wrong('Inline code formatter should prompt a user for text, i.e "- Text: > "')

        output = list(map(lambda item: item.lower(), pr.execute('code.work()').split('\n')))
        if len(output) != 2:
            return CheckResult.wrong("Inline code formatter should only return the given text enclosed with '`' (backtick) symbols, and prompt a user for a new formatter")

        if output[0] != '*italic text*`code.work()`':
            return CheckResult.wrong('Inline code formatter does not switch to a new line')

        if 'formatter' not in output[1].strip():
            return CheckResult.wrong('A user should be prompted for input again, i.e  "- Choose a formatter: > "')

        pr.execute('!done')
        if not pr.is_finished():
            return CheckResult.wrong('Your program should finish its execution whenever !done is an input')

        return self.check_result_in_file(attach=2)

    @dynamic_test
    def test4(self):
        pr = TestedProgram()
        pr.start()

        output = pr.execute('link').strip().lower()
        if 'label' not in output:
            return CheckResult.wrong('Link formatter should prompt a user for both label and URL, i.e "- Label: > "')

        output = pr.execute('google').strip().lower()
        if 'url' not in output:
            return CheckResult.wrong('Link formatter should prompt a user for both label and URL, i.e "- URL: > "')

        output = list(map(lambda item: item.lower(), pr.execute('https://www.google.com').split('\n')))
        if len(output) != 2:
            return CheckResult.wrong('Link code formatter should only return the given label associated with a URL in the form [Label](URL), and prompt a user for a new formatter')

        if output[0] != '[google](https://www.google.com)':
            return CheckResult.wrong('Please recall that for the given label and URL the correct link formatter return will be [Label](URL)')

        if 'formatter' not in output[1].strip():
            return CheckResult.wrong('A user should be prompted for input again, i.e  "- Choose a formatter: > "')

        output = list(map(lambda item: item.lower(), pr.execute('new-line').split('\n')))
        if len(output) != 3 or output[1] != '':
            return CheckResult.wrong('New-line formatter only moves the input pointer to the next line, and prompts a user for a new formatter')

        if output[0] != '[google](https://www.google.com)':
            return CheckResult.wrong('Please make sure that the markdown state is saved')

        if 'formatter' not in output[2].strip():
            return CheckResult.wrong('A user should be prompted for input again, i.e  "- Choose a formatter: > "')

        pr.execute('!done')
        if not pr.is_finished():
            return CheckResult.wrong('Your program should finish its execution whenever !done is an input')

        return self.check_result_in_file(attach=3)

    @dynamic_test
    def test5(self):
        pr = TestedProgram()
        pr.start()

        output = pr.execute('ordered-list').strip().lower()
        if 'number' not in output:
            return CheckResult.wrong('Ordered list formatter should prompt a user for the number of rows, i.e "- Number of rows: > "')

        output = list(map(lambda item: item.lower(), pr.execute('0').split('\n')))
        if len(output) < 2 or 'number' not in output[-1].strip():
            return CheckResult.wrong('(Un)ordered list formatter should inform a user that the number of rows should be greater than zero if the input was invalid, and prompt the user for this input again, i.e "- Number of rows: > "')

        pr.execute('4')
        pr.execute('first')
        pr.execute('second')
        pr.execute('third')
        output = list(map(lambda item: item.lower(), pr.execute('fourth').split('\n')))
        if len(output) != 6:
            return CheckResult.wrong('Ordered list formatter should switch to a new line automatically')

        if output[0] != '1. first' or output[1] != '2. second' or output[2] != '3. third' or output[3] != '4. fourth':
            return CheckResult.wrong('Ordered list formatter should enumerate its rows in the following manner: "1. ", "2.", and so on, depending on the given number of rows.')

        if 'formatter' not in output[5].strip():
            return CheckResult.wrong('A user should be prompted for input again, i.e  "- Choose a formatter: > "')

        pr.execute('!done')
        if not pr.is_finished():
            return CheckResult.wrong('Your program should finish its execution whenever !done is an input')

        return self.check_result_in_file(attach=4)


if __name__ == '__main__':
    Test().run_tests()
