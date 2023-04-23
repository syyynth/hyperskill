from predictor import Randomness


class Game:
    def __init__(self,
                 balance: int = 1000,
                 end_word: str = 'enough',
                 win_value: int = 1,
                 lose_value: int = 1,
                 end_msg: str = 'Game over!') -> None:
        self.balance = balance
        self.end_word = end_word
        self.win_value = win_value
        self.lose_value = lose_value
        self.end_msg = end_msg

    def play(self, model: Randomness) -> None:
        data: str | None = model.load('data')

        if not data:
            print(self.end_msg)
            return

        print('Final data string:')
        print(data)

        model.evaluate()

        print(
            f'You have ${self.balance}. '
            f'Every time the system successfully predicts your next press, you lose ${self.lose_value}.\n'
            f"""Otherwise, you earn ${self.win_value}. Print "{self.end_word}" to leave the game. Let's go!"""
        )

        while True:
            model.load('test', self.end_word)
            pred: dict[str, list[str]] | None = model.get_prediction()

            if not pred:
                print(self.end_msg)
                break

            prediction_data: list[str] = pred['data']
            original_data: list[str] = pred['original']

            print('predictions:\n', ''.join(prediction_data), sep='')

            corr: int = sum(a == b for a, b in zip(prediction_data, original_data))
            total: int = len(prediction_data)
            self.balance -= 2 * corr - total

            print(f'Computer guessed {corr} out of {total} symbols right ({corr / total * 100:.2f} %)')
            print(f'Your balance is now ${self.balance}')


if __name__ == '__main__':
    Game().play(Randomness())
