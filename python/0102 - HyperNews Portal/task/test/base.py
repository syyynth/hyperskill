# -*- coding: utf-8 -*-
import copy
import http.cookiejar
import json
import os
import re
import urllib
from datetime import datetime

from hstest import CheckResult, DjangoTest


class HyperNewsTest(DjangoTest):

    use_database = True

    COMMON_LINK_PATTERN = '''<a[^>]+href=['"]([a-zA-Z\d/_]+)['"][^>]*>'''
    CSRF_PATTERN = b'<input[^>]+name="csrfmiddlewaretoken" ' \
                   b'value="(?P<csrf>\w+)"[^>]*>'
    GROUPS_FIRST_PATTERN = '<h4>.*?</h4>.*?<ul>.+?</ul>'
    GROUPS_SECOND_PATTERN = (
        '''<a[^>]+href=['"]([a-zA-Z\d/_]+)['"][^>]*>(.+?)</a>'''
    )
    H2_PATTERN = '<h2>(.+?)</h2>'
    H4_PATTERN = '<h4>(.+?)</h4>'
    PARAGRAPH_PATTERN = '<p>(.+?)</p>'
    TEXT_LINK_PATTERN = '''<a[^>]+href=['"][a-zA-Z\d/_]+['"][^>]*>(.+?)</a>'''
    cookie_jar = http.cookiejar.CookieJar()

    def __init__(self, *args, **kwargs):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.news_file_name = os.path.join(current_dir,
                                           os.path.join('..', 'hypernews', 'news.json'))
        if not os.path.exists(os.path.split(self.news_file_name)[0]):
            os.makedirs(os.path.split(self.news_file_name)[0])
        os.environ['NEWS_JSON_PATH'] = self.news_file_name
        super().__init__(*args, **kwargs)

    def __stripped_list(self, list):
        return [item.strip() for item in list]

    def __setup(self):
        self.news_data = [{
            'created': '2020-02-22 16:40:00',
            'text': 'A new star appeared in the sky.',
            'title': 'A star is born',
            'link': 9234732
        }, {
            'created': '2020-02-09 14:15:10',
            'text': 'Text of the news 1',
            'title': 'News 1',
            'link': 1
        }, {
            'created': '2020-02-10 14:15:10',
            'text': 'Text of the news 2',
            'title': 'News 2',
            'link': 2
        }, {
            'created': '2020-02-09 16:15:10',
            'text': 'Text of the news 3',
            'title': 'News 3',
            'link': 3
        }]
        with open(self.news_file_name, 'w') as f:
            json.dump(self.news_data, f)

        self.coming_soon_page_link = self.get_url()
        self.main_page_link = self.get_url() + 'news/'
        self.create_page_link = self.main_page_link + 'create/'

    def check_coming_soon_page(self) -> CheckResult:
        self.__setup()

        try:
            page = self.read_page(self.coming_soon_page_link)
        except urllib.error.URLError:
            return CheckResult.wrong(
                f'Cannot connect to the "Coming soon" page ({self.coming_soon_page_link}).')

        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar))
        try:
            response = opener.open(self.coming_soon_page_link)
        except urllib.error.URLError:
            return CheckResult.wrong(
                f'Cannot connect to the "Coming soon" page ({self.coming_soon_page_link}).')

        coming_soon_text = 'Coming soon'

        # response.url for the backward compatibility
        if (coming_soon_text not in page
                and response.url != self.main_page_link):
            return CheckResult.wrong(
                f'"Coming soon" page ({self.coming_soon_page_link}) should contain "Coming soon" text'
            )

        return CheckResult.correct()

    def check_coming_soon_page_redirect(self) -> CheckResult:
        self.__setup()

        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar))
        try:
            response = opener.open(self.coming_soon_page_link)
        except urllib.error.URLError:
            return CheckResult.wrong(
                f'Cannot connect to the "Coming soon" page ({self.coming_soon_page_link}).')

        if response.url != self.main_page_link:
            return CheckResult.wrong(
                f'"Coming soon" ({self.coming_soon_page_link}) page should redirects to the {self.main_page_link}'
            )

        return CheckResult.correct()

    def check_main_header(self) -> CheckResult:
        self.__setup()
        try:
            page = self.read_page(self.main_page_link)
        except urllib.error.URLError:
            return CheckResult.wrong(
                f'Cannot connect to the main page {self.main_page_link}.'
            )

        h2_headers = re.findall(self.H2_PATTERN, page, re.S)
        h2_headers = self.__stripped_list(h2_headers)
        main_header = 'Hyper news'

        if len(h2_headers) != 1:
                return CheckResult.wrong(
                    f'News page should contain one <h2> element (<h2>Hyper news</h2>). '
                    f'Now news page contain {len(h2_headers)} <h2> elements.'
                )

        if main_header not in h2_headers:
            return CheckResult.wrong(
                f'Main page {self.main_page_link} should contain <h2> element with text "Hyper news"'
            )

        return CheckResult.correct()

    def check_news_page(self) -> CheckResult:
        self.__setup()

        for testing_news in self.news_data:
            created = testing_news['created']
            text = testing_news['text']
            title = testing_news['title']
            link = testing_news['link']
            task2_example_link = 9234732

            try:
                page = self.read_page(self.main_page_link + f'{link}/')
            except urllib.error.URLError:
                return CheckResult.wrong(
                    f'Cannot connect to the news page at {self.main_page_link}"link"/ '
                    'where "link" is the data of the link field from json file'
                )

            page_headers = re.findall(self.H2_PATTERN, page, re.S)
            page_headers = self.__stripped_list(page_headers)
            page_paragraphs = re.findall(self.PARAGRAPH_PATTERN, page, re.S)
            page_paragraphs = self.__stripped_list(page_paragraphs)

            if len(page_headers) != 1:
                return CheckResult.wrong(
                    f'News page should contain one <h2> element with the data '
                    f'of the title field from json file. '
                    f'Now news page containt {len(page_headers)} <h2> elements.'
                )

            if len(page_paragraphs) != 2:
                return CheckResult.wrong(
                    f'News page should contain two <p> elements with the data '
                    f'of the text field and the created field from json file. '
                    f'Now news page containt {len(page_paragraphs)} <p> elements.'
                )

            page_title = page_headers[0]

            if title not in page_title:
                if link is task2_example_link:
                    return CheckResult.wrong(
                        'News page should contain <h2> element with the data '
                        'of the title field from json file. '
                        'For example, the result for the data of the title field '
                        f'"{title}" is "{page_title}".'
                    )

                return CheckResult.wrong(
                    'News page should contain <h2> element with the data '
                    'of the title field from json file.'
                )

            page_created = page_paragraphs[0]
            page_text = page_paragraphs[1]

            if text not in page_text:
                if link is task2_example_link:
                    return CheckResult.wrong(
                        'News page should contain <p> element with the data '
                        'of the text field from json file. '
                        'For example, the result for the data of the text field '
                        f'"{text}" is "{page_text}".'
                    )

                return CheckResult.wrong(
                    'News page should contain <p> element with the data '
                    'of the text field from json file.'
                )

            if created not in page_created:
                if link is task2_example_link:
                    return CheckResult.wrong(
                        'News page should contain <p> element with the data '
                        'of the created field from json file '
                        'in the format: "%Y-%m-%d %H:%M:%S". '
                        'For example, the result for the data of the created field '
                        f'"{created}" is "{page_created}".'
                    )

                return CheckResult.wrong(
                    'News page should contain <p> element with the data '
                    'of the created field from json file '
                    'in the format: "%Y-%m-%d %H:%M:%S".'
                )

        return CheckResult.correct()

    def check_main_page_create_link(self):
        self.__setup()
        create_link = '/news/create/'

        try:
            page = self.read_page(self.main_page_link)
        except urllib.error.URLError:
            return CheckResult.wrong(
                f'Cannot connect to the main page ({self.main_page_link}).'
            )

        links_from_page = re.findall(self.COMMON_LINK_PATTERN, page, re.S)
        links_from_page = self.__stripped_list(links_from_page)

        if create_link not in links_from_page:
            return CheckResult.wrong(
                f'Main page ({self.main_page_link}) should contain <a> element with href {create_link}'
            )

        if len(links_from_page) - 1 != len(self.news_data):
            return CheckResult.wrong(
                f'Main page ({self.main_page_link}) should contain {len(self.news_data) + 1} <a> elements. '
                f'{len(self.news_data)} elements with href to news pages from the json file data '
                f'and one element with href {create_link}. '
                f'Now main page contains {len(links_from_page)} <a> elements.'
            )

        return CheckResult.correct()

    def check_main_page(self) -> CheckResult:
        self.__setup()
        created_set = set()
        news_data = copy.deepcopy(self.news_data)
        for news in news_data:
            created_dt = datetime.strptime(news['created'],
                                           '%Y-%m-%d %H:%M:%S') \
                                 .date()
            created_set.add(created_dt)

        created_list = [x for x in created_set]
        created_list.sort(reverse=True)
        created_list_str = [x.strftime('%Y-%m-%d') for x in created_list]

        try:
            page = self.read_page(self.main_page_link)
        except urllib.error.URLError:
            return CheckResult.wrong(
                f'Cannot connect to the main page {self.main_page_link}.'
            )

        h4_headers = re.findall(self.H4_PATTERN, page, re.S)
        h4_headers = self.__stripped_list(h4_headers)
        filtered_h4 = list(filter(lambda x: x in created_list_str, h4_headers))
        page_links = re.findall(self.COMMON_LINK_PATTERN, page, re.S)

        if filtered_h4 != created_list_str:
            return CheckResult.wrong(
                f'Main page ({self.main_page_link}) should contain <h4> elements grouped by '
                'date created and first should be fresh news.'
            )

        for news in news_data:
            created_date = datetime.strptime(news['created'],
                                             '%Y-%m-%d %H:%M:%S') \
                .date()
            news['created_date'] = created_date
            news['created_date_str'] = created_date.strftime('%Y-%m-%d')
            news['link'] = '/news/{}/'.format(news['link'])

        file_data = sorted(news_data, key=lambda x: x['title'])
        file_data = sorted(
            file_data, key=lambda x: x['created_date'], reverse=True)

        for news in file_data:
            news.pop('created_date')
            news.pop('created')
            news.pop('text')

        groups = re.findall(self.GROUPS_FIRST_PATTERN, page, re.S)
        news_list = [
            sorted(re.findall(self.GROUPS_SECOND_PATTERN, group, re.S),
                   key=lambda news: news[1])
            for group in groups
        ]
        response_data = []
        for news_l, h4 in zip(news_list, filtered_h4):
            for news in news_l:
                response_data.append({
                    'created_date_str': h4,
                    'link': news[0],
                    'title': news[1].strip()
                })

        if len(response_data) != len(file_data):
            return CheckResult.wrong(
                f'Main page ({self.main_page_link}) should contain {len(file_data)} <a> '
                'elements with href to news pages. Remember, that you need to use ordered dictionary.'
            )
        else:
            if response_data != file_data:
                return CheckResult.wrong(
                    f'Main page should contain correct titles and creating dates'
                )

        return CheckResult.correct()

    def check_creating_news(self):
        self.__setup()
        old_news_titles = [news['title'] for news in self.news_data]

        new_news = {
            'title': 'News 4',
            'text': 'Text of the news 4',
        }

        titles = (*old_news_titles, new_news['title'])

        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar))
        try:
            create_page_response = opener.open(
                self.create_page_link)
        except urllib.error.URLError:
            return CheckResult.wrong(f'Cannot connect to the create page ({self.create_page_link}).')

        create_page = create_page_response.read()

        csrf_options = re.findall(self.CSRF_PATTERN, create_page)
        if not csrf_options:
            return CheckResult.wrong(
                'Missing csrf_token in the create page form')

        try:
            create_response = opener.open(
                self.create_page_link,
                data=urllib.parse.urlencode({
                        'title': new_news['title'],
                        'text': new_news['text'],
                        'csrfmiddlewaretoken': csrf_options[0],
                }).encode()
            )
        except urllib.error.URLError as err:
            if 'Forbidden' not in err.reason:
                return CheckResult.wrong(
                    f'Wrong response for forbidden requests: {err.reason}')

        if create_response.url != self.main_page_link:
            return CheckResult.wrong(
                'After creating news handler should redirects to the /news/ '
                'page')

        try:
            page = self.read_page(self.main_page_link)
        except urllib.error.URLError:
            return CheckResult.wrong(
                f'Cannot connect to the main page ({self.main_page_link}).'
            )

        links_from_page = re.findall(self.TEXT_LINK_PATTERN, page, re.S)
        links_from_page = self.__stripped_list(links_from_page)

        for title in titles:
            if title not in links_from_page:
                return CheckResult.wrong(
                    f'After creating news main page ({self.main_page_link}) can\'t find {title}')

        return CheckResult.correct()

    def check_create_page_main_link(self):
        self.__setup()
        main_link = '/news/'

        try:
            page = self.read_page(self.create_page_link)
        except urllib.error.URLError:
            return CheckResult.wrong(
                f'Cannot connect to the create page ({self.create_page_link}).'
            )

        links_from_page = re.findall(self.COMMON_LINK_PATTERN, page, re.S)
        links_from_page = self.__stripped_list(links_from_page)

        if main_link not in links_from_page:
            return CheckResult.wrong(
                f'Create page {self.create_page_link} should contain '
                '<a> element with href {main_link}'
            )

        return CheckResult.correct()

    def check_news_page_main_link(self):
        self.__setup()
        main_link = '/news/'

        testing_news = self.news_data[0]
        link = testing_news['link']

        try:
            page = self.read_page(self.main_page_link + f'{link}/')
        except urllib.error.URLError:
            return CheckResult.wrong(
                f'Cannot connect to the news page at {self.main_page_link}"link"/ '
                    'where "link" is the data of the link field from json file'
            )

        links_from_page = re.findall(self.COMMON_LINK_PATTERN, page, re.S)
        links_from_page = self.__stripped_list(links_from_page)

        if main_link not in links_from_page:
            return CheckResult.wrong(
                f'News page should contain <a> element with href {main_link}'
            )

        return CheckResult.correct()

    def check_main_page_search(self):
        self.__setup()
        q = '2'
        news_data = copy.deepcopy(self.news_data)

        for news in news_data:
            created_date = datetime.strptime(news['created'],
                                             '%Y-%m-%d %H:%M:%S') \
                .date()
            news['created_date_str'] = created_date.strftime('%Y-%m-%d')

        all_headers = set((x['created_date_str'] for x in news_data))
        visible_headers = set((x['created_date_str'] for x in news_data
                               if q in x['title']))
        invisible_headers = all_headers - visible_headers
        visible_titles = [x['title'] for x in news_data
                          if q in x['title']]
        invisible_titles = [x['title'] for x in news_data
                            if q not in x['title']]

        try:
            search_page_link = self.main_page_link + f'?q={q}'
            page = self.read_page(search_page_link)
        except urllib.error.URLError:
            return CheckResult.wrong(
                f'Cannot connect to the search page.'
            )

        h4_headers = re.findall(self.H4_PATTERN, page, re.S)
        h4_headers = self.__stripped_list(h4_headers)

        for header in visible_headers:
            if header not in h4_headers:
                return CheckResult.wrong(
                    'Search page should contain headers with found news'
                )

        for header in invisible_headers:
            if header in h4_headers:
                return CheckResult.wrong(
                    'Search page should not contain headers with unfound news'
                )

        titles = re.findall(self.TEXT_LINK_PATTERN, page, re.S)
        titles = self.__stripped_list(titles)

        for title in visible_titles:
            if title not in titles:
                return CheckResult.wrong(
                    'Search page should contain found news'
                )

        for title in invisible_titles:
            if title in titles:
                return CheckResult.wrong(
                    'Search page should not contain unfound news'
                )

        return CheckResult.correct()
