from typing import List, Any
from hstest.stage_test import StageTest
from hstest.test_case import TestCase
from hstest.check_result import CheckResult
from hstest.exceptions import WrongAnswerException
import ast


class TestStage5(StageTest):
    first_move: bool

    def generate(self) -> List[TestCase]:
        list_of_funcs = [self.func1, self.func2, self.func3, self.func4, self.func5,
                         self.func6, self.func7, self.func8, (46, self.func9)]
        return [
            TestCase(stdin=list_of_funcs,
                     check_function=self.check_the_win),
            TestCase(stdin=list_of_funcs,
                     check_function=self.check_the_win),
            TestCase(stdin=list_of_funcs,
                     check_function=self.check_the_win),
            TestCase(stdin=list_of_funcs,
                     check_function=self.check_the_win),
            TestCase(stdin=list_of_funcs,
                     check_function=self.check_the_win),
            TestCase(stdin=list_of_funcs,
                     check_function=self.check_the_win),
            TestCase(stdin=list_of_funcs,
                     check_function=self.check_the_win),
            TestCase(stdin=list_of_funcs,
                     check_function=self.check_the_win),
        ]

    current_status = ""
    current_stock_size = 14
    current_computer_pieces = 7
    current_player_pieces = 6
    current_domino_snake = []
    chosen_piece = []
    left_end = []
    right_end = []

    def get_the_computer_pieces(self, output):
        """Get the amount of computer pieces"""

        output_parsed = self.parse_the_output(output)
        try:
            len_comp_pieces = int([i.strip() for i in output_parsed[2].split(':')][-1])
        except ValueError:
            raise WrongAnswerException("Make sure your output is formatted according to the examples")
        return len_comp_pieces

    def check_computer_pieces(self, output):
        """Check if the amount is right"""

        len_comp_pieces = self.get_the_computer_pieces(output)
        if len_comp_pieces != self.current_computer_pieces:
            return False
        return True

    def parse_the_output(self, output):
        """Parse the output"""

        out_parsed = [i.strip() for i in output.split('\n') if i]
        return out_parsed

    def get_the_stock(self, output):
        """Get the player's stock"""

        out_parsed = self.parse_the_output(output)
        try_stock = [i for i in out_parsed if ':[' in i.replace(' ', '')]
        try:
            the_stock = [ast.literal_eval(i[-6:]) for i in try_stock]
        except (ValueError, SyntaxError):
            raise WrongAnswerException("An error occurred while processing your output.\n"
                                       "Please make sure that your program's output is formatted exactly as described.")
        return the_stock

    def check_player_unique(self, output):
        """Check that the player pieces are uniqe"""

        uniq = self.get_the_stock(output)
        len1 = len(uniq)
        uniq = set([tuple(i) for i in uniq])
        len2 = len(uniq)
        if len1 != len2:
            return False
        return True

    def get_the_ends(self, output):
        """Get the ends of the domino snake"""

        try:
            domino_snake = self.parse_the_output(output)[3]
            self.left_end = ast.literal_eval(domino_snake[:6])
            self.right_end = ast.literal_eval(domino_snake[-6:])
        except (SyntaxError, ValueError, IndexError):
            raise WrongAnswerException("Make sure your output is formatted according to the examples")

    def choose_the_piece(self, output):
        """Choose the piece for the player to pick"""

        self.get_the_ends(output)
        try:
            end1 = self.left_end[0]
            end2 = self.right_end[1]
        except Exception:
            raise WrongAnswerException("Your output has wrong format! Make sure you print the pieces like in example!")
        player_stock = self.get_the_stock(output)
        for i, j in enumerate(player_stock):
            if end2 in j:
                return str(i + 1)
            elif end1 in j:
                return str(-(i + 1))
        else:
            return '0'

    def check_the_piece(self, output):
        """Check if the piece added is acceptable"""

        domino_snake = self.parse_the_output(output)[3]
        try:
            new1 = ast.literal_eval(domino_snake[:6])
            new2 = ast.literal_eval(domino_snake[-6:])
        except (ValueError, SyntaxError):
            raise WrongAnswerException("An error occurred while processing your output.\n"
                                       "Please make sure that your program's output is formatted exactly as described.")
        new_to_check = []
        if new1 != self.left_end:
            new_to_check = new1
        elif new2 != self.right_end:
            new_to_check = new2
        if new_to_check:
            if new_to_check[1] != self.left_end[0]:
                return False
            elif new_to_check[0] != self.right_end[1]:
                return False
        return True

    def check_the_design(self, output):
        """Check that the design is right"""

        output_parsed = self.parse_the_output(output)
        design = '=' * 70
        if output_parsed[0] != design:
            return False
        return True

    def get_stock_size(self, output):
        """Get the stock size"""

        output_parsed = self.parse_the_output(output)
        try:
            stock_size = int([i.strip() for i in output_parsed[1].split(':')][-1])
        except ValueError:
            raise WrongAnswerException("Make sure your output is formatted according to the examples")
        return stock_size

    def check_stock_size(self, output):
        """Check the stock size"""

        stock_size = self.get_stock_size(output)
        if stock_size != self.current_stock_size:
            return False
        return True

    def check_the_status(self, output):
        """Check if the status is correct"""

        output_parsed = self.parse_the_output(output)
        status_from_output = 'computer' if 'computer' in output_parsed[-1].lower() else 'player'
        if status_from_output != self.current_status:
            return False
        return True

    def choose_false(self, output):
        """Choose the piece for the player to pick"""

        self.get_the_ends(output)
        end1 = self.left_end[0]
        end2 = self.right_end[1]
        player_stock = self.get_the_stock(output)
        for i, j in enumerate(player_stock):
            if end2 not in j and end1 not in j:
                return str(i + 1)

    def check_the_move(self, output, to_fail=False, mistake=None):
        """Check the result when the computer made a move"""

        if not self.check_the_design(output):
            raise WrongAnswerException("The design is not right")
        if not self.check_stock_size(output):
            raise WrongAnswerException("The stock size is not right")
        if not self.check_computer_pieces(output):
            raise WrongAnswerException("The amount of computer pieces is not right")
        if not self.check_player_unique(output):
            raise WrongAnswerException("The player pieces are not unique")
        if not self.check_the_status(output):
            raise WrongAnswerException("The result is not right")
        if not self.check_the_piece(output):
            raise WrongAnswerException("The piece added is illegal")
        if 'computer is' in output.lower():
            self.current_status = 'player'
            return '\n'
        else:
            self.current_status = 'computer'
            if to_fail:
                return self.choose_false(output)
            if mistake is not None:
                return mistake
            else:
                return self.choose_the_piece(output)

    def set_the_currents(self, output):
        """Too random, need to consider computer options"""

        error = WrongAnswerException(
            f"Make sure you calculate the number of stock and computer pieces correctly")

        self.get_the_ends(output)
        if self.current_status == 'player':
            stock_dif = self.get_stock_size(output) - self.current_stock_size
            comp_dif = self.get_the_computer_pieces(output) - self.current_computer_pieces

            if self.first_move:
                if stock_dif != 0 or comp_dif != 0:
                    raise error
                else:
                    return

            # if the computer took a piece from the stock
            if stock_dif == -1 and comp_dif == 1:
                self.current_computer_pieces += 1
                self.current_stock_size -= 1
            # if the computer made a move
            elif stock_dif == 0 and comp_dif == -1:
                self.current_computer_pieces -= 1
            elif self.get_stock_size(output) == 0:
                return
            else:
                raise error

        elif self.current_status == 'computer':
            stock_dif = self.get_stock_size(output) - self.current_stock_size
            player_dif = len(self.get_the_stock(output)) - self.current_player_pieces

            if self.first_move:
                if stock_dif != 0 or player_dif != 0:
                    raise error
                else:
                    return

            # if player took piece from the
            if stock_dif == -1 and player_dif == 1:
                self.current_player_pieces += 1
                self.current_stock_size -= 1
            # if the player made a move
            elif stock_dif == 0 and player_dif == -1:
                self.current_player_pieces -= 1
            elif self.get_stock_size(output) == 0:
                return
            else:
                raise error

    def func1(self, output):
        self.chosen_piece = []
        if "computer is" in output.lower():
            self.current_stock_size = 14
            self.current_player_pieces = 6
            self.current_computer_pieces = 7
            self.current_status = 'computer'
        else:
            self.current_stock_size = 14
            self.current_player_pieces = 7
            self.current_computer_pieces = 6
            self.current_status = 'player'

        self.first_move = True
        self.set_the_currents(output)
        self.first_move = False
        return self.check_the_move(output)

    def func2(self, output):
        self.set_the_currents(output)
        return self.check_the_move(output)

    def func3(self, output):
        self.set_the_currents(output)
        self.chosen_piece = self.choose_the_piece(output)
        return self.check_the_move(output, to_fail=True)

    def func4(self, output):
        if self.current_status == 'computer':
            if "illegal move. please try again" not in output.lower():
                return CheckResult.wrong("The player should be informed about tne incorrect move")
            return self.chosen_piece
        else:
            self.set_the_currents(output)
            return self.check_the_move(output)

    def func5(self, output):
        self.set_the_currents(output)
        return self.check_the_move(output)

    def func6(self, output):
        self.set_the_currents(output)
        self.chosen_piece = self.choose_the_piece(output)
        return self.check_the_move(output, mistake='-25')

    def func7(self, output):
        if self.current_status == 'computer':
            if "invalid input. please try again." not in output.lower():
                return CheckResult.wrong("The player should be informed about tne incorrect move")
            return self.chosen_piece
        else:
            self.set_the_currents(output)
            return self.check_the_move(output)

    def func8(self, output):
        self.set_the_currents(output)
        return self.check_the_move(output)

    def func9(self, output):
        self.set_the_currents(output)
        return self.check_the_move(output)

    def check_the_win(self, reply: str, attach: Any) -> CheckResult:
        design = '=' * 70
        if not reply:
            raise WrongAnswerException("The reply is empty. Please, output the required data.")
        reply_parsed = reply.split(design)
        the_last = [i.strip() for i in reply_parsed[-1].strip().split('\n') if i]
        try:
            comp_pieces = int([i.strip() for i in the_last[1].split(':') if i][-1])
        except Exception:
            raise WrongAnswerException("Make sure you output pieces in the required format.")

        last_output = reply_parsed[-1].replace(' ', '')
        # check for the win
        if '1:[' not in last_output:
            if ':[' in last_output or comp_pieces == 0:
                return CheckResult.wrong("The result is wrong")
            if "the game is over. you won" not in the_last[-1].lower():
                return CheckResult.wrong("The status is not right")
        # check for the computer win
        elif int(the_last[1][-1]) == 0:
            if ':[' not in last_output or comp_pieces > 0:
                return CheckResult.wrong("The result is wrong")
            if "the game is over. the computer won" not in the_last[-1].lower():
                return CheckResult.wrong("The status is not right")
        else:
            if "the game is over. it's a draw" not in the_last[-1].lower():
                return CheckResult.wrong("The status is not right")
        return CheckResult.correct()


if __name__ == '__main__':
    TestStage5('dominoes.dominoes').run_tests()
