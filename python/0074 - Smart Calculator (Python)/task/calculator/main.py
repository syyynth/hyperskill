from calculator import Calculator
from constants import MSG_BYE, MSG_EXIT


def main():
    calc = Calculator()
    while (resp := calc.evaluate(input())) != MSG_EXIT:
        if resp is not None:
            print(resp)

    print(MSG_BYE)


if __name__ == '__main__':
    main()
