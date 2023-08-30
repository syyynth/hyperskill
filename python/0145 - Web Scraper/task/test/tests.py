import glob
import os
import random
import re
import shutil
import string

import requests
from bs4 import BeautifulSoup
from furl import furl
from hstest import StageTest, CheckResult, WrongAnswer, TestCase


class NatureScraper:
    def tag_leading_to_view_article(self, tag):
        return tag.has_attr("data-track-action") and tag["data-track-action"] == "view article"

    def tag_containing_atricle_type(self, tag):
        return tag.name == "span" and tag.has_attr("data-test") and tag["data-test"] == "article.type"

    def tag_containing_article_title(self, tag):
        return tag.name == "h1" and ("article" in tag["class"][0] and "title" in tag["class"][0])

    def get_article_links_of_type(self, url, article_type="News"):
        origin_url = furl(url).origin
        try:
            articles_resp = requests.get(url)
        except Exception:
            raise WrongAnswer(f"ConnectionError occurred when tests tried to reach the page \'{url}\'.\n"
                              f"Please try running tests again.")
        soup = BeautifulSoup(articles_resp.text, "html.parser")
        articles = soup.find_all(self.tag_containing_atricle_type)
        articles = list(filter(lambda x: x.text.strip() == article_type, articles))
        return [
            furl(origin_url).add(path=x.find_parent("article").find(self.tag_leading_to_view_article).get("href")).url \
            for x in articles]

    def get_article_title_and_content(self, url):
        try:
            article = requests.get(url)
        except Exception:
            raise WrongAnswer("An error occurred when tests tried to connect to the Internet page.\n"
                              "Please, try again.")
        soup = BeautifulSoup(article.text, "html.parser")
        title = soup.find(self.tag_containing_article_title)
        content = soup.find("p", {"class": "article__teaser"})
        print(title, content)
        if title and content:
            return title.text.strip(), content.text.strip()
        else:
            raise WrongAnswer("An error occurred when tests tried to get title and content of Internet page. Retry "
                              "submitting your solution")


class WebScraperTest(StageTest):
    def generate(self):
        for name in os.listdir():
            if os.path.isdir(name) and name.startswith("Page_"):
                try:
                    shutil.rmtree(name)
                except PermissionError as e:
                    print(f"The following error occurred when the tests tried to remove directory {name}:\n"
                          f"{e}\n"
                          f"If you can, please, make it possible to remove the directory.")

        return [
            TestCase(stdin="1\nNews", attach=(1, "News"), time_limit=0),
            TestCase(stdin="2\nNews Feature", attach=(2, "News Feature"), time_limit=0)]

    def check(self, reply, attach=None):
        n_pages, article_type = attach
        scraper = NatureScraper()
        for i in range(1, n_pages + 1):
            dirname = f"Page_{i}"
            dirname = os.path.abspath(dirname)
            if not os.path.exists(dirname):
                return CheckResult.wrong(f"Impossible to find directory {dirname}")
            try:
                os.chdir(dirname)
            except NotADirectoryError:
                return CheckResult.wrong("The directory name is incorrect.")
            txt_files = glob.glob("*.txt")
            url = furl("https://www.nature.com/nature/articles?sort=PubDate&year=2020").add({"page": str(i)})
            article_links = scraper.get_article_links_of_type(url, article_type=article_type)
            if len(txt_files) != len(article_links):
                return CheckResult.wrong("A wrong number of files with articles was found in the directory {0}. \n"
                                         "{1} files were found, {2} files were expected.".format(dirname,
                                                                                                 len(txt_files),
                                                                                                 len(article_links)))
            if article_links:
                random_val = random.randint(0, len(article_links) - 1)
                title, content = scraper.get_article_title_and_content(article_links[random_val])
                content = content.strip()
                title = f"{title.translate(str.maketrans('', '', string.punctuation)).replace(' ', '_')}.txt"
                title = os.path.abspath(title)
                if not os.path.exists(title):
                    return CheckResult.wrong("A file with the title {0} was expected, but was not found.".format(title))
                try:
                    with open(title, "rb") as f:
                        try:
                            file_content = f.read().decode('utf-8').strip()
                        except UnicodeDecodeError:
                            return CheckResult.wrong("An error occurred when tests tried to read the file \"{0}\"\n"
                                                     "Please, make sure you save your file in binary format \n"
                                                     "and encode the saved data using utf-8 encoding.".format(title))
                except (IsADirectoryError, PermissionError):
                    return CheckResult.wrong("An error occurred when tests tried to read the file \"{0}\"\n"
                                             "Make sure you didn't create a folder "
                                             "with the same name as the file.".format(title))

                file_content = re.sub('[\r\n]', '', file_content)
                content = re.sub('[\r\n]', '', content)
                if file_content.replace(" ", '') != content.replace(" ", ''):
                    return CheckResult.wrong("Some of the files do not contain the expected article's body. \n"
                                             "The tests expected the following article:\n"
                                             f"\"{content}\"\n"
                                             f"However, the following text was found in the file {title}:\n"
                                             f"\"{file_content}\"")
            os.chdir("..")
            try:
                shutil.rmtree(dirname)
            except OSError as e:
                print(f"The following error occurred when the tests tried to remove directory {dirname}:\n"
                      f"{e}\n"
                      f"If you can, please, make it possible to remove the directory.")
        return CheckResult.correct()


if __name__ == '__main__':
    WebScraperTest().run_tests()
