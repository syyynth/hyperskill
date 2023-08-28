import random
from itertools import combinations_with_replacement

from domino import Domino
from player import Player
from stock import Stock


class Field:
    def __init__(self) -> None:
        self.players: list[Player] = []
        self.snake: Stock = Stock()
        self.status: int | None = None
        self.stock: Stock | None = None

    def generate(self, n_players: int, n_dominos: int, player_names: list[tuple[int, str]]) -> None:
        """ Generate play field by some params. """

        total: int = 28

        assert 0 < n_players * n_dominos <= total, 'Unfair game! Please try again'
        assert len(player_names) == n_players, 'Unfair game! Please try again'

        while True:
            dominos = [Domino(a, b) for a, b in combinations_with_replacement(range(7), 2)]
            random.shuffle(dominos)

            self.stock = Stock()
            for _ in range(total - n_players * n_dominos):
                self.stock.add_domino(dominos.pop())

            players = [Player(id, name) for id, name in player_names]

            for player in players:
                for _ in range(n_dominos):
                    player.add_domino(dominos.pop())

            player = max((p for p in players if p.largest_double()),
                         default=None,
                         key=lambda p: p.largest_double().a)

            if player:
                self.players = players
                self.status = player.id
                self.snake.add_domino(player.pop_domino(player.find_domino(player.largest_double())))
                self.status = (self.status + 1) % len(self.players)
                break

    def __str__(self) -> str:
        s = self.snake.dominos
        return ''.join(map(str, s[:3] + ['...'] + s[-3:])) if len(s) >= 7 else ''.join(map(str, s))
