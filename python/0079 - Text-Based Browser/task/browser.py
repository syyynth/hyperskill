import sys
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from colorama import Fore


class Browser:
    def __init__(self, dir_name: str) -> None:
        self.cwd = self.create_directory(dir_name)
        self.history = []

    def read_file(self, file: str) -> str | None:
        path = self.cwd / file
        if path.is_file():
            with path.open() as f:
                self.history.append(file)
                return f.read()

    def write_file(self, file: str) -> str | None:
        response = self.get_response(file)
        text = self.parse_response(response)
        cache_name = self.cache_name(response.url)
        path = self.cwd / cache_name

        with path.open('w') as f:
            f.write(text)
            self.history.append(cache_name)

        return text

    def go_back(self) -> str | None:
        if self.history:
            self.history.pop()
            if self.history:
                file = self.history.pop()
                return self.read_file(file)

    @staticmethod
    def create_directory(dir_name: str) -> Path:
        cwd = Path.cwd() / dir_name
        cwd.mkdir(exist_ok=True)
        return cwd

    @staticmethod
    def get_response(file: str) -> requests.Response:
        try:
            response = requests.get(file)
        except requests.exceptions.MissingSchema:
            response = requests.get('https://' + file)
        return response

    @staticmethod
    def parse_response(response: requests.Response) -> str:
        soup = BeautifulSoup(response.content, 'html.parser')
        tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']
        text = ''.join(
            element.text if element.name != 'a' else Fore.BLUE + element.text + Fore.RESET
            for element in soup.find_all(tags)
        )
        return text

    @staticmethod
    def cache_name(url: str) -> str:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        return domain.split('.')[0]


def main() -> None:
    dir_name = sys.argv[1]
    browser = Browser(dir_name)

    while (file := input()) != 'exit':
        if file == 'back':
            if page := browser.go_back():
                print(page)
        elif '.' in file:
            page = browser.write_file(file)
            print(page or 'Invalid URL')
        else:
            page = browser.read_file(file)
            print(page or 'Invalid URL')


if __name__ == '__main__':
    main()
