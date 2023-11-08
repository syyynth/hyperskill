import itertools

CARD_WIDTH = 50
CARD_HEIGHT = 30


def create_layer(k, interval):
    tree_width = 2 * k - 3
    layer = ['*'] * tree_width
    possible_ball_start = (k - 2) * (k - 3) // 2

    for i in range(tree_width):
        if i % 2:
            if not possible_ball_start % interval:
                layer[i] = 'O'
            possible_ball_start += 1

    return ''.join(layer)


def build_tree(height, interval):
    align_size = 2 * height - 1
    tree_layers = []

    for x in range(height + 2):
        if x == 0:
            layer = f'{'X':^{align_size}}'
        elif x == 1:
            layer = f'{'^':^{align_size}}'
        elif x <= height:
            layer_content = '/' + create_layer(x, interval) + '\\'
            layer = f'{layer_content:^{align_size}}'
        else:
            layer = f'{'| |':^{align_size}}'

        tree_layers.append(layer)

    return '\n'.join(tree_layers)


def add_tree(postcard, tree, top_left_x, top_left_y):
    for y_delta, layer in enumerate(tree):
        x = top_left_x - len(layer.strip()) // 2
        y = top_left_y + y_delta
        for char in layer.strip():
            if 0 <= x < CARD_WIDTH and 0 <= y < CARD_HEIGHT:
                postcard[y][x] = char
            x += 1


def create_postcard(params):
    postcard = [[' ' for _ in range(CARD_WIDTH)]
                for _ in range(CARD_HEIGHT)]

    # X, Y are swapped
    for H, I, Y, X in itertools.batched(params, 4):
        tree = build_tree(H, I).split('\n')
        add_tree(postcard, tree, X, Y)

    postcard[CARD_HEIGHT - 3] = list(f'{'Merry Xmas':^{CARD_WIDTH}}')
    for i in range(CARD_HEIGHT):
        if i in [0, CARD_HEIGHT - 1]:
            postcard[i] = ['-'] * CARD_WIDTH
        else:
            postcard[i][0] = '|'
            postcard[i][CARD_WIDTH - 1] = '|'

    return '\n'.join(''.join(r) for r in postcard)


if __name__ == '__main__':
    data = [*map(int, input().split())]
    if len(data) == 2:
        print(build_tree(*data))
    else:
        print(create_postcard(data))
