keyword_len: int = int(input())

first_msg: list[str] = input().split()
second_msg: list[str] = input().split()
third_msg: list[str] = input().split()

shifts: list[int] = [ord(r) - ord(l) for r, l in zip(first_msg, second_msg)]

answer: list[str] = []
for count, letter in enumerate(third_msg):
    val = chr((ord(letter) % 97 + shifts[count % keyword_len]) % 26 + 97)
    answer.append(' ' if val == 'x' else val)

print(''.join(answer))
