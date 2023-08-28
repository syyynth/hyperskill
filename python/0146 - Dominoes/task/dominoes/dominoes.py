from engine import Engine
from field import Field


def main():
    field = Field()
    field.generate(n_players=2,
                   n_dominos=7,
                   player_names=[(0, 'Computer'), (1, 'Player')])

    Engine(field).play()


if __name__ == '__main__':
    main()
