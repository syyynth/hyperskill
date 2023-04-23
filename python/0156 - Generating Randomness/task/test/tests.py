from hstest import CheckResult, StageTest, dynamic_test, TestedProgram

ASK_RANDOM_STRING = "Print a random string containing 0 or 1:"

# Case test
test_data_1 = [
    {
        "start": [
            {
                "expected": "Please provide AI some data to learn...",
                "feedback": "'Please provide AI some data to learn...' not found in the output!"
            },
            {
                "expected": "The current data length is 0, 100 symbols left",
                "feedback": "'The current data length is 0, 100 symbols left' not found in the output!"
            },
            {
                "expected": "Print a random string containing 0 or 1:",
                "feedback": "'Print a random string containing 0 or 1:' not found in the output!"
            },
        ],
        "test_cases": [
            {
                "case": "010100100101010101000010001010101010100100100101001",
                "verify": [
                    {
                        "expected": "current data length",
                        "feedback": "'current data length' is not found in the output!"
                    },
                    {
                        "expected": "length is 51",
                        "feedback": "Value for 'data length' is wrong!"
                    },
                    {
                        "expected": "49 symbols",
                        "feedback": "Value for for 'symbol left' is wrong!"
                    },
                    {
                        "expected": ASK_RANDOM_STRING,
                        "feedback": f"The program should ask for a random string!"
                    },
                ]
            },
            {
                "case": "011010001011111100101010100011001010101010010001001010010011",
                "verify": [
                    {
                        "expected": "010100100101010101000010001010101010100100100101001011010001011111100101010100011001010101010010001001010010011",
                        "feedback": "Final data string is wrong!"
                    },
                    {
                        "expected": "You have $1000. Every time the system successfully predicts your next press, you lose $1.",
                        "feedback": "Game information not found in the output!"
                    },
                    {
                        "expected": 'Otherwise, you earn $1. Print "enough" to leave the game.',
                        "feedback": "Game information not found in the output!"
                    },
                    {
                        "expected": ASK_RANDOM_STRING,
                        "feedback": f"The program should ask for a random string!"
                    },
                ]
            },
            {
                "case": "011",
                "verify": [
                    {
                        "expected": ASK_RANDOM_STRING,
                        "feedback": "The program should ask for a random string if string length is less than '4'!"
                    },
                ]
            },
            {
                "case": "01110010010",
                "verify": [
                    {
                        "expected": "predictions:",
                        "feedback": "'predictions:' is not found in the output!"
                    },
                    {
                        "expected": "guessed 5",
                        "feedback": "Value for 'guessed' is wrong!"
                    },
                    {
                        "expected": "out of 8",
                        "feedback": "Value for 'out of' is wrong!"
                    },
                    {
                        "expected": "Computer guessed",
                        "feedback": "'Computer guessed' not found in the output!"
                    },
                    {
                        "expected": "62.5",
                        "feedback": "Accuracy value is wrong!"
                    },
                    {
                        "expected": "Your balance is now",
                        "feedback": "'Your balance is now' not found in the output!"
                    },
                    {
                        "expected": "$998",
                        "feedback": "Balance value is wrong!"
                    },
                    {
                        "expected": ASK_RANDOM_STRING,
                        "feedback": f"{ASK_RANDOM_STRING} is not found in output!"
                    },
                ]
            },
            {
                "case": "0111001001001",
                "verify": [
                    {
                        "expected": "predictions:",
                        "feedback": "'predictions:' is not found in the output!"
                    },
                    {
                        "expected": "guessed 6",
                        "feedback": "Value for 'guessed' is wrong!"
                    },
                    {
                        "expected": "out of 10",
                        "feedback": "Value for 'out of' is wrong!"
                    },
                    {
                        "expected": "Computer guessed",
                        "feedback": "'Computer guessed' not found in the output!"
                    },
                    {
                        "expected": "60.0",
                        "feedback": "Accuracy value is wrong!"
                    },
                    {
                        "expected": "Your balance is now",
                        "feedback": "'Your balance is now' not found in the output!"
                    },
                    {
                        "expected": "$996",
                        "feedback": "Balance value is wrong!"
                    },
                    {
                        "expected": ASK_RANDOM_STRING,
                        "feedback": f"{ASK_RANDOM_STRING} is not found in output!"
                    },
                ]
            },
            {
                "case": "enough",
                "verify": [
                    {
                        "expected": "Game over!",
                        "feedback": "'Game over!' is not found in the output!"
                    },
                ]
            },
        ]
    }
]


class GenRandTest(StageTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output = None

    def case_test(self, dict_):
        """Tests case/expected"""
        t = TestedProgram()
        self.output = t.start()
        for item in dict_["start"]:
            if item["expected"].lower() not in self.output.lower():
                return CheckResult.wrong(item["feedback"])

        for test_case in dict_["test_cases"]:
            self.output = t.execute(test_case["case"])
            for item in test_case["verify"]:
                if item["expected"].lower() not in self.output.lower():
                    return CheckResult.wrong(item["feedback"])
        return CheckResult.correct()

    @dynamic_test(data=test_data_1)
    def test1(self, dict_):
        """Tests invalid option,
        non scores messages
        """
        return self.case_test(dict_)


if __name__ == '__main__':
    GenRandTest('predictor.predictor').run_tests()
