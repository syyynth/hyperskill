import argparse
import hashlib

import requests


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--show-hash', action='store_true')
    return parser.parse_args()


def get_password_hash(password):
    return hashlib.sha1(password.encode()).hexdigest()


def check_password(args, password):
    sha1 = get_password_hash(password)

    if args.show_hash:
        print('Your hashed password is: ', sha1)

    url = f'https://api.pwnedpasswords.com/range/{sha1[:5]}'

    res = requests.get(url, headers={'Add-Padding': 'true'})
    print('Checking...')
    print(f'A request was sent to "{url}" endpoint, awaiting response...')

    for p in res.text.split():
        suffix, count = p.split(':')
        if sha1[5:].lower() == suffix.lower():
            print(f'Your password has been pwned! The password "{password}" appears {count} times in data breaches.')
            return
    print("Good news! Your password hasn't been pwned.")


def main():
    args = create_parser()

    while (password := input("Enter your password (or 'exit' to quit):\n")) != 'exit':
        if len(password) < 8:
            print('Your password is too short. Please enter a password of at least 8 characters.')
            continue
        check_password(args, password)

    print('Goodbye!')


if __name__ == '__main__':
    main()
