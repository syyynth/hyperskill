from domino import Domino


class Stock:
    def __init__(self) -> None:
        self.dominos: list[Domino] = []

    def add_domino(self, domino: Domino, *, left: bool = False) -> None:
        """ Add a `domino` to the stock. If `left` is True, add it to the left. Otherwise, add it to the right. """

        if left:
            self.dominos.insert(0, domino)
        else:
            self.dominos.append(domino)

    def pop_domino(self) -> Domino | None:
        """ Remove and return a `domino` from the right of the stock if any left. Otherwise, return None. """
        return self.dominos and self.dominos.pop()

    def size(self) -> int:
        """ Return the size of the stock. """

        return len(self.dominos)
