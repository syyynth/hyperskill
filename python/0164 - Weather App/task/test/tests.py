import asyncio
import os

from hstest import FlaskTest, CheckResult, WrongAnswer
from hstest import dynamic_test
from hstest.dynamic.security.exit_handler import ExitHandler
from pyppeteer import launch
from pyppeteer.errors import NetworkError, TimeoutError

import nest_asyncio

nest_asyncio.apply()


async def querySelector(page, selector):
    try:
        return await page.querySelector(selector)
    except (NetworkError, TimeoutError) as ex:
        print(ex)
        raise WrongAnswer(f"Can't access an item with a selector '{selector}'")


async def querySelectorAll(page, selector):
    try:
        return await page.querySelectorAll(selector)
    except (NetworkError, TimeoutError) as ex:
        print(ex)
        raise WrongAnswer(f"Can't access an item with a selector '{selector}'")


async def newPage(browser):
    try:
        return await browser.newPage()
    except (NetworkError, TimeoutError) as ex:
        print(ex)
        raise WrongAnswer("Browser tab is closed unexpectedly or inaccessible")


async def goto(page, url):
    try:
        return await page.goto(url)
    except (NetworkError, TimeoutError) as ex:
        print(ex)
        raise WrongAnswer(f"Can't access the page with URL '{url}'")


async def close_browser(browser):
    try:
        await browser.close()
    except Exception as ex:
        print(ex)
        pass


async def waitForNavigation(page):
    try:
        return await page.waitForNavigation()
    except (NetworkError, TimeoutError) as ex:
        print(ex)


async def reload(page):
    try:
        return await page.reload()
    except (NetworkError, TimeoutError) as ex:
        print(ex)


class FlaskProjectTest(FlaskTest):
    source = 'web.app'
    run_args = {
        "headless": False,
        "defaultViewport": None,
        "args": ['--start-maximized', '--disable-infobar', '--no-sandbox'],
        "ignoreDefaultArgs": ['--enable-automation'],
    }

    async def launch_and_get_browser(self):
        try:
            return await launch(self.run_args)
        except Exception as error:
            raise WrongAnswer(str(error))

    async def get_input_field(self, page):
        input_field = await querySelector(page, 'input#input-city')
        if input_field is None:
            raise WrongAnswer("Can't find input field with 'input-city' id!")
        return input_field

    async def get_submit_button(self, page):
        button = await querySelector(page, 'button.submit-button')
        if button is None:
            raise WrongAnswer("Can't find a button with 'submit-button' class!")
        return button

    def generate(self):
        try:
            if os.path.exists('web/weather.db'):
                os.remove('web/weather.db')
        except Exception as ignored:
            raise WrongAnswer(f"Looks like your 'weather.db' database file is blocked. "
                              f"Stop your apps that connects to that database!")
        return []

    @classmethod
    async def check_cards_in_the_page(cls, page, cards_number):
        cards = await querySelectorAll(page, 'div.card')

        if len(cards) != cards_number:
            raise WrongAnswer(f"Found {len(cards)} <div> blocks with class 'card', but should be {cards_number}!")

        for card in cards:
            degrees = await querySelector(card, 'div.degrees')
            if degrees is None:
                raise WrongAnswer(
                    "One of the <div> blocks with card class 'card' doesn't contain <div> block with class 'degrees'")
            state = await querySelector(card, 'div.state')
            if state is None:
                raise WrongAnswer(
                    "One of the <div> blocks with card class 'card' doesn't contain <div> block with class 'state'")
            city = await querySelector(card, 'div.city')
            if city is None:
                raise WrongAnswer(
                    "One of the <div> blocks with card class 'card' doesn't contain <div> block with class 'city'")
            button = await querySelector(card, 'button.delete-button')
            if button is None:
                raise WrongAnswer(
                    "One of the <div> blocks with card class 'card' doesn't contain a button with class 'delete-button'")

    async def test_response_async(self):
        browser = await self.launch_and_get_browser()
        page = await newPage(browser)
        await goto(page, self.get_url())
        await close_browser(browser)

    @dynamic_test(order=1, time_limit=-1)
    def test_response(self):
        ExitHandler.revert_exit()
        asyncio.new_event_loop().run_until_complete(self.test_response_async())
        return CheckResult.correct()

    async def test_main_page_structure_async(self):
        browser = await self.launch_and_get_browser()
        page = await newPage(browser)  # browser.newPage()

        await goto(page, self.get_url())

        cards_div = await querySelector(page, 'div.cards')

        if cards_div is None:
            raise WrongAnswer("Can't find <div> block with class 'cards'")

        button = await self.get_submit_button(page)

        if button is None:
            raise WrongAnswer("Can't find a button with 'submit-button' class!")

        input_field = await self.get_input_field(page)

        if input_field is None:
            raise WrongAnswer("Can't find input field with 'input-city' id!")

        await self.check_cards_in_the_page(page, 0)

        await close_browser(browser)

        return CheckResult.correct()

    @dynamic_test(order=2)
    def test_main_page_structure(self):
        asyncio.new_event_loop().run_until_complete(self.test_main_page_structure_async())
        return CheckResult.correct()

    async def test_add_city_async(self):
        browser = await self.launch_and_get_browser()
        page = await newPage(browser)
        await goto(page, self.get_url())

        input_field = await self.get_input_field(page)
        await input_field.type('London')

        button = await self.get_submit_button(page)

        await asyncio.gather(
            waitForNavigation(page),
            button.click(),
        )

        cards_div = await querySelector(page, 'div.cards')

        if cards_div is None:
            raise WrongAnswer("Can't find <div> block with class 'cards'")

        await self.check_cards_in_the_page(page, 1)

    @dynamic_test(order=3)
    def test_add_city(self):
        asyncio.new_event_loop().run_until_complete(self.test_add_city_async())
        return CheckResult.correct()

    async def test_city_name_after_adding_async(self):

        browser = await self.launch_and_get_browser()
        page = await newPage(browser)
        await goto(page, self.get_url())

        input_field = await self.get_input_field(page)
        await input_field.type('Fairbanks')

        button = await self.get_submit_button(page)

        await asyncio.gather(
            waitForNavigation(page),
            button.click(),
        )

        cards_div = await querySelector(page, 'div.cards')

        if cards_div is None:
            raise WrongAnswer("Can't find <div> block with class 'cards'")

        await self.check_cards_in_the_page(page, 2)

    @dynamic_test(order=4)
    def test_city_name_after_adding(self):
        asyncio.new_event_loop().run_until_complete(self.test_city_name_after_adding_async())
        return CheckResult.correct()

    async def test_refresh_async(self):
        browser = await self.launch_and_get_browser()
        page = await newPage(browser)
        await goto(page, self.get_url())

        input_field = await self.get_input_field(page)
        await input_field.type('Idaho')

        button = await self.get_submit_button(page)

        await asyncio.gather(
            waitForNavigation(page),
            button.click(),
        )

        cards_div = await querySelector(page, 'div.cards')

        if cards_div is None:
            raise WrongAnswer("Can't find <div> block with class 'cards'")

        await self.check_cards_in_the_page(page, 3)

        await reload(page)

        await self.check_cards_in_the_page(page, 3)

    @dynamic_test(order=5)
    def test_refresh(self):
        asyncio.new_event_loop().run_until_complete(self.test_refresh_async())
        return CheckResult.correct()

    async def test_flash_message_async(self):
        print(123123)
        browser = await self.launch_and_get_browser()
        page = await newPage(browser)
        await goto(page, self.get_url())

        input_field = await self.get_input_field(page)
        await input_field.type('Idaho')

        button = await self.get_submit_button(page)

        await asyncio.gather(
            waitForNavigation(page),
            button.click(),
        )

        input_field = await self.get_input_field(page)
        await input_field.type('Idaho')

        button = await self.get_submit_button(page)

        await asyncio.gather(
            waitForNavigation(page),
            button.click(),
        )

        html = await page.content()

        if 'The city has already been added to the list!' not in html:
            raise WrongAnswer(
                f'If the user tires to add a city that is already was added you should print '
                f'"The city has already been added to the list!"')

        input_field = await self.get_input_field(page)
        await input_field.type('The city that doesn\'t exist!')

        button = await self.get_submit_button(page)

        await asyncio.gather(
            waitForNavigation(page),
            button.click(),
        )

        html = await page.content()

        if 'The city doesn\'t exist!' not in html:
            raise WrongAnswer(
                f'If the user tires to add a city that is already was added you should print "The city doesn\'t exist!"')

    @dynamic_test(order=6)
    def test_flash_message(self):
        asyncio.new_event_loop().run_until_complete(self.test_flash_message_async())
        return CheckResult.correct()

    async def test_delete_card_async(self):
        browser = await self.launch_and_get_browser()
        page = await newPage(browser)
        await goto(page, self.get_url())

        await self.check_cards_in_the_page(page, 3)

        cards = await querySelectorAll(page, 'div.card')
        card = cards[0]
        delete_button = await querySelector(card, 'button.delete-button')

        await asyncio.gather(
            waitForNavigation(page),
            delete_button.click(),
        )

        await self.check_cards_in_the_page(page, 2)

        cards = await querySelectorAll(page, 'div.card')
        card = cards[0]
        delete_button = await querySelector(card, 'button.delete-button')

        await asyncio.gather(
            waitForNavigation(page),
            delete_button.click(),
        )

        await self.check_cards_in_the_page(page, 1)

        cards = await querySelectorAll(page, 'div.card')
        card = cards[0]
        delete_button = await querySelector(card, 'button.delete-button')

        await asyncio.gather(
            waitForNavigation(page),
            delete_button.click(),
        )

        await self.check_cards_in_the_page(page, 0)

    @dynamic_test(order=7)
    def test_delete_card(self):
        asyncio.new_event_loop().run_until_complete(self.test_delete_card_async())
        return CheckResult.correct()


if __name__ == '__main__':
    FlaskProjectTest().run_tests()
