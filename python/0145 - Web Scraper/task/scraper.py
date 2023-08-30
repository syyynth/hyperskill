import string
from pathlib import Path

import requests
from bs4 import BeautifulSoup

base_url = 'https://www.nature.com'
article_page_url = base_url + '/nature/articles?sort=PubDate&year=2020&page={page}'

num_pages = int(input())
article_type = input()

for page in range(1, num_pages + 1):
    page_dir = Path.cwd() / f'Page_{page}'
    page_dir.mkdir(exist_ok=True)

    article_page = requests.get(article_page_url.format(page=page)).content

    soup = BeautifulSoup(article_page, 'html.parser')

    articles = soup.find_all('article')

    for article in articles:
        if article.find(class_='c-meta__type').text == article_type:
            link = article.find('a')
            name = link.text.translate(str.maketrans(' ', '_', string.punctuation))

            file_path = page_dir / f'{name}.txt'
            with open(file_path, 'wb') as f:
                article_content = requests.get(base_url + link['href']).content
                article_soup = BeautifulSoup(article_content, 'html.parser')
                teaser = article_soup.find(class_='article__teaser')
                if teaser:
                    f.write(teaser.text.encode())
