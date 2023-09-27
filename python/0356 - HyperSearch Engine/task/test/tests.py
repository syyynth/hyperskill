from hstest import StageTest, TestedProgram, dynamic_test, WrongAnswer, TestPassed

class SearchEngineTest(StageTest):
    @dynamic_test
    def test_spacy(self):
        pr = TestedProgram()
        output = pr.start().lower()
        if 'enter your query' not in output:
            raise WrongAnswer("Your program should print 'Enter your query, please'")
        sec_output = pr.execute("Scala").lower().strip()
        if 'enter limit' not in sec_output:
            raise WrongAnswer("Your program should print 'Enter limit'")
        third_output = pr.execute("1").lower().strip()
        if 'enter offset' not in third_output:
            raise WrongAnswer("Your program should print 'Enter offset'")
        fourth_output = pr.execute("0").lower().strip()
        len_output = len(fourth_output)
        if len_output == 0:
            raise WrongAnswer(
                "The output is empty: your program should print the names of the files and the text from the files'")
        if 'branching.txt' not in fourth_output:
            raise WrongAnswer("Your program should find and print file name 'Branching.txt'")
        elif 'introduction to python.txt' in fourth_output:
            raise WrongAnswer("Your program shouldn't find and print file name 'Introduction to Python.txt'")
        elif 'invoking a function.txt' in fourth_output:
            raise WrongAnswer("Your program shouldn't find and print file name 'Invoking a function.txt'")
        elif 'functional decomposition.txt' in fourth_output:
            raise WrongAnswer("Your program shouldn't find and print file name 'Functional decomposition.txt'")
        elif 'reader and writer interfaces.txt' in fourth_output:
            raise WrongAnswer("Your program shouldn't find and print file name 'Reader and Writer interfaces.txt'")
        elif 'intro to text representation.txt' in fourth_output:
            raise WrongAnswer("Your program shouldn't find and print file name 'Intro to text representation.txt'")
        elif '...xecution, fork, or branching.' not in fourth_output:
            raise WrongAnswer("Invalid context window (start).")
        elif '<b>scala</b>' not in fourth_output:
            raise WrongAnswer("The target word should be surrounded by <b> and </b> symbols.")
        elif 'has the if else syntax for t...' not in fourth_output:
            raise WrongAnswer("Invalid context window (end).")
        elif 'do you want to make another request? (yes/no)' not in fourth_output:
            raise WrongAnswer("Your program should print 'Do you want to make another request? (yes/no)'")
        fifth_output = pr.execute("yes").lower().strip()
        if 'enter your query' not in fifth_output:
            raise WrongAnswer("Your program should print 'Enter your query, please'")
        sixth_output = pr.execute("Functional decomposition").lower().strip()
        if 'enter limit' not in sixth_output:
            raise WrongAnswer("Your program should print 'Enter limit'")
        seventh_output = pr.execute("1").lower().strip()
        if 'enter offset' not in seventh_output:
            raise WrongAnswer("Your program should print 'Enter offset'")
        eighth_output = pr.execute("0").lower().strip()
        len_output2 = len(eighth_output)
        if len_output2 == 0:
            raise WrongAnswer(
                "The output is empty: your program should print the names of the files and the text from the files'")
        if 'functional decomposition.txt' not in eighth_output:
            raise WrongAnswer("Your program should find and print file name 'Functional decomposition.txt'")
        elif 'intro to text representation.txt' in eighth_output:
            raise WrongAnswer("Your program shouldn't find and print file name 'Intro to text representation.txt'")
        elif 'introduction to python.txt' in eighth_output:
            raise WrongAnswer("Your program shouldn't find and print file name 'Introduction to Python.txt'")
        elif 'invoking a function.txt' in eighth_output:
            raise WrongAnswer("Your program shouldn't find and print file name 'Invoking a function.txt'")
        elif 'reader and writer interfaces.txt' in eighth_output:
            raise WrongAnswer("Your program shouldn't find and print file name 'Reader and Writer interfaces.txt'")
        elif 'branching.txt' in eighth_output:
            raise WrongAnswer("Your program shouldn't find and print file name 'Branching.txt'")
        elif '<b>functional</b>' not in eighth_output:
            raise WrongAnswer("The target word should be surrounded by <b> and </b> symbols.")
        elif '<b>decomposition</b>' not in eighth_output:
            raise WrongAnswer("The target word should be surrounded by <b> and </b> symbols.")
        elif 'is simply a pr...' not in eighth_output:
            raise WrongAnswer("Invalid context window (end).")
        elif '...<b>functional</b>' in eighth_output:
            raise WrongAnswer("There should not be an ellipsis at the beginning of the context window, because it is at the beginning of the document.")
        elif 'do you want to make another request? (yes/no)' not in eighth_output:
            raise WrongAnswer("Your program should print 'Do you want to make another request? (yes/no)'")
        ninth_output = pr.execute("yes").lower().strip()
        if 'enter your query' not in ninth_output:
            raise WrongAnswer("Your program should print 'Enter your query, please'")
        tenth_output = pr.execute("length").lower().strip()
        if 'enter limit' not in tenth_output:
            raise WrongAnswer("Your program should print 'Enter limit'")
        eleventh_output = pr.execute("1").lower().strip()
        if 'enter offset' not in eleventh_output:
            raise WrongAnswer("Your program should print 'Enter offset'")
        twelfth_output = pr.execute("0").lower().strip()
        len_output3 = len(twelfth_output)
        if len_output3 == 0:
            raise WrongAnswer(
                "The output is empty: your program should print the names of the files and the text from the files'")
        if 'invoking a function.txt' not in twelfth_output:
            raise WrongAnswer("Your program should find and print file name 'Invoking a function.txt'")
        elif 'intro to text representation.txt' in twelfth_output:
            raise WrongAnswer("Your program shouldn't find and print file name 'Intro to text representation.txt'")
        elif 'introduction to python.txt' in twelfth_output:
            raise WrongAnswer("Your program shouldn't find and print file name 'Introduction to Python.txt'")
        elif 'functional decomposition.txt' in twelfth_output:
            raise WrongAnswer("Your program shouldn't find and print file name 'Functional decomposition.txt'")
        elif 'reader and writer interfaces.txt' in twelfth_output:
            raise WrongAnswer("Your program shouldn't find and print file name 'Reader and Writer interfaces.txt'")
        elif 'branching.txt' in twelfth_output:
            raise WrongAnswer("Your program shouldn't find and print file name 'Branching.txt'")
        elif '<b>length</b>' not in twelfth_output:
            raise WrongAnswer("The target word should be surrounded by <b> and </b> symbols.")
        elif '...out the object: its type() or' not in twelfth_output:
            raise WrongAnswer("Invalid context window (start).")
        elif 'len().' not in twelfth_output:
            raise WrongAnswer("Invalid context window (end).")
        elif 'len()...' in eighth_output:
            raise WrongAnswer(
                "There should not be an ellipsis at the end of the context window, because it is at the end of the document.")
        elif 'do you want to make another request? (yes/no)' not in twelfth_output:
            raise WrongAnswer("Your program should print 'Do you want to make another request? (yes/no)'")
        ninth_output = pr.execute("no").lower().strip()
        if 'bye' not in ninth_output:
            raise WrongAnswer("Your program should print 'Bye!'")
        else:
            raise TestPassed()