from player import Player
from role import Role


class LastPencil:
    def __init__(self,
                 participants: dict[str: Player],
                 possible_values: tuple[str, str, str]) -> None:
        self.participants = participants
        self.possible_values = possible_values
        self.pencils: int = self.__set_pencils()
        self.current_player: Player = self.__set_player()

    def __set_pencils(self) -> int:
        pencils: str = input('How many pencils would you like to use: ')

        while not pencils.isnumeric() or not (int(pencils) > 0):
            print('The number of pencils should be numeric and positive.')
            pencils = input()

        return int(pencils)

    def __set_player(self) -> Player:
        player_names: str = ', '.join(self.participants)
        current_player: str = input(f'Who will be the first ({player_names}): ')

        while current_player not in self.participants:
            print(f'Choose between {player_names}.')
            current_player = input()

        return self.participants[current_player]

    def __swap_player(self) -> None:
        self.current_player = [
            self.participants[player]
            for player in self.participants
            if self.participants[player].name != self.current_player.name
        ][0]

    def __print_state(self) -> None:
        print('|' * self.pencils)
        print(f"{self.current_player.name}'s turn: ")

    def play(self) -> None:
        while self.pencils:
            self.__print_state()
            self.current_player.move(self)
            self.__swap_player()

        print(f'{self.current_player.name} won!')


if __name__ == '__main__':
    names: tuple[str, str] = 'Elon', 'Dylan'
    roles: tuple[Role, Role] = Role.PLAYER, Role.BOT
    players: dict[str: Player] = {
        name: Player(name, role)
        for name, role in zip(names, roles)
    }

    possible_takes: tuple[str, str, str] = '1', '2', '3'

    game: LastPencil = LastPencil(players, possible_takes)
    game.play()
