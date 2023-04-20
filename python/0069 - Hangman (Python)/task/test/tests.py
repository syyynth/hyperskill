import re
from typing import List

from hstest import StageTest, dynamic_test, TestedProgram, WrongAnswer, CheckResult
from string import ascii_lowercase
from random import shuffle, randint


class LetterAlreadyOpenedError(Exception):

    def __init__(self, letter: str):
        self.letter = letter


class CorrectLettersToOpenOverError(Exception):
    pass


class IncorrectLettersToOpenOverError(Exception):
    pass


class EmptyOpenedLettersError(Exception):
    pass


class TriesOverError(Exception):
    pass


class OutputContainsInputAnnouncementError(Exception):
    pass


class OutputContainsMoreThanOneLetterMessageError(Exception):
    pass


class OutputNotContainsMoreThanOneLetterMessageError(Exception):
    pass


class OutputContainsReopenLetterMessageError(Exception):
    pass


class OutputNotContainsReopenLetterMessageError(Exception):
    pass


class OutputNotContainsInputAnnouncementError(Exception):
    pass


class OutputContainsIncorrectLetterMessageError(Exception):
    pass


class OutputNotContainsIncorrectLetterMessageError(Exception):
    pass


class OutputContainsSurvivedMessageError(Exception):
    pass


class OutputContainsGuessedWordMessageError(Exception):
    pass


class OutputNotContainsGuessedWordMessageError(Exception):
    pass


class OutputNotContainsSurvivedMessageError(Exception):
    pass


class OutputContainsHangedMessageError(Exception):
    pass


class OutputNotContainsHangedMessageError(Exception):
    pass


class OutputContainsNonAsciiLetterMessageError(Exception):
    pass


class OutputNotContainsNonAsciiLetterMessageError(Exception):
    pass


class WrongLinesCountError(Exception):
    pass


class InitialMaskContainsInvalidCharactersError(Exception):
    pass


class IncorrectMaskTransitionError(Exception):
    pass


class GameOverException(Exception):
    pass


class Config:
    SURVIVED_MESSAGE = 'You survived!'
    HANGED_MESSAGE = 'You lost!'
    MAX_TRIES = 8
    INPUT_ANNOUNCEMENT = 'Input a letter'
    INCORRECT_LETTER_MESSAGE = 'That letter doesn\'t appear in the word'
    GUESSED_THE_WORD_MESSAGE = 'You guessed the word #LANGUAGE#!'
    REOPEN_LETTER_MESSAGE = 'You\'ve already guessed this letter'
    MORE_THAN_ONE_LETTER_MESSAGE = 'Please, input a single letter'
    NON_ASCII_LETTER_MESSAGE = 'Please, enter a lowercase letter from the English alphabet'
    GAME_MENU_TEXT = 'Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit'

    @staticmethod
    def languages():
        return [
            'java',
            'python',
            'swift',
            'javascript',
        ]

    @classmethod
    def mask_language_map(cls):
        return {cls.make_language_mask(language): language for language in cls.languages()}

    @classmethod
    def make_language_mask(cls, word):
        return '-' * len(word)


class GameState:

    def __init__(self, program: TestedProgram, language: str, tries: int):
        self.program = program
        self.language = language
        self.tries = tries
        self.correct_letters_to_open = self._language_correct_letters(language)
        self.incorrect_letters_to_open = self._language_incorrect_letters(language)
        self.opened_correct_letters = []
        self.all_opened_letters = []
        self.current_input = None
        self.output = None
        self.current_language_mask = self._language_mask(language, self.opened_correct_letters)
        self.prev_language_mask = self._language_mask(language, self.opened_correct_letters)
        shuffle(self.correct_letters_to_open)
        shuffle(self.incorrect_letters_to_open)
        self.correct_letters_to_open *= tries

    def open_correct_letter(self):
        letter = self._next_correct_letter_to_open()

        if letter in self.opened_correct_letters:
            raise LetterAlreadyOpenedError(letter)

        if letter in self.all_opened_letters:
            raise LetterAlreadyOpenedError(letter)

        self.current_input = letter
        self.output = self.program.execute(self.current_input).strip()
        self.opened_correct_letters.append(self.current_input)
        self.all_opened_letters.append(letter)
        self._update_language_mask()

    def open_incorrect_letter(self):
        letter = self._next_incorrect_letter_to_open()

        if letter not in self.all_opened_letters:
            self.all_opened_letters.append(letter)

        self.current_input = letter
        self.output = self.program.execute(self.current_input).strip()
        self._decrease_tries_count()
        self._update_language_mask()

    def reopen_letter(self):
        if not len(self.all_opened_letters):
            raise EmptyOpenedLettersError()

        letter = self.all_opened_letters[0]
        self.current_input = letter
        self.output = self.program.execute(letter).strip()
        self._update_language_mask()

    def pass_more_than_one_letter(self):
        letters = ['aa', 'cc', '', 'xx', 'asd']
        shuffle(letters)
        letters = letters[0]
        self.current_input = letters
        self.output = self.program.execute(letters).strip()

    def pass_not_lowercase_letter(self):
        letters = list('A-+09JSKIE*')
        shuffle(letters)
        letter = letters[0]
        self.current_input = letter
        self.output = self.program.execute(letter).strip()

    def _decrease_tries_count(self):
        if self.tries <= 0:
            raise TriesOverError()

        self.tries -= 1

    def _update_language_mask(self):
        self.prev_language_mask = self.current_language_mask
        self.current_language_mask = self._language_mask(self.language, self.opened_correct_letters)

    def _next_correct_letter_to_open(self):
        if len(self.correct_letters_to_open) <= 0:
            raise CorrectLettersToOpenOverError()

        return self.correct_letters_to_open.pop()

    def _next_incorrect_letter_to_open(self):
        if len(self.incorrect_letters_to_open) <= 0:
            raise IncorrectLettersToOpenOverError()

        return self.incorrect_letters_to_open.pop()

    @property
    def game_ended(self) -> bool:
        return self.hanged or self.survived

    @property
    def hanged(self) -> bool:
        return self.tries <= 0

    @property
    def survived(self) -> bool:
        return self.current_language_mask == self.language

    @property
    def letters_to_open(self):
        return len(list(set(self.language))) - len(self.opened_correct_letters)

    @property
    def guessed_word_message(self):
        return Config.GUESSED_THE_WORD_MESSAGE.replace('#LANGUAGE#', self.language)

    @classmethod
    def _language_mask(cls, language: str, opened_letters: list):
        language_letters = list(language)
        mask = ''

        for letter in language_letters:
            mask += letter if letter in opened_letters else '-'

        return mask

    @classmethod
    def _language_correct_letters(cls, language: str) -> List[str]:
        return list(set(language))

    @classmethod
    def _language_incorrect_letters(cls, language: str) -> List[str]:
        return list(set(ascii_lowercase).difference(set(language)))


class ValidationHelper:

    @classmethod
    def output_should_contains_input_announcement(cls, output: str):
        input_announcement = Config.INPUT_ANNOUNCEMENT

        if input_announcement.lower() not in output.lower():
            raise OutputNotContainsInputAnnouncementError()

    @classmethod
    def output_should_not_contains_input_announcement(cls, output: str):
        input_announcement = Config.INPUT_ANNOUNCEMENT

        if input_announcement.lower() in output.lower():
            raise OutputContainsInputAnnouncementError()

    @classmethod
    def output_should_contains_reopen_letter_message(cls, output: str):
        message = Config.REOPEN_LETTER_MESSAGE

        if message.lower() not in output.lower():
            raise OutputNotContainsReopenLetterMessageError

    @classmethod
    def output_should_not_contains_reopen_letter_message(cls, output: str):
        message = Config.REOPEN_LETTER_MESSAGE

        if message.lower() in output.lower():
            raise OutputContainsReopenLetterMessageError

    @classmethod
    def output_should_contains_incorrect_letter_message(cls, output: str):
        message = Config.INCORRECT_LETTER_MESSAGE

        if message.lower() not in output.lower():
            raise OutputNotContainsIncorrectLetterMessageError()

    @classmethod
    def output_should_not_contains_incorrect_letter_message(cls, output: str):
        message = Config.INCORRECT_LETTER_MESSAGE

        if message.lower() in output.lower():
            raise OutputContainsIncorrectLetterMessageError()

    @classmethod
    def output_should_contains_guessed_the_word_message(cls, output: str, language: str):
        message = Config.GUESSED_THE_WORD_MESSAGE.replace('#LANGUAGE#', language)

        if message.lower() not in output.lower():
            raise OutputNotContainsGuessedWordMessageError()

    @classmethod
    def output_should_not_contains_guessed_the_word_message(cls, output: str):
        message = Config.GUESSED_THE_WORD_MESSAGE

        if message.lower() in output.lower():
            raise OutputContainsGuessedWordMessageError()

    @classmethod
    def output_should_contains_survived_message(cls, output: str):
        message = Config.SURVIVED_MESSAGE

        if message.lower() not in output.lower():
            raise OutputNotContainsSurvivedMessageError()

    @classmethod
    def output_should_contains_hanged_message(cls, output: str):
        message = Config.HANGED_MESSAGE

        if message.lower() not in output.lower():
            raise OutputNotContainsHangedMessageError()

    @classmethod
    def output_should_not_contains_hanged_message(cls, output: str):
        message = Config.HANGED_MESSAGE

        if message.lower() in output.lower():
            raise OutputContainsHangedMessageError()

    @classmethod
    def output_should_not_contains_survived_message(cls, output: str):
        message = Config.SURVIVED_MESSAGE

        if message.lower() in output.lower():
            raise OutputContainsSurvivedMessageError()

    @classmethod
    def output_should_contains_more_than_one_letter_message(cls, output: str):
        message = Config.MORE_THAN_ONE_LETTER_MESSAGE

        if message.lower() not in output.lower():
            raise OutputNotContainsMoreThanOneLetterMessageError()

    @classmethod
    def output_should_not_contains_more_than_one_letter_message(cls, output: str):
        message = Config.MORE_THAN_ONE_LETTER_MESSAGE

        if message.lower() in output.lower():
            raise OutputContainsMoreThanOneLetterMessageError()

    @classmethod
    def output_should_contains_non_ascii_letter_message(cls, output: str):
        message = Config.NON_ASCII_LETTER_MESSAGE

        if message.lower() not in output.lower():
            raise OutputNotContainsNonAsciiLetterMessageError()

    @classmethod
    def output_should_not_contains_non_ascii_letter_message(cls, output: str):
        message = Config.NON_ASCII_LETTER_MESSAGE

        if message.lower() in output.lower():
            raise OutputContainsNonAsciiLetterMessageError()

    @classmethod
    def validate_min_lines_count(cls, lines: list, lines_count: int):
        if len(lines) < lines_count:
            raise WrongLinesCountError()

    @classmethod
    def initial_mask_should_contains_only_valid_characters(cls, mask: str):
        if len(mask.replace('-', '')):
            raise InitialMaskContainsInvalidCharactersError()


class LanguageMaskParser:

    def __init__(self, output: str):
        self.output = output
        self.helper = ValidationHelper()
        self.mask_line = 1
        self.lines = []
        self.mask = ''

    def parse(self):
        try:
            self.helper.output_should_contains_input_announcement(self.output)
            self.lines = self._get_lines_from_output()
            self.helper.validate_min_lines_count(self.lines, self.mask_line)
            self.mask = self._get_mask_from_lines()
            self.helper.initial_mask_should_contains_only_valid_characters(self.mask)
            language = self._get_language_from_mask()
        except OutputNotContainsInputAnnouncementError:
            raise WrongAnswer("The output doesn't contain any \"Input a letter\" lines.")
        except WrongLinesCountError:
            raise WrongAnswer(f"Cannot recognize a word from the mask. The mask should be on {self.mask_line} "
                              f"line but there are less than {self.mask_line} lines in the output.")
        except InitialMaskContainsInvalidCharactersError:
            raise WrongAnswer(f"Cannot recognize a word from the mask. "
                              f"The mask \"{self.mask}\" contains non-dash characters.")

        if language is None:
            raise WrongAnswer(f"Cannot recognize a word from the mask \"{self.mask}\". "
                              f"Did you only use the words from the description?")

        return language

    def _get_lines_from_output(self):
        return self.output.strip().split('\n')

    def _get_mask_from_lines(self):
        return self.lines[self.mask_line - 1]

    def _get_language_from_mask(self):
        for language_mask, language in Config.mask_language_map().items():
            if language_mask == self.mask:
                return language

        return None


class GameCommand:

    def __init__(self):
        self.helper = ValidationHelper()
        self.state = None

    def handle(self, state: GameState):
        self.state = state

        try:
            self.change_state()
            self.verify_on_game_end()
            self.validate_mask_transition()
            self.validate_output()
        except EmptyOpenedLettersError:
            pass
        except OutputNotContainsInputAnnouncementError:
            raise WrongAnswer("The output doesn't contain any \"Input a letter\" lines.")
        except OutputContainsInputAnnouncementError:
            raise WrongAnswer(f"The last block should not contain text \"{Config.INPUT_ANNOUNCEMENT}\".")
        except OutputContainsIncorrectLetterMessageError:
            raise WrongAnswer(f"The output contains \"{Config.INCORRECT_LETTER_MESSAGE}\" message, "
                              f"but a letter \"{self.state.current_input}\" "
                              f"is present in the word \"{self.state.language}\".")
        except OutputNotContainsIncorrectLetterMessageError:
            raise WrongAnswer(f"The output doesn't contain \"{Config.INCORRECT_LETTER_MESSAGE}\" message, "
                              f"but a letter \"{self.state.current_input}\" doesn't appear"
                              f" in the word \"{self.state.language}\".")
        except IncorrectMaskTransitionError:
            raise WrongAnswer(f'Incorrect mask transition. Cannot find correct mask in the output:\n'
                              f'Word: {self.state.language}\n'
                              f'Letter: {self.state.current_input}\n'
                              f'Previous mask: {self.state.prev_language_mask}\n'
                              f'Correct current mask: {self.state.current_language_mask}\n')
        except OutputContainsHangedMessageError:
            raise WrongAnswer(f'The user is hanged, but there are {self.state.tries} lives left.')
        except OutputNotContainsHangedMessageError:
            raise WrongAnswer(f'The user is hanged, but there is no \"{Config.HANGED_MESSAGE}\" message in the output.')
        except OutputContainsSurvivedMessageError:
            raise WrongAnswer(f'The user survived, but there are {self.state.letters_to_open} letters to open.')
        except OutputNotContainsSurvivedMessageError:
            raise WrongAnswer(
                f'The user survived, but there is no \"{Config.SURVIVED_MESSAGE}\" message in the output.')
        except OutputNotContainsGuessedWordMessageError:
            raise WrongAnswer(
                f'The user survived. The last block should contain text \"{self.state.guessed_word_message}\"')
        except OutputContainsGuessedWordMessageError:
            raise WrongAnswer(
                f'The user is hanged. The last block should not contain text \"{Config.GUESSED_THE_WORD_MESSAGE}\".'
            )
        except OutputContainsReopenLetterMessageError:
            raise WrongAnswer(f'The output contains \"{Config.REOPEN_LETTER_MESSAGE}\" message, '
                              f'but a letter \"{self.state.current_input}\" hasn\'t been suggested yet.')
        except OutputNotContainsReopenLetterMessageError:
            raise WrongAnswer(f'The output doesn\'t contain \"{Config.REOPEN_LETTER_MESSAGE}\" message, '
                              f'but a letter \"{self.state.current_input}\" has already been suggested.')
        except OutputContainsMoreThanOneLetterMessageError:
            raise WrongAnswer(f'The output contains \"{Config.MORE_THAN_ONE_LETTER_MESSAGE}\" message, '
                              f'but a single letter \"{self.state.current_input}\" was provided.')
        except OutputNotContainsMoreThanOneLetterMessageError:
            raise WrongAnswer(f'The output doesn\'t contain \"{Config.MORE_THAN_ONE_LETTER_MESSAGE}\" message, '
                              f'but letters \"{self.state.current_input}\" were provided.')
        except OutputContainsNonAsciiLetterMessageError:
            raise WrongAnswer(f'The output contains \"{Config.NON_ASCII_LETTER_MESSAGE}\" message, '
                              f'but a letter \"{self.state.current_input}\" was provided.')
        except OutputNotContainsNonAsciiLetterMessageError:
            raise WrongAnswer(f'The output doesn\'t contain \"{Config.NON_ASCII_LETTER_MESSAGE}\" message, '
                              f'but a symbol \"{self.state.current_input}\" was provided.')

    def change_state(self):
        pass

    def validate_output(self):
        pass

    def validate_end_game_output(self):
        pass

    def validate_mask_transition(self):
        lines = self._get_lines_from_output(self.state.output)

        for line in lines:
            if line.strip() == self.state.current_language_mask:
                return

        raise IncorrectMaskTransitionError

    def verify_on_game_end(self):
        if not self.state.game_ended:
            return

        self.validate_end_game_output()
        raise GameOverException

    @classmethod
    def _get_lines_from_output(cls, output: str):
        return output.strip().split('\n')


class OpenCorrectLetterCommand(GameCommand):

    def change_state(self):
        self.state.open_correct_letter()

    def validate_output(self):
        output = self.state.output
        self.helper.output_should_contains_input_announcement(output)
        self.helper.output_should_not_contains_incorrect_letter_message(output)
        self.helper.output_should_not_contains_hanged_message(output)
        self.helper.output_should_not_contains_survived_message(output)
        self.helper.output_should_not_contains_reopen_letter_message(output)
        self.helper.output_should_not_contains_more_than_one_letter_message(output)

    def validate_end_game_output(self):
        output = self.state.output
        self.helper.output_should_contains_survived_message(output)
        self.helper.output_should_contains_guessed_the_word_message(output, self.state.language)
        self.helper.output_should_not_contains_input_announcement(output)
        self.helper.output_should_not_contains_hanged_message(output)
        self.helper.output_should_not_contains_reopen_letter_message(output)
        self.helper.output_should_not_contains_more_than_one_letter_message(output)


class OpenIncorrectLetterCommand(GameCommand):

    def change_state(self):
        self.state.open_incorrect_letter()

    def validate_output(self):
        output = self.state.output
        self.helper.output_should_contains_input_announcement(output)
        self.helper.output_should_contains_incorrect_letter_message(output)
        self.helper.output_should_not_contains_hanged_message(output)
        self.helper.output_should_not_contains_survived_message(output)
        self.helper.output_should_not_contains_reopen_letter_message(output)
        self.helper.output_should_not_contains_more_than_one_letter_message(output)

    def validate_end_game_output(self):
        output = self.state.output
        self.helper.output_should_contains_hanged_message(output)
        self.helper.output_should_not_contains_input_announcement(output)
        self.helper.output_should_not_contains_survived_message(output)
        self.helper.output_should_not_contains_guessed_the_word_message(output)
        self.helper.output_should_not_contains_reopen_letter_message(output)
        self.helper.output_should_not_contains_more_than_one_letter_message(output)


class ReopenLetterCommand(GameCommand):

    def change_state(self):
        self.state.reopen_letter()

    def validate_output(self):
        output = self.state.output
        self.helper.output_should_contains_input_announcement(output)
        self.helper.output_should_contains_reopen_letter_message(output)
        self.helper.output_should_not_contains_hanged_message(output)
        self.helper.output_should_not_contains_survived_message(output)
        self.helper.output_should_not_contains_more_than_one_letter_message(output)

    def validate_end_game_output(self):
        output = self.state.output
        self.helper.output_should_contains_hanged_message(output)
        self.helper.output_should_contains_reopen_letter_message(output)
        self.helper.output_should_not_contains_input_announcement(output)
        self.helper.output_should_not_contains_survived_message(output)
        self.helper.output_should_not_contains_more_than_one_letter_message(output)


class OpenMoreThanOneLetterCommand(GameCommand):

    def change_state(self):
        self.state.pass_more_than_one_letter()

    def validate_output(self):
        output = self.state.output
        self.helper.output_should_contains_input_announcement(output)
        self.helper.output_should_contains_more_than_one_letter_message(output)
        self.helper.output_should_not_contains_hanged_message(output)
        self.helper.output_should_not_contains_survived_message(output)
        self.helper.output_should_not_contains_reopen_letter_message(output)


class OpenNonAsciiLetterCommand(GameCommand):

    def change_state(self):
        self.state.pass_not_lowercase_letter()

    def validate_output(self):
        output = self.state.output
        self.helper.output_should_contains_input_announcement(output)
        self.helper.output_should_contains_non_ascii_letter_message(output)
        self.helper.output_should_not_contains_hanged_message(output)
        self.helper.output_should_not_contains_survived_message(output)


class TestCommandsCollection:

    @classmethod
    def survived(cls):
        language_lengths = [len(language) for language in Config.languages()]
        max_length = max(language_lengths)
        valid_commands = [OpenCorrectLetterCommand() for _ in range(max_length)]
        invalid_commands = [OpenIncorrectLetterCommand() for _ in range(2)]
        invalid_commands += [ReopenLetterCommand() for _ in range(2)]
        skip_commands = [OpenMoreThanOneLetterCommand() for _ in range(4)]
        skip_commands += [OpenNonAsciiLetterCommand() for _ in range(4)]
        commands = valid_commands + invalid_commands + skip_commands
        shuffle(commands)

        return commands

    @classmethod
    def hanged(cls):
        language_lengths = [len(language) for language in Config.languages()]
        min_length = min(language_lengths)
        valid_commands = [OpenCorrectLetterCommand() for _ in range(min_length - 1)]
        invalid_commands = [OpenIncorrectLetterCommand() for _ in range(Config.MAX_TRIES)]
        skip_commands = [OpenMoreThanOneLetterCommand() for _ in range(4)]
        skip_commands += [OpenNonAsciiLetterCommand() for _ in range(4)]
        commands = valid_commands + invalid_commands + skip_commands
        shuffle(commands)

        return commands


class GameMenu:

    def __init__(self, program: TestedProgram):
        self.program = program

    def play(self) -> str:
        return self.program.execute('play')

    def exit(self):
        self.program.execute('exit')

    def scoreboard(self):
        return self.program.execute('results')

    @classmethod
    def output_should_contains_menu(cls, output: str):
        if Config.GAME_MENU_TEXT not in output.strip():
            raise WrongAnswer(
                f'The output doesn\'t contain game menu text: \"{Config.GAME_MENU_TEXT}\". Please, make sure that you '
                f'output the text exactly as in the example task.')


class Scoreboard:

    @staticmethod
    def output_should_contains_scoreboard(wins: int, loses: int, output: str):
        wins_text = f'You won: {wins} times'
        loses_text = f'You lost: {loses} times'
        scoreboard = re.sub(" +", " ", output.strip())

        if wins_text not in scoreboard:
            raise WrongAnswer(f'Invalid scoreboard. The output should contain: \"{wins_text}\". Please, check the '
                              f'correctness of the output of wins.')

        if loses_text not in scoreboard:
            raise WrongAnswer(f'Invalid scoreboard. The output should contain: \"{loses_text}\". Please, check the '
                              f'correctness of the output of loses.')


class HangmanTest(StageTest):

    def __init__(self, source_name: str = ''):
        super().__init__(source_name)
        self.helper = ValidationHelper()
        self.survived_history = {language: False for language in Config.languages()}
        self.hanged_history = {language: False for language in Config.languages()}

    @dynamic_test(order=1)
    def test_should_print_game_menu(self):
        pr = TestedProgram(self.source_name)
        game_menu = GameMenu(pr)
        first_block = pr.start().strip()
        game_menu.output_should_contains_menu(first_block)

        return CheckResult.correct()

    @dynamic_test(order=2)
    def test_should_can_replay_game(self):
        pr = TestedProgram(self.source_name)
        game_menu = GameMenu(pr)
        first_block = pr.start().strip()
        game_menu.output_should_contains_menu(first_block)

        parser = LanguageMaskParser(game_menu.play())
        language = parser.parse()

        game_state = GameState(program=pr, language=language, tries=Config.MAX_TRIES)
        commands = TestCommandsCollection.survived()
        self._run_commands(commands, game_state)

        game_menu.output_should_contains_menu(game_state.output)
        parser = LanguageMaskParser(game_menu.play())
        language = parser.parse()

        game_state = GameState(program=pr, language=language, tries=Config.MAX_TRIES)
        commands = TestCommandsCollection.survived()
        self._run_commands(commands, game_state)
        game_menu.exit()

        return CheckResult.correct()

    @dynamic_test(order=3)
    def test_should_quit_after_exit_command(self):
        pr = TestedProgram(self.source_name)
        game_menu = GameMenu(pr)
        first_block = pr.start().strip()
        game_menu.output_should_contains_menu(first_block)

        parser = LanguageMaskParser(game_menu.play())
        language = parser.parse()
        game_state = GameState(program=pr, language=language, tries=Config.MAX_TRIES)
        commands = TestCommandsCollection.survived()
        self._run_commands(commands, game_state)
        game_menu.output_should_contains_menu(game_state.output)
        game_menu.exit()

        if not pr.is_finished():
            raise WrongAnswer(f'The program should be terminated after \"exit\" command.')

        return CheckResult.correct()

    @dynamic_test(order=4)
    def test_game_should_output_correct_scoreboard(self):
        wins = 0
        loses = 0
        pr = TestedProgram(self.source_name)
        game_menu = GameMenu(pr)
        first_block = pr.start().strip()
        game_menu.output_should_contains_menu(first_block)
        Scoreboard.output_should_contains_scoreboard(wins=wins, loses=loses, output=game_menu.scoreboard())

        parser = LanguageMaskParser(game_menu.play())
        language = parser.parse()
        game_state = GameState(program=pr, language=language, tries=Config.MAX_TRIES)
        commands = TestCommandsCollection.survived()
        self._run_commands(commands, game_state)
        wins += 1

        game_menu.output_should_contains_menu(game_state.output)
        Scoreboard.output_should_contains_scoreboard(wins=wins, loses=loses, output=game_menu.scoreboard())

        parser = LanguageMaskParser(game_menu.play())
        language = parser.parse()
        game_state = GameState(program=pr, language=language, tries=Config.MAX_TRIES)
        commands = TestCommandsCollection.hanged()
        self._run_commands(commands, game_state)
        loses += 1

        game_menu.output_should_contains_menu(game_state.output)
        Scoreboard.output_should_contains_scoreboard(wins=wins, loses=loses, output=game_menu.scoreboard())

        game_menu.exit()

        return CheckResult.correct()

    @dynamic_test(order=5, repeat=100)
    def test_all_languages_from_description_should_can_be_guessed(self):
        if self._all_languages_from_description_was_guessed_at_least_once():
            return CheckResult.correct()

        pr = TestedProgram(self.source_name)
        game_menu = GameMenu(pr)
        first_block = pr.start().strip()
        game_menu.output_should_contains_menu(first_block)

        parser = LanguageMaskParser(game_menu.play())
        language = parser.parse()
        game_state = GameState(program=pr, language=language, tries=Config.MAX_TRIES)
        commands = TestCommandsCollection.survived()
        self._run_commands(commands, game_state)
        self._store_language_to_survived_history(language)

        return CheckResult.correct()

    @dynamic_test(order=6)
    def test_all_languages_from_description_should_be_guessed_at_least_once(self):
        if self._all_languages_from_description_was_guessed_at_least_once():
            return CheckResult.correct()

        raise WrongAnswer("It looks like your program is not using "
                          "all of the words to guess from the list in the description.")

    @dynamic_test(order=7, repeat=100)
    def test_all_languages_from_description_should_be_incorrect_at_least_once(self):
        if self._all_languages_from_description_was_incorrect_at_least_once():
            return CheckResult.correct()

        pr = TestedProgram(self.source_name)
        game_menu = GameMenu(pr)
        first_block = pr.start().strip()
        game_menu.output_should_contains_menu(first_block)

        parser = LanguageMaskParser(game_menu.play())
        language = parser.parse()

        game_state = GameState(program=pr, language=language, tries=Config.MAX_TRIES)
        commands = TestCommandsCollection.hanged()
        self._run_commands(commands, game_state)
        self._store_language_to_hanged_history(language)

        return CheckResult.correct()

    def _store_language_to_survived_history(self, language: str):
        self.survived_history[language] = True

    def _store_language_to_hanged_history(self, language: str):
        self.hanged_history[language] = True

    def _all_languages_from_description_was_guessed_at_least_once(self):
        return all(self.survived_history.values())

    def _all_languages_from_description_was_incorrect_at_least_once(self):
        return all(self.hanged_history.values())

    @classmethod
    def _run_commands(cls, commands: List[GameCommand], game_state: GameState):
        try:
            for command in commands:
                command.handle(game_state)
        except GameOverException:
            pass


if __name__ == '__main__':
    HangmanTest('hangman.hangman').run_tests()
