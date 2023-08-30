from domino import Domino


class Player:
    def __init__(self, id, name) -> None:
        self.id: int = id
        self.name: str = name
        self.dominos: list[Domino] = []

    def __str__(self) -> str:
        return "\n".join(f'{c}:{domino}' for c, domino in enumerate(self.dominos, start=1))

    def add_domino(self, domino: Domino) -> None:
        """ Add a domino to a player's stack. """

        self.dominos.append(domino)

    def pop_domino(self, index: int) -> Domino:
        """ Remove a domino from a player's stack by an index from 0 to len(D). """

        return self.dominos.pop(index)

    def largest_double(self) -> Domino | None:
        """ Return the largest player's double-domino or None """

        return max((d for d in self.dominos if d.is_double()),
                   default=None,
                   key=lambda d: d.a)

    def find_domino(self, domino: Domino) -> int:
        """ Return the index of the domino otherwise raises an exception. """

        try:
            return self.dominos.index(domino)
        except ValueError:
            raise ValueError(f'Domino {domino} is not in the stack!')

    def size(self) -> int:
        """ Return the size of the player's stack. """

        return len(self.dominos)

    def is_computer(self) -> bool:
        """ Check if the current player is a computer. """

        return not self.id
