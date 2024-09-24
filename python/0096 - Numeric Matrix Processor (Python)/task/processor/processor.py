import numpy as np

menu = """1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit
"""

transpose_menu = """1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line
"""


def display(A):
    for row in A:
        print(*row)


def read():
    return np.r_[[[*map(float, input().split())]
                  for _ in range(int(input().split()[0]))]]


def add(A, B):
    if A.shape == B.shape:
        display(A + B)
    else:
        print('ERROR')


def by_scalar(A, scalar):
    display(scalar * A)


def multiply(A, B):
    if A.shape[1] == B.shape[0]:
        display(A @ B)
    else:
        print('ERROR')


def transpose():
    print(transpose_menu)
    choice = input()
    A = read()
    match choice:
        case '1':
            display(A.T)
        case '2':
            display(np.flip(A.T))
        case '3':
            display(np.fliplr(A))
        case '4':
            display(np.flipud(A))


def det(A):
    print(np.linalg.det(A))


def inv(A):
    display(np.linalg.inv(A))


def main():
    while (req := input(menu)) != '0':
        match req:
            case '1':
                add(read(), read())
            case '2':
                by_scalar(read(), float(input()))
            case '3':
                multiply(read(), read())
            case '4':
                transpose()
            case '5':
                det(read())
            case '6':
                inv(read())


if __name__ == '__main__':
    main()
