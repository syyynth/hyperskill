import enum


class Feedback(enum.Enum):
    """Prefix:
        I_ -> Information,
        E_ -> Error,
        B_ -> Bullying
    """
    I_WELCOME = 'Enter an equation'
    I_MEMO = 'Do you want to store the result? (y / n):'
    I_CONTINUE = 'Do you want to continue calculations? (y / n):'

    E_OPERAND = "Do you even know what numbers are? Stay focused!"
    E_OPERATOR = "Yes ... an interesting math operation. You've slept through all classes, haven't you?"
    E_DIVISION_BY_ZERO = "Yeah... division by zero. Smart move..."

    B_LAZY0 = 'You are'
    B_LAZY1 = ' ... lazy'
    B_LAZY2 = ' ... very lazy'
    B_LAZY3 = ' ... very, very lazy'

    B_MEMO1 = 'Are you sure? It is only one digit! (y / n)'
    B_MEMO2 = "Don't be silly! It's just one number! Add to the memory? (y / n)"
    B_MEMO3 = 'Last chance! Do you really want to embarrass yourself? (y / n)'
