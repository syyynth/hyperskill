import numpy as np

data = np.array([
    [500, 503, 498],
    [501, 490, 499],
    [495, 493, 493],
    [448, 440, 439],
    [435, 434, 432],
    [430, 426, 428],
    [402, 416, 426],
    [391, 413, 412],
    [384, 404, 413],
    [379, 404, 402]
])

means = np.mean(data, axis=0)
centered_data = data - means

print(centered_data)