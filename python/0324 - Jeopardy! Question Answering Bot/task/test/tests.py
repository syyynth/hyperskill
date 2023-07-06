from hstest import StageTest, TestedProgram,  dynamic_test, WrongAnswer, TestPassed
import re

def check_percent(text):
    percent_pat = re.compile(r'(\d{2})(?=%)')
    find_percent = re.search(percent_pat, text)
    if find_percent == None:
        raise WrongAnswer("""Your output should contain the similarity rank, but it doesn't""")
    percent = int(find_percent.group(0))
    if percent < 50:
        return False
    else:
        return True

class QABotTest(StageTest):
    @dynamic_test(time_limit=0)
    def test_program(self):
        pr = TestedProgram()
        output = pr.start().lower().strip()
        marks = '''!',."'''
        for x in output:
            if x in marks:
                output = output.replace(x, "")
        if "hello im" not in output:
            raise WrongAnswer(
                """Your output should contain "Hello! I'm (the QA bot name you chose), a question answering bot who knows answers to all questions from the 'Jeopardy!' game.", but it doesn't""")
        elif "a question answering bot who knows answers to all questions from the jeopardy game" not in output:
            raise WrongAnswer(
                """Your output should contain "Hello! I'm (the QA bot name you chose), a question answering bot who knows answers to all questions from the 'Jeopardy!' game.", but it doesn't""")
        elif "ask me something" not in output:
            raise WrongAnswer("""Your output should contain "Ask me something!", but it doesn't""")
        question1 = """The song "Cherish" was the first No. 1 hit for this L.A. band"""
        output2 = pr.execute(question1)
        if "76740" not in output2:
            raise WrongAnswer(
                'The number of the closest topic is wrong. Please, check the parameters and retrain your model.')
        model_qual1 = check_percent(output2)
        if model_qual1 == False:
            raise WrongAnswer("Similarity rank is too low. Please, check the parameters and retrain your model.")
        elif "The Association" not in output2:
            raise WrongAnswer("The selected answer is incorrect.")
        pr.execute('yes')
        question2 = "This butterfly-shaped gland straddles the windpipe just behind the Adam's apple"
        output3 = pr.execute(question2)
        if "76900" not in output3:
            raise WrongAnswer(
                'The number of the closest topic is wrong. Please, check the parameters and retrain your model.')
        model_qual2 = check_percent(output3)
        if model_qual2 == False:
            raise WrongAnswer("Similarity rank is too low. Please, check the parameters and retrain your model.")
        elif "the thyroid" not in output3:
            raise WrongAnswer("The selected answer is incorrect.")
        pr.execute('yes')
        question3 = "In Egypt & Algeria, some areas of this desert are below sea level"
        output4 = pr.execute(question3)
        if "79995" not in output4:
            raise WrongAnswer(
                'The number of the closest topic is wrong. Please, check the parameters and retrain your model.')
        model_qual3 = check_percent(output4)
        if model_qual3 == False:
            raise WrongAnswer("Similarity rank is too low. Please, check the parameters and retrain your model.")
        elif "Sahara" not in output4:
            raise WrongAnswer("The selected answer is incorrect.")
        pr.execute('yes')
        question4 = "After converting this Balkan country to Christianity, Czar Boris I put out his own son's eyes"
        output5 = pr.execute(question4)
        if "51508" not in output5:
            raise WrongAnswer(
                'The number of the closest topic is wrong. Please, check the parameters and retrain your model.')
        model_qual4 = check_percent(output5)
        if model_qual4 == False:
            raise WrongAnswer("Similarity rank is too low. Please, check the parameters and retrain your model.")
        elif "Bulgaria" not in output5:
            raise WrongAnswer("The selected answer is incorrect.")
        pr.execute('yes')
        question5 = 'The name of this ballroom dance with gliding turns comes from German for "roll" or "turn"'
        output6 = pr.execute(question5)
        if "19908" not in output6:
            raise WrongAnswer(
                'The number of the closest topic is wrong. Please, check the parameters and retrain your model.')
        model_qual5 = check_percent(output6)
        if model_qual5 == False:
            raise WrongAnswer("Similarity rank is too low. Please, check the parameters and retrain your model.")
        elif "a waltz" not in output6:
            raise WrongAnswer("The selected answer is incorrect.")
        output7 = pr.execute('no').lower().strip()
        if "it was nice to play with you" not in output7 or "goodbye" not in output7:
            raise WrongAnswer("""Your output should contain "It was nice to play with you! Goodbye!", but it doesn't""")
        else:
            raise TestPassed()
