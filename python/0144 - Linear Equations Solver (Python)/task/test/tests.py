from typing import List, Any
from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.check_result import CheckResult
import numpy as np


class TestClue:

    def __init__(self, feedback, out_file, answers):
        self.feedback = feedback
        self.out_file = out_file
        self.answers = answers


class TestTheFifth(StageTest):

    no_solutions = "No solutions"
    infinite_solutions = "Infinitely many solutions"

    def generate(self) -> List[TestCase]:
        list_tests = [
            TestCase(attach=TestClue("Test exactly like in the example",
                                     "out.txt", np.array([1.0, 2.0, 3.0])),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "3 3\n1 1 2 9\n2 4 -3 1\n3 6 -5 0",
                     }),

            TestCase(attach=TestClue("",
                                     "out.txt", np.array([1.0, 1.0])),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "2 2\n1 0 1\n0 1 1",
                     }),

            TestCase(attach=TestClue("Check if you process \"-in\" argument from command line",
                                     "out.txt", np.array([1.0, 1.0])),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "2 2\n1 0 1\n0 1 1",
                     }),

            TestCase(attach=TestClue("Check if you process \"-out\" argument from command line",
                                     "out.txt", np.array([1.0, 1.0])),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "2 2\n1 0 1\n0 1 1",
                     }),

            TestCase(attach=TestClue("",
                                     "out.txt", np.array([2.0, 2.0])),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "2 2\n1 0 2\n0 1 2",
                     }),

            TestCase(attach=TestClue("",
                                     "out.txt", np.array([1.0, 1.0])),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "2 2\n2 0 2\n0 2 2",
                     }),

            TestCase(attach=TestClue("",
                                     "out.txt", np.array([-1.0, 1.0])),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "2 2\n1 2 1\n3 4 1",
                     }),

            TestCase(attach=TestClue("This test is a system of 20 linear equations",
                                     "out.txt", np.array([0.5428, -2.3923, 1.5789, -1.3679, 0.6433, -1.7531,
                                                          -0.0432, -0.7503, -0.8245, -0.4562, -1.2163, 0.3093,
                                                          -0.1105, 1.1717, -0.5873, -1.3933, 1.1229, 3.0693,
                                                          1.1995, 1.5399])),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "20 20\n26.0 90. 17. 67. 68. 9. 60. 38. 37. 38. 76. 14. 33. 94. 88. 58. 99. 84. 9. 45. 18.\n"
                                   "37.0 34.0 20. 53. 10. 61. 75. 49. 91. 84. 55. 84. 84. 81. 30. 22. 42. 76. 33. 27. 2.\n"
                                   "99.0 69. 63. 57. 39. 45. 33. 43. 99. 26. 25. 24. 80. 91. 62. 90. 54. 77. 88. 32. 94.\n"
                                   "37.0 40. 14. 5. 47. 30. 5. 21. 36. 77. 57. 38. 29. 3. 61. 12. 81. 19. 39. 56. 9.\n"
                                   "36.0 73. 71. 39. 9. 9. 31. 10. 84. 7. 13. 45. 9. 34. 2. 14. 88. 43. 17. 4. 86.\n"
                                   "31.0 29. 76. 89. 26. 35. 11. 55. 37. 5. 41. 96. 19. 18. 100. 20. 21. 49. 83. 5. 20.\n"
                                   "18.0 18. 25. 70. 79. 74. 30. 66. 41. 93. 63. 2. 90. 4. 46. 1. 77. 89. 21. 47. 52.\n"
                                   "32.0 62. 27. 80. 57. 10. 35. 44. 97. 18. 58. 19. 5. 81. 33. 54. 83. 66. 25. 75. 75.\n"
                                   "56.0 53. 13. 91. 30. 11. 72. 52. 13. 86. 73. 88. 94. 20. 25. 77. 90. 75. 73. 52. 36.\n"
                                   "63.0 9. 40. 40. 35. 90. 55. 92. 12.0 98.0 34. 37. 64. 21. 67. 91. 15. 65. 82. 87. 30.\n"
                                   "71.0 5. 65. 64. 6. 20. 9. 81. 40. 56. 39. 93. 74. 55. 83. 81. 74. 2. 58. 86. 58.\n"
                                   "13.0 50. 31. 86. 73. 36. 83. 27. 37. 96. 37. 28. 75. 91. 15. 78. 90. 56. 57. 18. 18.\n"
                                   "34.0 9. 51. 11. 92. 54. 25. 91. 61. 69. 37. 37. 89. 91. 95. 50. 10. 16. 69. 71. 66.\n"
                                   "25.0 16.0 79. 36. 6. 28. 51. 100. 5. 28. 97. 23. 44. 32. 50. 2. 96. 18. 5. 48. 44.\n"
                                   "80.0 38.0 47. 96. 41. 72. 85. 79. 2. 3. 96. 14. 2. 65. 97. 38. 76. 73. 88. 59. 89.\n"
                                   "31.0 98.0 88. 52. 49. 68. 46. 79. 26. 30. 31. 76. 84. 87. 27. 16. 66. 55. 78. 2. 46.\n"
                                   "57. 2. 32. 78. 70. 7 95. 56. 77. 97. 49. 14. 74. 7. 85. 48. 83. 59. 71. 5. 44.\n"
                                   "4. 64. 4. 43. 54. 99. 77. 7. 72. 82. 27. 22. 29. 94. 53. 48. 65. 88. 26. 86. 42.\n"
                                   "69. 59. 62. 63. 42. 29. 73. 18. 82. 78. 48. 60. 84. 73. 84. 9. 82. 53. 14. 1. 12.\n"
                                   "98.0 2. 47. 62. 69. 11. 28. 14. 83. 32. 94. 24. 71. 1. 16. 91. 53. 50. 38. 26. 17."
                     }),

            TestCase(attach=TestClue("This test is a system of 20 linear equations",
                                     "out.txt", np.array([0.2182, 0.3886, 0.2337, 0.5804, -0.1867, 0.3536,
                                                          -0.5597, -0.4706, -0.3946, -0.4577, 0.371, -0.1959,
                                                          1.1403, 0.2808, -0.8712, -0.3355, -0.1309, -0.3008,
                                                          0.6355, 0.4716])),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "20 20\n0.11 0.62 0.28 0.94 0.53 0.94 0.06 1.0 0.61 0.45 0.03 0.79 0.87 0.32 0.66 0.5 0.14 0.82 0.44 0.13 0.43\n"
                    "0.8 0.7 0.16 0.09 0.4 0.63 0.46 1.0 0.9 0.14 0.03 0.8 0.98 0.71 0.67 0.42 0.73 0.01 0.75 0.59 0.64\n"
                    "0.99 0.01 0.45 0.85 0.17 0.14 0.58 0.27 0.96 0.52 0.74 0.89 0.72 0.93 0.22 0.9 0.41 0.78 0.56 0.67 0.84\n"
                    "0.19 0.35 0.98 0.28 0.74 0.42 0.82 0.51 0.33 0.84 0.85 0.46 0.71 0.93 0.11 0.88 0.08 0.72 0.68 0.73 0.82\n"
                    "0.59 0.52 0.17 0.62 0.9 0.66 0.23 0.47 0.29 0.78 0.43 0.99 0.67 0.63 0.38 0.85 0.72 0.6 0.97 0.75 0.96\n"
                    "0.66 0.24 0.9 0.43 0.39 0.31 0.64 0.17 0.75 0.62 0.38 0.38 0.41 0.38 0.41 0.9 0.29 0.21 0.54 0.87 0.35\n"
                    "0.06 0.57 0.04 0.74 0.27 0.75 0.0 0.52 0.42 0.85 0.35 0.19 0.57 0.42 0.93 0.77 0.09 0.4 0.83 0.39 0.46\n"
                    "0.87 0.77 0.71 0.61 0.73 0.28 0.02 0.96 0.29 0.37 0.27 0.43 0.02 0.82 0.16 0.34 0.49 0.9 0.35 0.11 0.18\n"
                    "0.87 0.7 0.4 0.27 0.35 0.57 0.36 0.89 0.09 0.78 0.64 0.84 0.06 0.69 0.41 0.4 0.64 0.55 0.81 0.69 0.27\n"
                    "0.34 0.49 0.27 1.0 0.78 0.01 0.58 0.87 0.47 0.27 0.23 0.35 0.55 0.06 0.67 0.74 0.17 0.68 0.75 0.76 0.16\n"
                    "0.38 0.71 0.29 0.94 0.84 0.46 0.98 0.0 0.89 0.58 0.09 0.04 0.04 0.66 0.21 0.58 0.8 0.96 0.78 0.67 0.11\n"
                    "0.36 0.37 0.1 0.36 0.46 0.15 0.99 0.38 0.39 0.52 0.76 0.68 0.94 0.31 0.21 0.99 0.78 0.17 0.15 0.06 0.06\n"
                    "0.94 0.3 0.35 0.24 0.79 0.86 0.7 0.81 0.2 0.23 0.52 0.91 0.55 0.21 0.47 0.44 0.1 0.97 0.61 0.13 0.03\n"
                    "0.03 0.28 0.32 0.06 0.54 0.08 1.0 0.69 0.29 0.48 0.84 0.37 0.74 0.13 0.2 0.75 0.46 0.03 0.68 0.72 0.33\n"
                    "0.43 0.78 0.69 0.91 0.8 0.68 0.46 0.9 0.65 0.19 0.81 0.28 0.3 0.75 0.94 0.05 0.65 0.29 0.61 0.74 0.68\n"
                    "0.01 0.46 0.38 0.72 0.97 0.39 0.88 0.62 0.93 0.26 0.58 0.02 0.95 0.49 0.69 0.64 0.47 0.53 0.43 0.1 0.09\n"
                    "0.83 0.72 0.84 0.41 0.53 0.53 0.67 0.09 0.49 0.42 0.88 0.14 0.09 0.02 0.49 0.29 0.29 0.17 0.08 0.9 0.45\n"
                    "0.54 0.57 0.53 0.23 0.78 0.89 0.24 0.98 0.7 0.75 0.46 0.85 0.39 0.58 0.36 0.29 0.54 0.83 0.97 0.62 0.34\n"
                    "0.3 0.64 0.71 0.07 0.03 0.76 0.25 0.34 0.97 0.93 0.48 0.57 0.98 0.33 0.4 0.18 0.01 0.81 0.38 0.87 0.95\n"
                    "0.25 0.7 0.07 0.4 0.67 0.84 0.12 0.43 0.61 0.7 0.89 0.88 0.48 0.14 0.32 0.98 0.15 0.87 0.34 0.81 0.37"}),

            TestCase(attach=TestClue("Check is the first element is zero",
                                     "out.txt", np.array([1.0, 1.0])),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "2 2\n0 1 1\n1 0 1",
                     }),

            TestCase(attach=TestClue("",
                                     "out.txt", np.array([2.0, 1.0])),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "2 2\n0 1 1\n1 0 2",
                     }),

            TestCase(attach=TestClue("",
                                     "out.txt", np.array([-0.5175, -0.1523, 0.7669, 2.0115, 0.0958, 0.2849])),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "6 6\n2.0 6.0 1.0 3.0 9.0 1.0 6.0"
                                   "\n9.0 2.0 4.0 3.0 6.0 1.0 5.0"
                                   "\n6.0 5.0 9.0 1.0 4.0 2.0 6.0"
                                   "\n4.0 1.0 1.0 2.0 9.0 2.0 4.0"
                                   "\n5.0 4.0 6.0 2.0 3.0 1.0 6.0"
                                   "\n3.0 5.0 4.0 1.0 7.0 9.0 6.0",
                     }),

            TestCase(attach=TestClue("",
                                     "out.txt", np.array([0.241, 0.5984, 0.2851, 0.1325, 0.1446, 0.4257])),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "6 6\n0.0 6.0 1.0 3.0 9.0 1.0 6.0"
                                   "\n9.0 0.0 4.0 3.0 6.0 1.0 5.0"
                                   "\n6.0 5.0 0.0 1.0 4.0 2.0 6.0"
                                   "\n4.0 1.0 1.0 0.0 9.0 2.0 4.0"
                                   "\n5.0 4.0 6.0 2.0 0.0 1.0 6.0"
                                   "\n3.0 5.0 4.0 1.0 7.0 0.0 6.0",
                     }),

            TestCase(attach=TestClue("",
                                     "out.txt", np.array([-65.8154, 13.0615, -4.4, 2.6154, -0.9231, 3.5385])),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "6 6\n1.0 6.0 1.0 1.0 9.0 1.0 6.0"
                                   "\n0.0 1.0 4.0 3.0 2.0 1.0 5.0"
                                   "\n0.0 0.0 0.0 1.0 4.0 2.0 6.0"
                                   "\n0.0 0.0 0.0 2.0 9.0 2.0 4.0"
                                   "\n0.0 0.0 0.0 2.0 3.0 1.0 6.0"
                                   "\n0.0 0.0 5.0 1.0 7.0 9.0 6.0",
                     }),

            TestCase(attach=TestClue("",
                                     "out.txt", np.array([-50.381, 10.6508, -2.0794, 0.5556, -1.0, 3.0])),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "6 6\n1.0 6.0 1.0 1.0 9.0 1.0 6.0"
                                   "\n0.0 1.0 4.0 3.0 2.0 1.0 5.0"
                                   "\n0.0 0.0 0.0 0.0 0.0 2.0 6.0"
                                   "\n0.0 0.0 0.0 0.0 2.0 2.0 4.0"
                                   "\n0.0 0.0 0.0 9.0 2.0 1.0 6.0"
                                   "\n0.0 0.0 7.0 1.0 7.0 9.0 6.0",
                     }),

            TestCase(attach=TestClue("Test exactly like in the example",
                                     "out.txt", self.no_solutions),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "3 4\n0.0 1.0 2.0 9.0"
                                   "\n0.0 1.0 3.0 1.0"
                                   "\n1.0 0.0 6.0 0.0"
                                   "\n2.0 0.0 2.0 0.0"

                     }),

            TestCase(attach=TestClue("There are 4 rows, 3 columns, and a single solution",
                                     "out.txt", np.array([8.0, 1.0, 0.0])),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "3 4\n1.0 1.0 2.0 9.0"
                                   "\n0.0 1.0 3.0 1.0"
                                   "\n0.0 0.0 6.0 0.0"
                                   "\n0.0 0.0 0.0 0.0"

                     }),

            TestCase(attach=TestClue("There are 4 rows, 3 columns, and no solutions",
                                     "out.txt", self.no_solutions),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "3 4\n1.0 1.0 2.0 9.0"
                                   "\n0.0 1.0 3.0 1.0"
                                   "\n0.0 0.0 6.0 0.0"
                                   "\n0.0 0.0 0.0 7.0"

                     }),

            TestCase(attach=TestClue("There are 4 rows, 3 columns, and infinite solutions",
                                     "out.txt", self.infinite_solutions),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "3 4\n1.0 1.0 2.0 9.0"
                                   "\n0.0 1.0 3.0 1.0"
                                   "\n0.0 2.0 6.0 2.0"
                                   "\n0.0 0.0 0.0 0.0"

                     }),

            TestCase(attach=TestClue("There are 3 rows, 4 columns, and no solutions",
                                     "out.txt", self.no_solutions),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "4 3\n1.0 1.0 2.0 9.0 7.0"
                                   "\n0.0 1.0 3.0 1.0 2.0"
                                   "\n0.0 2.0 6.0 2.0 9.0"

                     }),

            TestCase(attach=TestClue("There are 3 rows, 4 columns, and infinite solutions",
                                     "out.txt", self.infinite_solutions),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "4 3\n1.0 1.0 2.0 9.0 7.0"
                                   "\n0.0 1.0 3.0 1.0 2.0"
                                   "\n0.0 2.0 6.0 3.0 9.0"

                     }),

            TestCase(attach=TestClue("There are 3 rows, 4 columns, and no solutions",
                                     "out.txt", self.no_solutions),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "4 3\n1.0 0.0 0.0 0.0 1.0"
                                   "\n0.0 0.0 0.0 0.0 0.0"
                                   "\n1.0 0.0 0.0 0.0 0.0"

                     }),

            TestCase(attach=TestClue("This is the first test with complex numbers. "
                                     "Maybe output format is wrong?",
                                     "out.txt", np.array([0.-1j, 0.-1j], dtype=complex)),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "2 2\n0.+1j 0.0 1.0"
                                   "\n0.0 0.+1j 1.0"
                     }, check_function=self.check_complex),

            TestCase(attach=TestClue("This test is about complex numbers.",
                                     "out.txt", self.no_solutions),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "2 2\n0.+1.j 0.-1.j 0.+1.j"
                                   "\n0.-1.j 0.+1.j 0.+1.j"
                     }, check_function=self.check_complex),

            TestCase(attach=TestClue("This test is about complex numbers.",
                                     "out.txt", self.infinite_solutions),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "2 2\n0.+1.j 0.-1.j 0.+1.j"
                                   "\n0.-1.j 0.+1.j 0.-1.j"
                     }, check_function=self.check_complex),

            TestCase(attach=TestClue("This test is about complex numbers.",
                                     "out.txt", np.array([-0.0879+0.1686j, -0.0707-0.0877j, 0.6987+0.8726j], dtype=complex)),
                     args=["--infile", "in.txt", "--outfile", "out.txt"],
                     files={
                         "in.txt": "3 3\n1.+1j 2.+6.j 7.-8.j 12.0"
                                   "\n0.-7.j 123.0 12.+1.j 0.+1.j"
                                   "\n11.-11.j 12.+1.j 0.-1.j 1.+1.j"
                     }, check_function=self.check_complex)


        ]

        return list_tests

    def check(self, reply: str, attach) -> CheckResult:
        try:
            with open(attach.out_file, 'r') as filik:
                try:
                    cor_answers = attach.answers
                    replyk = [i.strip().replace("[", "").replace("]", "").replace("'", "") for i in filik.readlines()]
                    hum_answers = np.array(list(map(lambda x: np.float64(x), replyk)))
                    n = hum_answers.size
                    if n != len(attach.answers):
                        return CheckResult.wrong(attach.feedback)
                    for i in range(n):
                        if abs(hum_answers[i] - cor_answers[i]) > 0.001:
                            return CheckResult.wrong(attach.feedback)
                except ValueError:
                    with open(attach.out_file, 'r') as filik:
                        hum_answer = filik.readline()
                        if hum_answer.strip() != attach.answers:
                            return CheckResult.wrong(attach.feedback)
        except IOError:
                return CheckResult.wrong("File doesn't exist or cannot be opened. "
                      "Did you close the file in your program?")
        return CheckResult.correct()

    def check_complex(self, reply: str, attach) -> CheckResult:
        try:
            with open(attach.out_file, 'r') as filik:
                try:
                    cor_answers = attach.answers
                    replyk = [i.strip().replace("[", "").replace("]", "").replace("'", "") for i in filik.readlines()]
                    if not replyk:
                        return CheckResult.wrong("The output file seems to be empty.")
                    hum_answers = np.array(list(map(lambda x: np.complex128(x), replyk)))
                    n = hum_answers.size
                    if n != len(attach.answers):
                        return CheckResult.wrong("The number of rows with answers in the output file is not correct.\n"
                                                 "{0} lines were expected, {1} lines were found.".format(len(attach.answers),
                                                                                                         n))
                    for i in range(n):
                        if abs(hum_answers[i] - cor_answers[i]) > 0.001:
                            return CheckResult.wrong("Answer {0} was expected, \n"
                                                     "but answer {1} was found.".format(cor_answers[i], hum_answers[i]))
                except ValueError:
                    with open(attach.out_file, 'r') as filik:
                        hum_answer = filik.readline()
                        if hum_answer.strip() != attach.answers:
                            return CheckResult.wrong("Answer \"{0}\" was expected, \n"
                                                     "but answer \"{1}\" was found.".format(attach.answers, hum_answer.strip()))
        except IOError:
                return CheckResult.wrong("File doesn't exist or cannot be opened. "
                      "Did you close the file in your program?")
        return CheckResult.correct()


if __name__ == '__main__':
    TestTheFifth('linear.solver').run_tests()
