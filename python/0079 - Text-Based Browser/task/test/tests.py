from hstest.stage_test import *
import requests
from bs4 import BeautifulSoup
import os
import shutil
from colorama import Fore
import sys
import re
if sys.platform.startswith("win"):
    import _locale
    # pylint: disable=protected-access
    _locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

CheckResult.correct = lambda: CheckResult(True, '')
CheckResult.wrong = lambda feedback: CheckResult(False, feedback)


class TextBasedBrowserTest(StageTest):

    def generate(self):

        dir_for_files = os.path.join(os.curdir, 'tb_tabs')
        return [
            TestCase(
                stdin='docs.python.org\nexit',
                attach='docs.python.org',
                args=[dir_for_files]
            ),
            TestCase(
                stdin='nytimescom\nexit',
                attach=None,
                args=[dir_for_files]
            ),
            TestCase(
                stdin='back\nexit',
                attach='back',
                args=['tb_tabs']
            ),
            TestCase(
                stdin='peps.python.org/pep-0008/\ndocs.python.org\npeps\nexit',
                attach=('peps.python.org/pep-0008/', 'docs.python.org', 'peps.python.org/pep-0008/'),
                args=[dir_for_files]
            ),
            TestCase(
                stdin='peps.python.org/pep-0008/\ndocs.python.org\nback\nexit',
                attach=('peps.python.org/pep-0008/', 'docs.python.org', 'docs.python.org'),
                args=['tb_tabs']
            )
        ]

    def check_output(self, output_text, links, not_links, source):
        """
        :param output_text: the text from the user's file or from the console output
        :param links: list with links highlighted with blue
        :param not_links: list with text that was taken from other tags than <a>
        :param source: the name of the file from which the user's text is taken or "console output" line
        :return: raises WrongAnswer if a highlighted link is not found in the output_text,
        or if a non-link text is not found in the output_text,
        or if a non-link text is highlighted with blue
        """
        output_text = re.sub(r'\s', ' ', output_text)
        for i, link in enumerate(links):
            link = re.sub(r'\s', ' ', link)
            links[i] = link
            if not link:
                continue
            if link not in output_text:
                raise WrongAnswer(f"In {source} the following link is missing: \n"
                                  f"{link}")
            if Fore.BLUE + link not in output_text:
                raise WrongAnswer(f"In {source} the following link is not highlighted with blue: \n"
                                  f"{link}")

        for line in not_links:
            line = re.sub(r'\s', ' ', line)
            highlighted_version = Fore.BLUE + line
            # the following conditions is put here in case some text from non-link tags coincides with some link's text
            if highlighted_version in links:
                continue

            if line not in output_text:
                raise WrongAnswer(f"In {source} the following text is not found:\n"
                                  f"{line}\n"
                                  f"Make sure you extract all the text from the page.\n"
                                  f"Also, make sure you don't highlight any parts of this text with blue, \n"
                                  f"and don't put any escape sequences in it.")

            if highlighted_version in output_text:
                raise WrongAnswer(f"In {source} the following text is highlighted with blue:\n"
                                  f"{highlighted_version}\n"
                                  f"Make sure you highlight only the links.")

    @staticmethod
    def get_links_and_text(url):

        url = f'https://{url}'
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/70.0.3538.77 Safari/537.36"
        try:
            page = requests.get(url, headers={'User-Agent': user_agent})
        except requests.exceptions.ConnectionError:
            raise WrongAnswer(f"An error occurred while tests tried to connect to the page {url}.\n"
                              f"Please try again a bit later.")
        soup = BeautifulSoup(page.content, 'html.parser')
        links = []
        links_tags = soup.find_all("a")
        for tag in links_tags:
            link_text = str(tag.text.strip())
            if link_text:
                links.append(link_text)
        not_links = []
        for tag in soup.find_all(["h1", "p"]):
            tag_text = str(tag.text.strip())
            if tag not in links_tags and tag_text and "<a" not in str(tag) and tag_text not in links:
                not_links.append(tag_text)

        return links, not_links

    def check_correct_url(self, attach_0, reply):
        links, not_links = TextBasedBrowserTest.get_links_and_text(attach_0)
        self.check_output(reply, links, not_links, "the console output")

    def check(self, reply, attach):

        # Incorrect URL
        if attach is None:
            if 'invalid url' in reply.lower():
                return CheckResult.correct()
            else:
                return CheckResult.wrong('An invalid URL was input to your program.\n'
                                         'Your program should print \'Invalid URL\'.')

        if attach == 'back':
            if not reply:
                return CheckResult.correct()
            else:
                return CheckResult.wrong(f'There should be no output. But your program printed: {reply}')

        # Correct URL
        path_for_tabs = os.path.join(os.curdir, 'tb_tabs')

        if not os.path.isdir(path_for_tabs):
            return CheckResult.wrong("There is no directory for tabs")

        if isinstance(attach, tuple):
            for element in attach:
                attach_0 = element
                self.check_correct_url(attach_0, reply)

        elif isinstance(attach, str):
            attach_0 = attach
            self.check_correct_url(attach_0, reply)

        try:
            shutil.rmtree(path_for_tabs)
        except PermissionError:
            return CheckResult.wrong("Impossible to remove the directory for tabs. Perhaps you haven't closed some file?")

        return CheckResult.correct()


if __name__ == '__main__':
    TextBasedBrowserTest().run_tests()
