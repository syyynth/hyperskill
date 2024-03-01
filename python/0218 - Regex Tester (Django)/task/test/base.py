import http.cookiejar
import re
import sqlite3
import urllib
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup
import requests

from hstest import CheckResult, DjangoTest

INITIAL_RECORDS = [
    ('[a-zA-Z]+_66!', 'Thrawn_66!', True),
    ('^.*$', '34534o', False),
    ('HELLO WORLD', 'HELLO WORLD', True),
    ('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', 'some text', False),
    ('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', 'example@gmail.com', True),
]


class RegexToolTest(DjangoTest):
    use_database = True
    cookie_jar = http.cookiejar.CookieJar()
    CSRF_PATTERN = r'<input[^>]+name="csrfmiddlewaretoken" ' \
                   r'value="(?P<csrf>\w+)"[^>]*>'
    input_pattern = '''<input[^>]+name=['"][a-zA-Z\d/_]+['"][^>]*>'''
    link_pattern = '''<a[^>]+href=['"][a-zA-Z\d/_]+['"][^>]*>(.+?)</a>'''

    testing_regex = [('[0-9]?[0-9]:[0-9][0-9]', '17:50', True),
                     ('\d{5}-\d{4}|\d{5}', 'zipcode', False)]

    def check_create_record(self) -> CheckResult:
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.executemany(
                "INSERT INTO record_record "
                " ('regex', 'text', 'result')"
                " VALUES (?, ?, ?)",
                INITIAL_RECORDS
            )
            connection.commit()
            cursor.execute("SELECT regex, text, result FROM record_record")
            result = cursor.fetchall()
            for item in INITIAL_RECORDS:
                if item not in result:
                    return CheckResult.wrong(('Check your Record model: '
                                              '"regex" and "text" should be of the string type, '
                                              '"result" should be of the "bool" type'))
            return CheckResult.correct()
        except sqlite3.DatabaseError as error:
            return CheckResult.wrong(str(error))

    def check_home_page_greeting(self) -> CheckResult:
        try:
            main_page = self.read_page(self.get_url())
            soup = BeautifulSoup(main_page, 'html.parser')
            try:
                h2_content = soup.find('h2').text.lower()
            except AttributeError:
                return CheckResult.wrong('Check your URLs or h2 tag in your template')
            if 'welcome to regex testing tool' not in h2_content:
                return CheckResult.wrong(
                    'Main page should contain "Welcome to regex testing tool!" line'
                )
            try:
                inputs = soup.find_all('input')
                if len(inputs) != 4:
                    button = soup.find('button')
                    if button is not None:
                        inputs.append(button)
                if inputs[1].attrs['name'] != 'regex':
                    return CheckResult.wrong('The first field should have name "regex"')
                if inputs[2].attrs['name'] != 'text':
                    return CheckResult.wrong('The second field should have name "text"')
                if inputs[3].attrs['type'] != 'submit':
                    return CheckResult.wrong(('Make sure there is a button wih the type '
                                              '"submit" on your page'))
            except IndexError:
                return CheckResult.wrong('The form lacks some of the fields')
            try:
                a_href = soup.find('a').attrs['href']
            except AttributeError:
                return CheckResult.wrong('The link to the history page is missing')
            href = '/history/'
            if a_href != href:
                return CheckResult.wrong(f'The "href" attribute is to be equal to {href}')
            return CheckResult.correct()
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the menu page.'
            )

    def check_the_csrf_token(self) -> CheckResult:
        main_page = self.read_page(self.get_url())
        csrf_options = re.findall(self.CSRF_PATTERN, main_page)
        if not csrf_options:
            return CheckResult.wrong(
                'Missing csrf_token in the main page form')
        return CheckResult.correct()

    def check_home_page_layout(self) -> CheckResult:
        number_of_input_tags = 3
        main_page = self.read_page(self.get_url())

        input_tags = re.findall(self.input_pattern, main_page)

        if len(input_tags) < number_of_input_tags:
            return CheckResult.wrong("Missing input tags or name attribute")

        link_tag = re.findall(self.link_pattern, main_page)
        if not link_tag:
            return CheckResult.wrong("Main page should contain link to history page")

        return CheckResult.correct()

    def check_create_regex_test(self) -> CheckResult:

        URL = self.get_url()
        client = requests.session()
        client.get(URL)
        try:
            csrftoken = client.cookies['csrftoken']
            for regex in self.testing_regex:
                regex_data = dict(regex=regex[0], text=regex[1], csrfmiddlewaretoken=csrftoken)
                response = client.post(URL, data=regex_data, headers=dict(Referer=URL))
                if not response.ok:
                    return CheckResult.wrong("Bad response.")
                if str(regex[2]) not in response.text:
                    return CheckResult.wrong((f"Match result is wrong. "
                                              f"For regex {regex[0]} and text {regex[1]} "
                                              f"should be {regex[2]}"))
        except urllib.error.URLError as err:
            return CheckResult.wrong(f'Cannot create test: {err.reason}. Check the form method.')
        return CheckResult.correct()

    def check_write_to_database(self) -> CheckResult:
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT regex, text, result FROM record_record")
            result = cursor.fetchall()

            for item in self.testing_regex:
                if item not in result:
                    return CheckResult.wrong('New tests are not in database')
            return CheckResult.correct()
        except sqlite3.DatabaseError as error:
            return CheckResult.wrong(str(error))

    def check_redirect_result_page(self) -> CheckResult:
        URL = self.get_url()
        client = requests.session()
        client.get(URL)
        csrftoken = client.cookies['csrftoken']
        regex_data = dict(regex='\d?\d/\d?\d/\d\d\d\d', text='12/25/2009', csrfmiddlewaretoken=csrftoken)
        response = client.post(URL, data=regex_data, headers=dict(Referer=URL))
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM record_record ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()[0]
        expected_url = self.get_url(f"result/{result}/")
        if expected_url != response.url:
            return CheckResult.wrong(("Request was not redirected correctly, "
                                      "it should have been redirected to the result page"))
        return CheckResult.correct()

    def check_result_page(self) -> CheckResult:
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM record_record")
        records = cursor.fetchall()
        for record in records:
            text = f"Text: {record[2]}"
            regex = f"Regex: {record[1]}"
            result = f"{bool(record[3])}"
            result_page = self.read_page(self.get_url(f"result/{record[0]}/"))
            if regex not in result_page:
                return CheckResult.wrong("Regex should be in the page")
            if text not in result_page:
                return CheckResult.wrong("Testing string should appear in the page")
            if result not in result_page:
                return CheckResult.wrong("Result of testing also must be in the page")
        return CheckResult.correct()

    def check_result_links(self) -> CheckResult:
        history_page_url = self.get_url('history/')
        history_page = self.read_page(history_page_url)
        soup = BeautifulSoup(history_page, features="html.parser")
        names = ['[a-zA-Z]+_66!', '^.*$', 'HELLO WORLD',
                 '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)',
                 '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)',
                 '[0-9]?[0-9]:[0-9][0-9]', '\\d{5}-\\d{4}|\\d{5}',
                 '\\d?\\d/\\d?\\d/\\d\\d\\d\\d']
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM record_record ORDER BY id DESC ")

        result = cursor.fetchall()
        all_a = soup.findAll('a')
        if len(all_a) != len(result):
            return CheckResult.wrong("Wrong number of links on history page")
        for link, record_id in zip(all_a, result):

            try:
                if str(record_id[0]) not in link.get('href'):
                    return CheckResult.wrong("Links are in the wrong order")
                self.read_page(self.get_url(link.get('href')))
            except urllib.error.URLError:
                return CheckResult.wrong(
                    f"Cannot connect to the {link.get('href')} page."
                )
            if link.text not in names:
                return CheckResult.wrong(f'The link {link.attrs["href"]} has a wrong name')
        return CheckResult.correct()
