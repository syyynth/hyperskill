# -*- coding: utf-8 -*-
from hstest import dynamic_test

from .base import HyperNewsTest


class HyperNewsTestRunner(HyperNewsTest):

    funcs = [
        # 1 task
        HyperNewsTest.check_coming_soon_page,
        # 2 task
        HyperNewsTest.check_news_page,
        HyperNewsTest.check_news_page_main_link,
        # 3 task
        HyperNewsTest.check_main_header,
        HyperNewsTest.check_main_page,
        HyperNewsTest.check_main_page_create_link,
        # 4 task
        HyperNewsTest.check_creating_news,
        HyperNewsTest.check_create_page_main_link,
        # 5 task
        HyperNewsTest.check_main_page_search,
        HyperNewsTest.check_coming_soon_page_redirect,
    ]

    @dynamic_test(data=funcs)
    def test(self, func):
        return func(self)


if __name__ == '__main__':
    HyperNewsTestRunner().run_tests()
