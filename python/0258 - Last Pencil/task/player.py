import random

from role import Role


class Player:
    def __init__(self, name: str, role: Role) -> None:
        self.name = name
        self.role = role

    @staticmethod
    def move(state) -> None:
        if state.current_player.role == Role.PLAYER:
            while True:
                take: str = input()
                if take not in state.possible_values:
                    print(f'Possible values: {", ".join(state.possible_values)}.')
                elif int(take) > state.pencils:
                    print('Too many pencils were taken.')
                else:
                    break
            state.pencils -= int(take)
        elif state.current_player.role == Role.BOT:
            strategic_moves: int = (state.pencils - 1) % (len(state.possible_values) + 1)
            moves: int = (strategic_moves
                          if strategic_moves > 0
                          else random.randint(1, min(len(state.possible_values), state.pencils)))
            print(moves)
            state.pencils -= moves
