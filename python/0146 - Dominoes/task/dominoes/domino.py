class Domino:
    def __init__(self, a, b) -> None:
        self.a: int = a
        self.b: int = b

    def __str__(self) -> str:
        return f'[{self.a}, {self.b}]'

    def __eq__(self, other):
        return (self.a, self.b) in [(other.a, other.b), (other.b, other.a)]

    def is_double(self) -> bool:
        """ Check if this domino is a double. """

        return self.a == self.b

    @staticmethod
    def largest_double(x, y) -> int:
        """ neg ? y > x : pos ? x > y : zero """

        if x is None and y is None:
            return 0
        if x is None and y:
            return -1
        if x and y is None:
            return 1
        return x.a - y.a

    def rotate(self) -> None:
        self.a, self.b = self.b, self.a
