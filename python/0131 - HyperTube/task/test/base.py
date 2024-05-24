# -*- coding: utf-8 -*-
import http.cookiejar
import io
import os
import re
import sqlite3
import urllib

import requests

from hstest import CheckResult, DjangoTest, WrongAnswer, dynamic_test


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADING_FILE_NAME = 'test_video.mp4'


TEST_FILE_NAME = 'test/test_video.mp4'
BACKUP_URL = 'https://stepik.org/media/attachments/lesson/415777/test_video.mp4'

if not os.path.exists(UPLOADING_FILE_NAME):
    if not os.path.exists(TEST_FILE_NAME):
        from urllib.request import urlopen
        file_bytes = urlopen(BACKUP_URL).read()

        with open(TEST_FILE_NAME, 'wb') as f:
            f.write(file_bytes)

    from shutil import copyfile
    copyfile(TEST_FILE_NAME, UPLOADING_FILE_NAME)


with open(UPLOADING_FILE_NAME, 'rb') as f:
    test_video_data = f.read()

INITIAL_TAGS = [
    (1, 'sport'),
    (2, 'snake'),
    (3, 'waves'),
]

INITIAL_VIDEOS = [
    (1, 'surf.mp4', 'surfing'),
    (2, 'tai.mp4', 'tai'),
]

INITIAL_VIDEOTAGS = [
    (1, 1, 1),
    (2, 2, 2),
    (3, 3, 1),
]


class HyperTubeTest(DjangoTest):

    use_database = True

    COMMON_LINK_PATTERN = '''<a[^>]+href=['"]([a-zA-Z\\d/_]+)['"][^>]*>'''
    CSRF_PATTERN = b'<input[^>]+name="csrfmiddlewaretoken" ' \
                   b'value="(?P<csrf>\\w+)"[^>]*>'
    GROUPS_FIRST_PATTERN = '<h4>.*?</h4>.*?<ul>.+?</ul>'
    GROUPS_SECOND_PATTERN = (
        '''<a[^>]+href=['"]([a-zA-Z\\d/_]+)['"][^>]*>(.+?)</a>'''
    )
    H2_PATTERN = '<h2>(.+?)</h2>'
    LINK_WITH_TEXT_PATTERN = '''<a[^>]+href=['"]([a-zA-Z\\d/_?=]+)['"][^>]*>(.+?)</a>'''
    PARAGRAPH_PATTERN = '<p>(.+?)</p>'
    SRC_PATTERN = '''<source[^>]+src=['"]([a-zA-Z\\d/_.]+)['"][^>]*>'''
    TEXT_LINK_PATTERN = '''<a[^>]+href=['"][a-zA-Z\\d/_]+['"][^>]*>(.+?)</a>'''
    cookie_jar = http.cookiejar.CookieJar()
    USERNAME = 'Test'
    PASSWORD = 'TestPassword123'
    TAG = 'testtag'
    TITLE = 'Test Video'

    def __init__(self, *args, **kwargs):
        os.environ['HYPERSKILL_MEDIA_ROOT'] = CURRENT_DIR
        file_and_dir_names = os.listdir(CURRENT_DIR)
        file_name_without_extension = UPLOADING_FILE_NAME.split('.')[0]
        for name in file_and_dir_names:
            if file_name_without_extension in name:
                self.__delete_file(name)

        super().__init__(*args, **kwargs)

    def __delete_file(self, name):
        file_path = os.path.join(CURRENT_DIR, name)
        if name != UPLOADING_FILE_NAME and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                raise WrongAnswer(
                    f'Cannot delete file "{file_path}"\n'
                    f'Did you close it?')

    def check_create_videos(self) -> CheckResult:
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.executemany(
                'INSERT INTO tube_tag (`id`, `name`) VALUES (?, ?)',
                INITIAL_TAGS
            )
            cursor.executemany(
                'INSERT INTO tube_video (`id`,`file`, `title`) '
                'VALUES (?, ?, ?)',
                INITIAL_VIDEOS
            )
            cursor.executemany(
                'INSERT INTO tube_videotag (`id`,`tag_id`, `video_id`) '
                'VALUES (?, ?, ?)',
                INITIAL_VIDEOTAGS
            )
            connection.commit()

            cursor.execute(
                'SELECT `id`, `name` FROM tube_tag')
            tags = cursor.fetchall()

            if tags != INITIAL_TAGS:
                return CheckResult.wrong('Check your Tag model')

            cursor.execute(
                'SELECT `id`,`file`, `title` FROM tube_video')
            videos = cursor.fetchall()

            if videos != INITIAL_VIDEOS:
                return CheckResult.wrong('Check your Video model')

            cursor.execute(
                'SELECT `id`,`tag_id`, `video_id` FROM tube_videotag')
            videotags = cursor.fetchall()

            if videotags != INITIAL_VIDEOTAGS:
                return CheckResult.wrong('Check your VideoTag model')

            return CheckResult.correct()
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

    def check_main_header(self) -> CheckResult:
        try:
            page = self.read_page(self.get_url() + 'tube/')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the main page.'
            )

        h2_headers = re.findall(self.H2_PATTERN, page, re.S)
        h2_headers = self.__stripped_list(h2_headers)
        main_header = 'Hypertube'

        is_main_header = False
        for h2_header in h2_headers:
            if main_header in h2_header:
                is_main_header = True
                break

        if not is_main_header:
            return CheckResult.wrong(
                'Main page should contain <h2> element with text "Hypertube"'
            )

        return CheckResult.correct()

    def check_main_page_login_link(self):
        login_link = '/login/'
        try:
            page = self.read_page(self.get_url() + 'tube/')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the main page.'
            )

        links_from_page = re.findall(self.COMMON_LINK_PATTERN, page, re.S)
        links_from_page = self.__stripped_list(links_from_page)

        if login_link not in links_from_page:
            return CheckResult.wrong(
                f'Main page should contain <a> element with href {login_link}'
            )

        return CheckResult.correct()

    def check_main_page_upload_link(self):
        upload_link = '/tube/upload/'
        try:
            page = self.read_page(self.get_url() + 'tube/')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the main page.'
            )

        links_from_page = re.findall(self.COMMON_LINK_PATTERN, page, re.S)
        links_from_page = self.__stripped_list(links_from_page)

        if upload_link not in links_from_page:
            return CheckResult.wrong(
                f'Main page should contain <a> element with href {upload_link}'
            )

        return CheckResult.correct()

    def check_main_page_video_links(self):
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.execute(
                'SELECT `id`, `title` FROM tube_video')
            videos = cursor.fetchall()
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

        video_links_with_titles_from_db = [(f'/tube/watch/{x[0]}/',
                                            x[1]) for x in videos]

        try:
            page = self.read_page(self.get_url() + 'tube/')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the main page.'
            )

        links_from_page = re.findall(self.LINK_WITH_TEXT_PATTERN, page, re.S)
        links_from_page = self.__stripped_list_with_tuple(links_from_page)

        for video_link in video_links_with_titles_from_db:
            if video_link not in links_from_page:
                return CheckResult.wrong(
                    'Main page should contain <a> element with href '
                    '/tube/watch/{id}/ and title as link text'
                )

        return CheckResult.correct()

    def check_main_page_video_count(self):
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.execute(
                'SELECT count(*) FROM tube_video')
            video_count = str(cursor.fetchall()[0][0])
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

        try:
            page = self.read_page(self.get_url() + 'tube/')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the main page.'
            )

        paragraphs_from_page = re.findall(self.PARAGRAPH_PATTERN, page, re.S)
        paragraphs_from_page = self.__stripped_list(paragraphs_from_page)

        quantity_in_paragraphs = False
        for paragraph in paragraphs_from_page:
            if video_count in paragraph:
                quantity_in_paragraphs = True
                break

        if not quantity_in_paragraphs:
            return CheckResult.wrong(
                f'Main page should contain <p> element with quantity of videos'
            )

        return CheckResult.correct()

    def __stripped_list(self, list):
        return [item.strip() for item in list]

    def __stripped_list_with_tuple(self, list):
        return [(item[0].strip(), item[1].strip()) for item in list]

    def check_main_page_search(self):
        q = 'ai'
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"SELECT `id`, `title` FROM tube_video WHERE title "
                f"LIKE '%{q}%'"
            )
            visible_videos = cursor.fetchall()
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

        visible_video_links_with_titles_from_db = \
            [(f'/tube/watch/{x[0]}/', x[1]) for x in visible_videos]

        try:
            cursor.execute(
                f"SELECT `id`, `title` FROM tube_video WHERE title "
                f"NOT LIKE '%{q}%'"
            )
            invisible_videos = cursor.fetchall()
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

        invisible_video_links_with_titles_from_db = \
            [(f'/tube/watch/{x[0]}/', x[1]) for x in invisible_videos]

        try:
            page = self.read_page(self.get_url() + f'tube/?q={q}')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the main page.'
            )

        links_from_page = re.findall(self.LINK_WITH_TEXT_PATTERN, page, re.S)
        links_from_page = self.__stripped_list_with_tuple(links_from_page)

        for video_link in visible_video_links_with_titles_from_db:
            if video_link not in links_from_page:
                return CheckResult.wrong(
                    'Main page should contain links with found videos '
                    'when searching'
                )

        for video_link in invisible_video_links_with_titles_from_db:
            if video_link in links_from_page:
                return CheckResult.wrong(
                    f'Main page should not contain links with unfound videos '
                    f'when searching'
                )

        return CheckResult.correct()

    def check_main_page_tag_filtering(self):
        tag = 'sport'
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"SELECT tube_video.id, tube_video.title FROM tube_video "
                f"JOIN tube_videotag ON tube_video.id = tube_videotag.video_id "
                f"JOIN tube_tag ON tube_videotag.tag_id = tube_tag.id "
                f"WHERE tube_tag.name = '{tag}'"
            )
            visible_videos = cursor.fetchall()
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

        visible_video_links_with_titles_from_db = \
            [(f'/tube/watch/{x[0]}/', x[1]) for x in visible_videos]

        try:
            cursor.execute(
                f"SELECT tv.id, tv.title FROM tube_video tv "
                f"WHERE NOT EXISTS (SELECT 1 FROM tube_video "
                f"JOIN tube_videotag ON tube_video.id = tube_videotag.video_id "
                f"JOIN tube_tag ON tube_videotag.tag_id = tube_tag.id "
                f"WHERE tube_tag.name = '{tag}' AND tv.id = tube_video.id)"
            )
            invisible_videos = cursor.fetchall()
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

        invisible_video_links_with_titles_from_db = \
            [(f'/tube/watch/{x[0]}/', x[1]) for x in invisible_videos]

        try:
            page = self.read_page(
                self.get_url() + f'tube/?tag={tag}'
            )
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the main page.'
            )

        links_from_page = re.findall(self.LINK_WITH_TEXT_PATTERN, page, re.S)
        links_from_page = self.__stripped_list_with_tuple(links_from_page)

        for video_link in visible_video_links_with_titles_from_db:
            if video_link not in links_from_page:
                return CheckResult.wrong(
                    'Main page should contain links with found videos when '
                    'filtering with tags'
                )

        for video_link in invisible_video_links_with_titles_from_db:
            if video_link in links_from_page:
                return CheckResult.wrong(
                    'Main page should not contain links with unfound videos '
                    'when filtering with tags'
                )

        return CheckResult.correct()

    def check_signup(self) -> CheckResult:
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )
        try:
            response = opener.open(self.get_url() + 'signup/')
        except urllib.error.URLError:
            return CheckResult.wrong('Cannot connect to the signup page.')

        csrf_options = re.findall(
            b'<input[^>]+value="(?P<csrf>\\w+)"[^>]*>', response.read()
        )
        if not csrf_options:
            return CheckResult.wrong('Missing csrf_token in the form')

        try:
            response = opener.open(
                self.get_url() + 'signup/',
                data=urllib.parse.urlencode({
                    'csrfmiddlewaretoken': csrf_options[0],
                    'username': self.USERNAME,
                    'password1': self.PASSWORD,
                    'password2': self.PASSWORD,
                }).encode()
            )

            if f'login' in response.url:
                return CheckResult.correct()
            return CheckResult.wrong('Cannot signup: problems with form')
        except urllib.error.URLError as err:
            return CheckResult.wrong(f'Cannot signup: {err.reason}')

    def check_login(self) -> CheckResult:
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar))
        try:
            response = opener.open(self.get_url() + 'login/')
        except urllib.error.URLError:
            return CheckResult.wrong('Cannot connect to the login page.')

        csrf_options = re.findall(
            b'<input[^>]+value="(?P<csrf>\\w+)"[^>]*>', response.read()
        )
        if not csrf_options:
            return CheckResult.wrong('Missing csrf_token in the form')

        try:
            response = opener.open(
                self.get_url() + 'login/',
                data=urllib.parse.urlencode({
                    'csrfmiddlewaretoken': csrf_options[0],
                    'username': self.USERNAME,
                    'password': self.PASSWORD,
                }).encode(),
            )
            if 'login' not in response.url:
                return CheckResult.correct()
            return CheckResult.wrong('Cannot login: problems with form')
        except urllib.error.URLError as err:
            return CheckResult.wrong(f'Cannot login: {err.reason}')

    def check_uploading_video(self):
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar))
        try:
            upload_page_response = opener.open(
                self.get_url() + 'tube/upload/')
        except urllib.error.URLError:
            return CheckResult.wrong('Cannot connect to the upload page.')

        upload_page = upload_page_response.read()

        csrf_options = re.findall(self.CSRF_PATTERN, upload_page)

        if not csrf_options:
            return CheckResult.wrong(
                'Missing csrf_token in the upload page form')

        new_video = {
            'title': self.TITLE,
            'tags': self.TAG,
            'csrfmiddlewaretoken': csrf_options[0],
        }
        files = {'video': open(UPLOADING_FILE_NAME, 'rb')}

        upload_response = requests.post(
            self.get_url() + 'tube/upload/',
            cookies=self.cookie_jar, files=files, data=new_video
        )

        if upload_response.url != self.get_url() + 'tube/':
            return CheckResult.wrong(
                'After uploading video handler should redirects to the /tube/ '
                'page')

        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"SELECT count(*) FROM tube_video WHERE title = '{self.TITLE}'"
            )
            videos = cursor.fetchall()
        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))

        if videos[0][0] != 1:
            return CheckResult.wrong(
                'After uploading video data doesn\'t saved in database')

        return CheckResult.correct()

    def check_forbid_anonymous_upload(self) -> CheckResult:
        opener = urllib.request.build_opener()
        try:
            upload_page_response = opener.open(
                self.get_url() + 'tube/upload/')
        except urllib.error.URLError:
            return CheckResult.wrong('Cannot connect to the upload page.')

        upload_page = upload_page_response.read()

        csrf_options = re.findall(self.CSRF_PATTERN, upload_page)
        if not csrf_options:
            return CheckResult.correct()

        title = 'Test Video'

        new_video = {
            'title': title,
            'tags': 'testtag',
            'csrfmiddlewaretoken': csrf_options[0],
        }
        files = {'video': open(UPLOADING_FILE_NAME, 'rb')}

        upload_response = requests.post(
            self.get_url() + 'tube/upload/', files=files,
            data=new_video
        )

        if upload_response.status_code != 403:
            return CheckResult.wrong(
                'Should not allow anonymous users upload video')

        return CheckResult.correct()

    def check_upload_page_main_link(self):
        main_link = '/tube/'

        try:
            page = self.read_page(
                self.get_url() + 'tube/upload/')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the upload page.'
            )

        links_from_page = re.findall(self.COMMON_LINK_PATTERN, page, re.S)
        links_from_page = self.__stripped_list(links_from_page)

        if main_link not in links_from_page:
            return CheckResult.wrong(
                f'Upload page should contain <a> element with href {main_link}'
            )

        return CheckResult.correct()

    def check_watch_and_video_response(self):
        video_template_link = '/tube/{file_name}/'
        login_link = '/login/'
        main_link = '/tube/'
        try:
            watch_response = self.read_page(
                self.get_url() + 'tube/watch/3/')
        except urllib.error.URLError:
            return CheckResult.wrong(
                'Cannot connect to the watch page.'
            )

        links_from_page = re.findall(self.COMMON_LINK_PATTERN, watch_response,
                                     re.S)
        links_from_page = self.__stripped_list(links_from_page)

        if login_link not in links_from_page:
            return CheckResult.wrong(
                f'Watch page should contain <a> element with href {login_link}'
            )
        if main_link not in links_from_page:
            return CheckResult.wrong(
                f'Watch page should contain <a> element with href {main_link}'
            )

        paragraphs_from_page = re.findall(self.PARAGRAPH_PATTERN,
                                          watch_response, re.S)
        paragraphs_from_page = self.__stripped_list(paragraphs_from_page)
        if self.TITLE not in paragraphs_from_page:
            return CheckResult.wrong(
                f'Watch page should contain <p> element with the video title'
            )

        links_with_text_from_page = re.findall(
            self.LINK_WITH_TEXT_PATTERN, watch_response, re.S)
        links_with_text_from_page = self.__stripped_list_with_tuple(
            links_with_text_from_page)

        video_link_with_text = (f'/tube/?tag={self.TAG}', f'#{self.TAG}')
        if video_link_with_text not in links_with_text_from_page:
            return CheckResult.wrong(
                'Watch page should contain <a> element with href to '
                '/tube/?tag={tag} filter and #{tag} as link text, where '
                'tag is your tag name'
            )

        src_from_page = re.findall(self.SRC_PATTERN, watch_response, re.S)
        src_from_page = self.__stripped_list(src_from_page)
        video_link = None

        for src in src_from_page:
            if UPLOADING_FILE_NAME.split('.')[0] in src:
                if src.endswith('/'):
                    src = src[:-1]
                video_link = src
                break

        if not video_link:
            return CheckResult.wrong(
                f'Watch page should contain <source> element with src '
                f'{video_template_link}'
            )
        file_name_to_delete = video_link.split('/')[-1]

        video_response = requests.get(
            f'{self.get_url()}{video_link[1:]}/')

        required_header = {'Accept-Ranges': 'bytes'}

        if video_response.headers.get('Accept-Ranges') != 'bytes':
            self.__delete_file(file_name_to_delete)
            return CheckResult.wrong(
                f'Video response should contain header {required_header}'
            )

        if video_response.headers.get('Content-Type') != 'video/mp4':
            self.__delete_file(file_name_to_delete)
            return CheckResult.wrong(
                f'Video response should contain Content-Type header, '
                f'e.g. Content-Type: video/mp4 for mp4 video'
            )

        response_file_bytes = io.BytesIO()
        for chunk in video_response.iter_content(chunk_size=1024):
            response_file_bytes.write(chunk)

        if response_file_bytes.getvalue() != test_video_data:
            self.__delete_file(file_name_to_delete)
            return CheckResult.wrong(
                'Video response should contain uploaded file in bytes'
            )

        self.__delete_file(file_name_to_delete)
        return CheckResult.correct()


class HyperTubeTestRunner(HyperTubeTest):

    funcs = [
        # 1 task
        HyperTubeTest.check_create_videos,
        # 2 task
        HyperTubeTest.check_main_header,
        HyperTubeTest.check_main_page_login_link,
        HyperTubeTest.check_main_page_upload_link,
        HyperTubeTest.check_main_page_video_links,
        HyperTubeTest.check_main_page_video_count,
        # 3 task
        HyperTubeTest.check_main_page_search,
        HyperTubeTest.check_main_page_tag_filtering,
        # 4 task
        HyperTubeTest.check_signup,
        HyperTubeTest.check_login,
        # 5 task
        HyperTubeTest.check_uploading_video,
        HyperTubeTest.check_forbid_anonymous_upload,
        HyperTubeTest.check_upload_page_main_link,
        # 6 task
        HyperTubeTest.check_watch_and_video_response,
    ]

    @dynamic_test(data=funcs)
    def test(self, func):
        return func(self)


if __name__ == '__main__':
    HyperTubeTestRunner().run_tests()
