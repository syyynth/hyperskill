import random

OPERATION_MAP = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y
}
QUESTIONS_AMOUNT = 5
SAVE_CHOICES = ['yes', 'YES', 'y', 'Yes']
LEVEL_HELP = {
    1: 'simple operations with numbers 2-9',
    2: 'integral squares of 11-29'
}


def generate_expression() -> tuple[int, int, str]:
    x = random.randint(2, 9)
    y = random.randint(2, 9)
    op = random.choice(list(OPERATION_MAP))
    return x, y, op


def get_question(x: int, y: int, op: str) -> tuple[str, float]:
    return f'{x} {op} {y}', OPERATION_MAP[op](x, y)


def check_answer(expected: float, given: str) -> bool:
    try:
        return expected == float(given)
    except ValueError:
        return False


def generate_square() -> tuple[int, int]:
    num = random.randint(11, 29)
    return num, num * num


def ask_question(level: int) -> bool:
    if level == 1:
        question, correct_answer = get_question(*generate_expression())
    elif level == 2:
        question, correct_answer = generate_square()
    else:
        raise ValueError(f'Unknown level: {level}')

    print(question)
    given_answer = get_answer()
    is_correct = check_answer(correct_answer, given_answer)
    print('Right!' if is_correct else 'Wrong!')
    return is_correct


def get_answer() -> str:
    while True:
        given_answer = input().strip()
        try:
            float(given_answer)
            return given_answer
        except ValueError:
            print('Incorrect format.')


def get_level() -> int:
    while True:
        print('Which level do you want? Enter a number:\n'
              f'1 - {LEVEL_HELP[1]}\n'
              f'2 - {LEVEL_HELP[2]}\n')
        try:
            lvl = int(input().strip())
            if lvl in LEVEL_HELP:
                return lvl
        except ValueError:
            print('Incorrect format.')


def save_results(name: str, correct_answers: int, level: int) -> None:
    result_data = f'{name}: {correct_answers}/{QUESTIONS_AMOUNT} in level {level} ({LEVEL_HELP[level]}).\n'
    try:
        with open('results.txt', 'a') as file:
            file.write(result_data)
        print('The results are saved in "results.txt".')
    except IOError:
        print('Error saving results. Please try again.')


def main() -> None:
    level = get_level()
    correct_answers = sum(ask_question(level) for _ in range(QUESTIONS_AMOUNT))

    print(f'Your mark is {correct_answers}/{QUESTIONS_AMOUNT}. '
          f'Would you like to save the result? Enter yes or no.')
    save = input().strip()

    if save.lower() in SAVE_CHOICES:
        print('What is your name?')
        name = input().strip()
        save_results(name, correct_answers, level)


if __name__ == '__main__':
    main()
