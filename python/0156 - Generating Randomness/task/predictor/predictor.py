class Randomness:
    TRAINING_SIZE: int = 100
    PREDICTION_SIZE: int = 4
    DATA_VALUES: str = '01'
    PROMPT_TRAINING: str = 'Print a random string containing 0 or 1:\n'
    PROMPT_PREDICTION: str = 'Print a random string containing 0 or 1:\n'
    PROMPT_WELCOME: str = 'Please provide AI some data to learn...'

    def __init__(self) -> None:
        print(self.PROMPT_WELCOME)
        self.stop_word: str = ''
        self.training_data: str | None = None
        self.prediction_data: str | None = None
        self.triads_count: dict[str, list[int, int]] = {f'{t:03b}': [0, 0] for t in range(8)}
        self.is_evaluated: bool = False

    def __repr__(self) -> None:
        for triad, [zeros, ones] in self.triads_count.items():
            print(f'{triad}: {zeros}, {ones}')

    def reset(self) -> None:
        self.training_data = None
        self.prediction_data = None
        self.triads_count = {f'{t:03b}': [0, 0] for t in range(8)}
        self.is_evaluated = False

    def evaluate(self) -> None:
        if not self.is_evaluated and self.training_data:
            for char in range(3, len(self.training_data)):
                triad = self.training_data[char - 3: char]
                val = int(self.training_data[char])
                self.triads_count[triad][val] += 1
            self.is_evaluated = True

    def get_triads(self) -> dict[str, list[int, int]]:
        return self.triads_count

    def get_prediction(self) -> dict[str, list[str]] | None:
        if not self.prediction_data or not self.training_data:
            return
        original: list[str] = []
        prediction: list[str] = []

        for char in range(3, len(self.prediction_data)):
            triad = self.prediction_data[char - 3: char]
            zeros, ones = self.triads_count[triad]
            predicted_value = self.DATA_VALUES[zeros < ones]
            prediction.append(predicted_value)
            original.append(self.prediction_data[char])

        return {'data': prediction, 'original': original}

    def read(self, size: int, prompt: str, is_training: bool = False) -> str | None:
        data: list[str] = []

        while len(data) < size:
            if is_training:
                print(f'The current data length is {len(data)}, {size - len(data)} symbols left')

            inp = input(prompt)
            if inp == self.stop_word:
                return

            clean_data = list(filter(self.DATA_VALUES.__contains__, inp))

            if not is_training and len(clean_data) < size:
                continue
            data.extend(clean_data)

        return ''.join(data)

    def load(self, c: str, end_word: str = '') -> str | None:
        c = c.lower()
        values: list[str] = ['data', 'test']

        if c not in values:
            raise ValueError(f'Please provide a correct value [{"|".join(values)}]')

        if c == 'data':
            self.reset()
            self.training_data = self.read(self.TRAINING_SIZE, self.PROMPT_TRAINING, True)
            return self.training_data
        if c == 'test':
            self.stop_word = end_word
            self.prediction_data = self.read(self.PREDICTION_SIZE, self.PROMPT_PREDICTION)
            return self.prediction_data
