import re
from typing import Match

from feedback import Feedback

OPERATORS: set[str] = set('+-*/')


def is_float(*nums: str) -> bool:
    try:
        list(map(float, nums))
        return True
    except ValueError:
        return False


def is_one_digit(v: str, digit: str = r'\d') -> Match[bytes] | None:
    return re.match(rf'^-?{digit}(?:\.|\.0+)?$', v)


def check(op1: str, operator: str, op2: str) -> None:
    msg: str = ''

    if is_one_digit(op1) and is_one_digit(op2):
        msg += Feedback.B_LAZY1.value

    if any(is_one_digit(o, '1') for o in (op1, op2)) and operator == '*':
        msg += Feedback.B_LAZY2.value

    if any(is_one_digit(o, '0') for o in (op1, op2)) and operator in '*+-':
        msg += Feedback.B_LAZY3.value

    if msg != '':
        print(Feedback.B_LAZY0.value + msg)


def is_valid_expr(op1: str, operator: str, op2: str) -> bool:
    if not is_float(op1, op2):
        print(Feedback.E_OPERAND.value)
        return False

    if operator not in OPERATORS:
        print(Feedback.E_OPERATOR.value)
        return False

    if operator == '/' and float(op2) == 0:
        print(Feedback.E_DIVISION_BY_ZERO.value)
        return False

    return True


def calculate(x: str, op: str, y: str) -> float:
    a: float = float(x)
    b: float = float(y)

    match op:
        case '+':
            return a + b
        case '/':
            return a / b
        case '-':
            return a - b
        case '*':
            return a * b


def take_input(feedback: str) -> str:
    while True:
        r: str = input(feedback)
        if r in ('y', 'n'):
            break
    return r


def memory(memo: float, res: float) -> float:
    res: str = str(res)
    response: list[str] = [
        Feedback.B_MEMO3.value,
        Feedback.B_MEMO2.value,
        Feedback.B_MEMO1.value
    ]

    st = take_input(Feedback.I_MEMO.value)

    if st == 'n':
        return memo

    if not is_one_digit(res):
        return float(res)

    while response:
        if take_input(response.pop()) == 'n':
            return memo

    return float(res)


def main() -> None:
    memo: float = 0
    cont: str = 'y'

    while cont == 'y':
        print(Feedback.I_WELCOME.value)

        tokens: list[str, str, str] = [
            str(memo) if t == 'M' else t for t in re.split(r'\s+', input())
        ]

        if f := check(*tokens):
            print(f)

        if is_valid_expr(*tokens):
            res = calculate(*tokens)
            print(res)
            memo = memory(memo, res)
            cont = take_input(Feedback.I_CONTINUE.value)


if __name__ == '__main__':
    main()
