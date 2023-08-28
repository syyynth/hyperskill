from collections import Counter

from domino import Domino
from field import Field
from player import Player


class Engine:
    """ A class representing the game engine for a game of dominos. """

    def __init__(self, field: Field) -> None:
        """ Initialize a new game engine with the given playing field. """

        self.field = field
        self.finished: bool = False

    def play(self) -> None:
        """ Play the game until it is finished. """

        while not self.finished:
            self.report()
            self.make_move()
            self.switch_player()
            self.finished = self.check_game_over()

        self.report()

    def make_move(self) -> None:
        """ Make a move for the current player. """

        current_player = self.field.players[self.field.status]
        if current_player.is_computer():
            input()
            move = self.ai_move(current_player.dominos, self.field.snake.dominos)
            self.transfer(move, current_player)
        else:
            while True:
                move = self.get_move(current_player.size())
                if self.transfer(move, current_player):
                    break
                print('Illegal move. Please try again.')

    def transfer(self, m: int, player: Player) -> bool:
        """ Transfer a domino from the current player to the snake or from the stock to the current player.
            Return True of False as transfer
        """
        # I don't want to refactor it
        snake = self.field.snake
        if m > 0:  # add to the right end of the snake
            domino = player.dominos[m - 1]
            if domino.a == snake.dominos[-1].b:
                d = player.pop_domino(m - 1)
                snake.add_domino(d)
                return True
            if domino.b == snake.dominos[-1].b:
                d = player.pop_domino(m - 1)
                d.rotate()
                snake.add_domino(d)
                return True
        elif m < 0:  # add to the left end of the snake
            domino = player.dominos[abs(m) - 1]
            if domino.b == snake.dominos[0].a:
                d = player.pop_domino(abs(m) - 1)
                snake.add_domino(d, left=True)
                return True
            if domino.a == snake.dominos[0].a:
                d = player.pop_domino(abs(m) - 1)
                d.rotate()
                snake.add_domino(d, left=True)
                return True
        elif m == 0:
            if self.field.stock.size():  # draw from the stock
                player.add_domino(self.field.stock.pop_domino())
            return True
        return False

    def switch_player(self) -> None:
        """ Switch to the next player. """

        self.field.status = (self.field.status + 1) % len(self.field.players)

    def check_game_over(self) -> bool:
        """ Check if the game is over. """

        for player in self.field.players:
            if player.size() == 0:
                return True

        snake = self.field.snake

        if snake.size():
            left = snake.dominos[0].a
            right = snake.dominos[-1].b
            if left == right:
                return sum((piece.a == left) + (piece.b == left) for piece in snake.dominos) >= 8

        # no possible moves
        if not self.field.stock.size():
            left = snake.dominos[0].a
            right = snake.dominos[-1].b
            return sum((domino.a == left) or (domino.a == right) or (domino.b == left) or (domino.b == right)
                       for player in self.field.players
                       for domino in player.dominos) == 0

        return False

    def report(self) -> None:
        """ Report the current state of the game. """

        computer = self.field.players[0]
        player = self.field.players[1]
        stock_size = self.field.stock.size()
        computer_size = computer.size()
        player_size = player.size()
        game_status = self.field.status

        print(f'{"=" * 70}\n'
              f'Stock size: {stock_size}\n'
              f'Computer pieces: {computer_size}\n'
              f'{self.field}\n'
              f'Your pieces:\n'
              f'{player}')

        status = 'Status: '
        if self.finished:
            result = ("It's a draw!" if computer_size and player_size else
                      'The computer won!' if computer_size == 0 else
                      'You won!')
            status += f'The game is over. {result}'
        else:
            status += ('Computer is about to make a move. Press Enter to continue...' if game_status == 0 else
                       "It's your turn to make a move. Enter your command." if game_status == 1 else
                       'Invalid game status.')
        print(status)

    @staticmethod
    def ai_move(hand: list[Domino], snake: list[Domino]) -> int:
        counter = Counter(d.a for d in hand + snake) + Counter(d.b for d in hand + snake)
        scores = sorted([(counter[d.a] + counter[d.b], i) for i, d in enumerate(hand)],
                        reverse=True)

        left, right = snake[0].a, snake[-1].b
        for _, i in scores:
            domino_left, domino_right = hand[i].a, hand[i].b
            if left in (domino_left, domino_right):
                return -(i + 1)
            if right in (domino_left, domino_right):
                return i + 1
        return 0

    @staticmethod
    def get_move(size) -> int:
        """ Get a valid move from the human player. """

        while True:
            try:
                move = int(input())
                if not -size <= move <= size:
                    raise ValueError
            except ValueError:
                print('Invalid input. Please try again.')
                continue
            else:
                return move
