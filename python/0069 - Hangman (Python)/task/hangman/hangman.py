import random
import string

print('H A N G M A N\n')

OPTIONS: list[str] = ['python', 'java', 'swift', 'javascript']
LETTERS: set[str] = set(string.ascii_lowercase)
STATS: dict[str, int] = {'won': 0, 'lost': 0}


def print_results() -> None:
    """ Print the current statistics; wins and loses. """
    print(f'You won: {STATS["won"]} times.')
    print(f'You lost: {STATS["lost"]} times.')


def validate(guess: str, guessed: set[str], answer: list[str]) -> tuple[str, int]:
    """ Check if the guess is valid and return a message and a cost. """
    if len(guess) != 1:
        return 'Please, input a single letter.', 0
    if guess not in LETTERS:
        return 'Please, enter a lowercase letter from the English alphabet.', 0
    if guess in guessed:
        return "You've already guessed this letter.", 0
    if guess not in answer:
        return "That letter doesn't appear in the word.", 1
    return 'Good guess! Open the letter!', 0


def main() -> None:
    max_moves: int = 8
    answer: list[str] = [*random.choice(OPTIONS)]
    opened: list[str] = ['-'] * len(answer)
    guessed: set[str] = set()

    while max_moves and '-' in opened:
        print(''.join(opened))

        guess = input('\nInput a letter:')

        msg, cost = validate(guess, guessed, answer)

        print(msg)
        max_moves -= cost

        guessed.add(guess)
        for idx, c in enumerate(answer):
            if c == guess:
                opened[idx] = guess

    if answer == opened:
        print(f'You guessed the word {"".join(answer)}!')
        print('You survived!')
        STATS["won"] += 1
    else:
        print('You lost!')
        STATS["lost"] += 1


while True:
    print('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit:')
    match input():
        case 'play':
            main()
        case 'results':
            print_results()
        case 'exit':
            break
