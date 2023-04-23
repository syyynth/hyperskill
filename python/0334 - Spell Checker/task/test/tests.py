from hstest import StageTest, TestedProgram, dynamic_test, WrongAnswer, TestPassed
import string

class SpellCheckerTest(StageTest):

    @dynamic_test(time_limit=0)
    def test_bigrams(self):
        pr = TestedProgram()
        output = pr.start().lower().strip()
        rem_punct = [sym for sym in output if sym not in string.punctuation]
        cl_output = ''.join(rem_punct)
        if "hello please enter a text here" not in cl_output:
            raise WrongAnswer('Your program should print "Hello! Please, enter a text here", but it doesn\'t.')
        text = "I think it is realy important to keap your own word"
        second_output = pr.execute(text).lower().strip()
        if "misspelled words found in your text" not in second_output:
            raise WrongAnswer("""Your program should print "Misspelled words found in your text", but it doesn\'t.""")
        elif "realy" not in second_output:
            raise WrongAnswer('Your program doesn\'t found a misspelled word "realy" in the text.')
        elif "keap" not in second_output:
            raise WrongAnswer('Your program doesn\'t found a misspelled word "keap" in the text.')
        elif "your grade is b" not in second_output:
            raise WrongAnswer("""The grade is incorrect.""")
        elif "errors found in the text" not in second_output:
            raise WrongAnswer("""Your program should print "Errors found in the text: ", but it doesn\'t.""")
        elif "2" not in second_output:
            raise WrongAnswer("The number of errors is incorrect.")
        elif "i think it is really important to keep your own word" not in second_output:
            raise WrongAnswer("There are errors in the corrected text.")
        else:
            raise TestPassed()
