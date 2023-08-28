import numpy


class Cell:
    X_PLAYER = 'X'
    O_PLAYER = 'O'
    EMPTY = ' '


class Board:
    winning_lines: list[list[int]] = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                                      [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    def __init__(self) -> None:
        self.board = numpy.r_[list(' ' * 9)]
        self.players = 'XO'
        self.player = 0

    def print_field(self) -> None:
        field = '---------\n' + (3 * '| %s %s %s |\n') + '---------'
        print(field % tuple(self.board))

    def get_coord(self) -> None:
        while True:
            try:
                x, y = map(lambda z: int(z) - 1, input().split())
                if 0 <= x <= 2 and 0 <= y <= 2:
                    single = x * 3 + y
                    if self.is_empty(single):
                        return single
                    print('This cell is occupied! Choose another one!')
                else:
                    print('Coordinates should be from 1 to 3!')
            except ValueError:
                print('You should enter numbers!')

    def get_state(self) -> str:
        translate = [self.board[pos] for pos in self.winning_lines]

        os = sum(all(line == Cell.O_PLAYER) for line in translate)
        xs = sum(all(line == Cell.X_PLAYER) for line in translate)

        if xs:
            return 'X wins'
        if os:
            return 'O wins'
        return 'Game not finished' if ' ' in self.board else 'Draw'

    def play(self) -> None:
        self.print_field()
        while (result := self.get_state()) == 'Game not finished':
            self.board[self.get_coord()] = self.players[self.player]
            self.player ^= 1
            self.print_field()
        print(result)

    def is_empty(self, s) -> bool:
        return self.board[s] == Cell.EMPTY


if __name__ == '__main__':
    board = Board()
    board.play()
