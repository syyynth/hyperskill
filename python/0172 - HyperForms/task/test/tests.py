import sqlite3
from copy import copy
from itertools import repeat
from time import sleep
from urllib.error import HTTPError, URLError

import requests
from hstest import DjangoTest, CheckResult, WrongAnswer, dynamic_test

FORM_FIELDS = [
    ("name", "Your name", "text", 1),
    ("age", "Your age", "number", 1),
    ("favorite_book", "Your favorite book", "text", 1)
]


class HyperFormsUpdatingFieldsTest(DjangoTest):
    use_database = True

    def get_index_with_no_participants(self) -> CheckResult:
        try:
            index = self.read_page(self.get_url())
            if all(x in index.lower() for x in ["no participants", "be the first"]):
                return CheckResult.correct()
            else:
                return CheckResult.wrong(
                    "Seems like there is no line telling a first visitor to become the first participant...")
        except HTTPError:
            return CheckResult.wrong("Make sure the url is correct")
        except Exception as e:
            print(f'An unexpected exception has occurred: {str(e)}')

    def create_form_and_fields(self) -> CheckResult:
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.execute(
                """INSERT INTO forms_formmodel (`name`)
                VALUES (?)""",
                ("participants",))

            cursor.executemany(
                """INSERT INTO forms_formfield (`name`, `label`, `type`, `form_id`) 
                VALUES (?, ?, ?, ?)""",
                FORM_FIELDS)
            connection.commit()

            cursor.execute('SELECT `name`, `label`, `type`, `form_id` FROM forms_formfield')
            result = cursor.fetchall()
            for item in FORM_FIELDS:
                if item not in result:
                    return CheckResult.wrong(f"Check your FormField model: couldn't find the {item[0]} field.")
            return CheckResult.correct()

        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))
        except Exception as e:
            print(f'An unexpected exception has occurred: {str(e)}')

    def check_field(self, page, field_name):
        return all(x in page.lower() for x in ["<input", f'name="{field_name.lower()}"'])

    def check_button(self, page, button_value):
        return f'<button type="submit">{button_value}</button>'.lower() in page.lower()

    def get_register_page_with_form(self, fields_to_check):
        try:
            register_page = self.read_page(self.get_url('register'))
            if all(list(map(self.check_field, repeat(register_page), fields_to_check))):
                if self.check_button(register_page, "Submit"):
                    return CheckResult.correct()
                else:
                    return CheckResult.wrong(
                        'Register page should contain a "Submit" button.'
                    )
            else:
                return CheckResult.wrong(
                    'Register page should contain all of three fields with names "name", "age", "favorite_book"')
        except URLError:
            return CheckResult.wrong('Cannot connect to the register page.')

    def fill_in_the_form(self, data_to_fill) -> CheckResult:
        register_page = requests.get(self.get_url('register'))
        post_data = copy(data_to_fill)
        post_data.update({"csrfmiddlewaretoken": register_page.cookies.get("csrftoken")})
        filled_form = requests.post(self.get_url('register/'),
                                    cookies={"csrftoken": register_page.cookies.get("csrftoken")},
                                    data=post_data)
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT `value`, `record_id` FROM forms_formdata where record_id=2')
        except sqlite3.OperationalError:
            return CheckResult.wrong('Make sure you run the migrations, your FormData model should have the following fields: record_id, value')
        result = cursor.fetchall()
        try:
            if all(x[0].lower() in list(map(str.lower, list(data_to_fill.values()))) for x in result):
                if all(x[1] == result[0][1] for x in result):
                    return CheckResult.correct()
                else:
                    return CheckResult.wrong("Each form entry should be tied to one FormRecord.")
            else:
                return CheckResult.wrong("Seems like not everything inserted in the form is saved to FormData.")
        except AttributeError:
            return CheckResult.wrong("Seems like not everything inserted in the form is saved to FormData.")

    def check_data_on_index(self, data_to_check) -> CheckResult:
        index = self.read_page(self.get_url())
        if all(x in index.lower() for x in data_to_check):
            if all(x not in index.lower() for x in ["no participants", "be the first"]):
                return CheckResult.correct()
            else:
                return CheckResult.wrong(
                    "If there are participants in the club, the page should not tell people there are no participants!")
        else:
            return CheckResult.wrong("Cannot see the inserted form data on the main page!")

    def add_one_more_field(self) -> CheckResult:
        connection = sqlite3.connect(self.attach.test_database)
        cursor = connection.cursor()
        try:
            cursor.execute(
                """INSERT INTO forms_formfield (`name`, `label`, `type`, `form_id`) 
                VALUES (?, ?, ?, ?)""",
                ("town", "Your town", "text", 1))
            connection.commit()

            cursor.execute('SELECT `name`, `label`, `type`, `form_id` FROM forms_formfield')
            result = cursor.fetchall()
            FORM_FIELDS.append(("town", "Your town", "text", 1))
            for item in FORM_FIELDS:
                if item not in result:
                    return CheckResult.wrong("FormField doesn't seem to be saving new fields correctly.")
            return CheckResult.correct()

        except sqlite3.DatabaseError as err:
            return CheckResult.wrong(str(err))
        except Exception as e:
            print("An unexpected exception has occurred: ", str(e))

    @dynamic_test(order=1)
    def test_get_index_no_participants(self):
        return self.get_index_with_no_participants()

    @dynamic_test(order=2)
    def test_create_form_and_fields(self):
        return self.create_form_and_fields()

    @dynamic_test(order=3)
    def test_get_register_page_with_tree_fields(self):
        return self.get_register_page_with_form(["name", "age", "favorite_book"])

    @dynamic_test(order=4)
    def test_post_form_three_fields(self):
        return self.fill_in_the_form({"name": "Boba", "age": "22", "favorite_book": "Kuka"})

    @dynamic_test(order=5)
    def test_inserted_data_on_index_three_fields(self):
        return self.check_data_on_index(["boba", "22", "kuka"])

    @dynamic_test(order=6)
    def test_add_one_more_field(self):
        return self.add_one_more_field()

    @dynamic_test(order=7)
    def test_post_form_with_new_field(self):
        return self.fill_in_the_form({"name": "Biba", "age": "44", "favorite_book": "Keka", "town": "LolCity"})

    @dynamic_test(order=8)
    def test_inserted_data_on_index_new(self):
        return self.check_data_on_index(["boba", "22", "kuka", "biba", "44", "keka", "lolcity"])


if __name__ == '__main__':
    HyperFormsUpdatingFieldsTest().run_tests()
