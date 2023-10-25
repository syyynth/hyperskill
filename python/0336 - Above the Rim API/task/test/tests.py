import asyncio
import json
import random
from hstest import FlaskTest, CheckResult, WrongAnswer
from hstest import dynamic_test
from hstest.dynamic.security.exit_handler import ExitHandler
import requests
from bs4 import BeautifulSoup
import sqlite3
import os


class SQLite3Test:

    """It's recommended to keep the sequence:
    1. Create object SQLite3Check
    2. Check is file exists
    3. Establish connection
    4. Check is table exists
    5. Check are columns exists
    6. Do the rest of tests on tables: is column primary key, not null

    To do tests: is unique and is foreign key"""

    cursor_message = f"There is no cursor to connection."  # Is it proper message?
    no_table_message = f"There is no table you are looking for."

    def __init__(self, file_name):  # file_name -> string
        self.file_name = file_name
        self.conn = None
        self.cursor = None

    def is_file_exist(self):
        if not os.path.exists(self.file_name):
            raise WrongAnswer(f"The file '{self.file_name}' does not exist or is outside of the script directory.")

    def connect(self):
        ans = self.is_file_exist()
        if ans:
            return ans
        try:
            self.conn = sqlite3.connect(self.file_name)
            self.cursor = self.conn.cursor()
        except sqlite3.OperationalError as err:
            raise WrongAnswer(f"DataBase {self.file_name} may be locked. An error was returned when trying to connect: {err}.")

    def close(self):
        try:
            self.conn.close()
        except AttributeError:
            raise WrongAnswer(self.cursor_message)

    def run_query(self, query):
        try:
            lines = self.cursor.execute(f"{query}")
        except AttributeError:
            raise WrongAnswer(self.cursor_message)
        except sqlite3.OperationalError as err:
            self.close()
            raise WrongAnswer(f"Error '{err}' occurred while trying to read from database '{self.file_name}'.")
        except sqlite3.DatabaseError as err:
            self.close()
            raise WrongAnswer(f"Error '{err}' occurred while trying to read from database '{self.file_name}'.")
        return lines

    def is_table_exist(self, name):  # table name -> string
        lines = self.run_query(f"SELECT count(name) FROM sqlite_master WHERE "
                               f"type='table' AND (name='{name.lower()}' OR name='{name.upper()}');").fetchall()
        if lines[0][0] == 0:
            self.close()
            raise WrongAnswer(f"There is no table named '{name}' in database {self.file_name}")

    def number_of_records(self, name, expected_lines):   # table name -> string, expected_lines -> integer
        lines = self.run_query(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
        if lines != expected_lines:
            self.close()
            raise WrongAnswer(f"Wrong number of records in table {name}. Expected {expected_lines}, found {lines}")

    def is_column_exist(self, name, names):  # table name -> string, column names -> list of strings for all columns, or list with one string for one column
        lines = self.run_query(f'select * from {name}').description
        if len(names) != 1:
            if sorted(names) != sorted([line[0].lower() for line in lines]):
                self.close()
                raise WrongAnswer(f"There is something wrong in table {name}. Found column names: {[line[0] for line in lines]}. Expected {names}'")
        else:
            if not any([names[0] == c_name for c_name in [line[0].lower() for line in lines]]):
                self.close()
                raise WrongAnswer(f"There is something wrong in table {name}. Found column names: {[line[0] for line in lines]}. Expected to find '{names[0]}'")

    def table_info(self, name, column, attribute):   # table name -> string, column name -> string, attr ("PK" Primary Key; "NN" Not null)
        lines = self.run_query(f"PRAGMA table_info({name})").fetchall()
        lines = [line[:1] + tuple([line[1].lower()]) + line[2:] for line in lines]
        if column not in [line[1] for line in lines]:
            raise WrongAnswer(f"There is no column {column}.")
        for line in lines:
            if attribute == "PK":
                if line[1] == column and line[5] != 1:
                    self.close()
                    raise WrongAnswer(f"There is no PRIMARY KEY parameter in {name} on column {column}.")
            elif attribute == "NN":
                if line[1] == column and line[3] != 1:
                    raise WrongAnswer(f"There is no NOT NULL parameter in {name} on column {column}.")

    def is_unique(self, name, column):  # table name -> string, column name -> string
        lines = self.run_query(f"SELECT inf.name FROM pragma_index_list('{name}') as lst, pragma_index_info(lst.name) as inf WHERE lst.[unique] = 1;").fetchall()
        lines = [tuple([line[0].lower()]) + line[1:] for line in lines]
        if not any([column in line for line in lines]):
            raise WrongAnswer(f"There is no UNIQUE parameter in {name} on column {column}.")
        return True

    def is_foreign_key(self, name, column):  # table name -> string, column name -> string
        lines = self.run_query(f"SELECT * FROM pragma_foreign_key_list('{name}');").fetchall()
        lines = [line[:2] + tuple([line[2].lower()]) + tuple([line[3].lower()])
                 + tuple([line[4].lower()]) + line[5:] for line in lines]
        if not any([column in line for line in lines]):
            raise WrongAnswer(f"There is no FOREIGN KEY parameter in {name} on column {column}.")
        return True


class FlaskProjectTest(FlaskTest):
    source = 'basketball_API'

    def check_json(self, output_dict, expect_dict):
        #  print(type(output_dict), type(expect_dict))
        if len(output_dict) != len(expect_dict):
            #  print("First condition")
            return True
        for key in expect_dict.keys():
            if key not in output_dict.keys():
                #  print("Second condition")
                return True
            if expect_dict[key] != output_dict[key]:
                #  print("Third condition")
                return True
        return False

    async def test_home_page(self):
        r = requests.get(self.get_url())
        if r.status_code != 200:
            raise WrongAnswer(f"Home page should return code 200. Found {r.status_code}.")
        content = r.content.decode('UTF-8')
        if content.lower().count("<h1>") != 1 or content.lower().count("</h1>") != 1:
            raise WrongAnswer("Checking Home Page.\nThere should be one tag <h1> and one tag </h1>.")
        p_tags = 8
        if content.lower().count("<p>") != p_tags or content.lower().count("/p") != p_tags:
            raise WrongAnswer(f"Checking Home Page.\nThere should be {p_tags} tags <p> and {p_tags} tags </p>.")
        soup = BeautifulSoup(content, 'html.parser')
        list_all_h1 = soup.find_all('h1')
        if 'Welcome to the "Above the Rim" API!' not in list_all_h1[0].text:
            raise WrongAnswer('Checking Home Page.\nThere is no welcome text inside the tag <h1>: Welcome to the "Above the Rim" API!')
        list_all_p = soup.find_all('p')
        ps = ["/api/v1/teams GET all teams",
              "/api/v1/teams POST add team",
              "/api/v1/games GET all games",
              "/api/v1/games POST add game",
              "/api/v1/team/%SHORT% GET a team statistics",
              "/api/v2/games POST add a new game",
              "/api/v2/games GET all games",
              "/api/v2/games/%GAME_ID% POST updated quarters"]
        if any([txt not in [l.text for l in list_all_p] for txt in ps]):
            raise WrongAnswer(f'Checking Home Page.\nThere is some mistake in <p> tags!\nExpected:\n{sorted(ps)}\nFound:\n{sorted([txt.text for txt in list_all_p])}')

    async def test_random_page(self):
        r = requests.get("/".join([self.get_url(), ''.join(random.choice("abcdefghijk") for i in range(5))]))
        if r.status_code != 404:
            raise WrongAnswer(f"Checking not existing page.\nNot existing page should return code 404. Found {r.status_code}.")
        content = r.content.decode('UTF-8')
        expected = {"success": False, "data": "Wrong address"}
        try:
            content = json.loads(content)
        except json.decoder.JSONDecodeError:
            raise WrongAnswer(f'Checking not existing page.\nRequest do not return JSON data.\nExpected {expected}.\nFound {content}.')
        #  expected = json.loads(json.dumps({"success": False, "data": "Wrong address"}))
        if self.check_json(content, expected):
            raise WrongAnswer(f'Checking not existing page.\nWrong JSON format. \n'
                              f'Expected\n{dict(sorted(expected.items()))}, \n'
                              f'Found:\n{dict(sorted(content.items() if isinstance(content, dict) else content))}')

    async def test_get_method(self, api_address, expected, code, text):
        r = requests.get("/".join([self.get_url(), api_address]))
        if r.status_code != code:
            raise WrongAnswer(f"{text} GET method at {api_address} should return code {code}. Found {r.status_code}.")
        content = r.content.decode('UTF-8')
        try:
            content = json.loads(content)
        except json.decoder.JSONDecodeError:
            raise WrongAnswer(f'{text} GET method at {api_address} do not return JSON data.\nExpected {expected}.\nFound {content}.')
        if self.check_json(content, expected):
            raise WrongAnswer(f'{text} GET method at {api_address} return wrong JSON format. \n'
                              f'Expected\n{dict(sorted(expected.items()))}, \n'
                              f'Found:\n{dict(sorted(content.items() if isinstance(content, dict) else content))}')
        return

    async def test_post_method(self, api_address, input_post, expected, code, text):
        r = requests.post("/".join([self.get_url(), api_address]), json=input_post)
        if r.status_code != code:
            raise WrongAnswer(f"{text} POST method at {api_address} should return code {code}. Found {r.status_code}.")
        content = r.content.decode('UTF-8')
        try:
            content = json.loads(content)
        except json.decoder.JSONDecodeError:
            raise WrongAnswer(f'{text} POST method at {api_address} do not return JSON data.\nExpected {expected}.\nFound {content}.')
        if self.check_json(content, expected):
            raise WrongAnswer(f'{text} POST method at {api_address} return wrong JSON format. \n'
                              f'Expected\n{dict(sorted(expected.items()))}, \n'
                              f'Found:\n{dict(sorted(content.items() if isinstance(content, dict) else content))}')
        return

    async def test_patch_method(self, api_address, input_post, expected, code, text):
        r = requests.patch("/".join([self.get_url(), api_address]), json=input_post)
        if r.status_code != code:
            raise WrongAnswer(f"{text} PATCH method should return code {code}.")
        content = r.content.decode('UTF-8')
        try:
            content = json.loads(content)
        except json.decoder.JSONDecodeError:
            raise WrongAnswer('Request do not return JSON data.')
        if self.check_json(content, expected):
            raise WrongAnswer(f'Wrong JSON format. \n'
                              f'Expected\n{dict(sorted(expected.items()))}, \n'
                              f'Found:\n{dict(sorted(content.items() if isinstance(content, dict) else content))}')
        return

    @dynamic_test(order=1)
    def test1(self):
        ExitHandler.revert_exit()
        print("Checking Home Page.")
        asyncio.get_event_loop().run_until_complete(self.test_home_page())
        return CheckResult.correct()

    @dynamic_test(order=2)
    def test2(self):
        ExitHandler.revert_exit()
        print("Checking not existing page.")
        asyncio.get_event_loop().run_until_complete(self.test_random_page())
        return CheckResult.correct()

    @dynamic_test(order=3)
    def test3(self):
        ExitHandler.revert_exit()
        print("Checking database and deleting data.")
        db_name = "instance/db.sqlite3"
        database = SQLite3Test(db_name)
        database.connect()
        database.is_file_exist()
        tables = {"teams": {"id": ["PK"], "short": ["NN", "UN"], "name": ["NN", "UN"]},
                  "games": {"id": ["PK"], "home_team_id": ["FK"], "visiting_team_id": ["FK"], "home_team_score": [], "visiting_team_score": []},
                  "quarters": {"id": ["PK"], "game_id": ["FK"], "quarters": []}}
        for table, columns in tables.items():
            database.is_table_exist(table)
            database.is_column_exist(table, [column for column in columns.keys()])
            for column in columns.keys():
                for param in columns[column]:
                    if param == "UN":
                        database.is_unique(table, column)
                    if param not in ["UN", "FK"]:
                        database.table_info(table, column, param)
                    if param == "FK":
                        database.is_foreign_key(table, column)
        for table in tables:
            database.run_query(f"DELETE FROM {table}")

        database.conn.commit()
        database.close()
        return CheckResult.correct()

#  stage 2

    @dynamic_test(order=4)
    def test4(self):
        ExitHandler.revert_exit()
        print("Checking GET without data.")
        output = {"success": True, "data": {}}
        asyncio.get_event_loop().run_until_complete(self.test_get_method("/api/v1/teams", output, 200, "Successful"))
        return CheckResult.correct()

    @dynamic_test(order=5)
    def test5(self):
        ExitHandler.revert_exit()
        print("POST method at /api/v1/teams")
        input_post = [{"short": "PRW", "name": "Prague Wizards"}, {"short": "CHG", "name": "Chicago Gulls"}]
        expected = {"data": "Team has been added", "success": True}
        for post in input_post:
            asyncio.get_event_loop().run_until_complete(self.test_post_method("/api/v1/teams", post, expected, 201, "Successful"))
        return CheckResult.correct()

    @dynamic_test(order=6)
    def test6(self):
        ExitHandler.revert_exit()
        print("GET method at /api/v1/teams")
        expected = {"success": True, "data": {"CHG": "Chicago Gulls", "PRW": "Prague Wizards"}}
        asyncio.get_event_loop().run_until_complete(self.test_get_method("/api/v1/teams", expected, 200, "Successful"))
        return CheckResult.correct()

#  stage 3

    @dynamic_test(order=7)
    def test7(self):
        ExitHandler.revert_exit()
        print("POST method at /api/v1/games")
        input_post = [{"home_team": "CHG", "visiting_team": "PRW", "home_team_score": 123, "visiting_team_score": 89}, {"home_team": "PRW", "visiting_team": "CHG", "home_team_score": 76, "visiting_team_score": 67}]
        expected = {"data": "Game has been added", "success": True}
        for post in input_post:
            asyncio.get_event_loop().run_until_complete(self.test_post_method("/api/v1/games", post, expected, 201, "Successful"))
        return CheckResult.correct()

    @dynamic_test(order=8)
    def test8(self):
        ExitHandler.revert_exit()
        print("Proper GET method at /api/v1/games")
        expected = {"success": True, "data": {"1": "Chicago Gulls 123:89 Prague Wizards", "2": "Prague Wizards 76:67 Chicago Gulls"}}
        asyncio.get_event_loop().run_until_complete(self.test_get_method("/api/v1/games", expected, 200, "Successful"))
        return CheckResult.correct()

    @dynamic_test(order=9)
    def test9(self):
        ExitHandler.revert_exit()
        print("POST method at /api/v1/games with wrong team")
        input_post = [{"home_team": "CHG", "visiting_team": "PRS", "home_team_score": 123, "visiting_team_score": 89}]
        expected = {"data": "Wrong team short", "success": False}
        for post in input_post:
            asyncio.get_event_loop().run_until_complete(self.test_post_method("/api/v1/games", post, expected, 400, "Wrong"))
        return CheckResult.correct()

#  stage 4

    @dynamic_test(order=10)
    def test10(self):
        ExitHandler.revert_exit()
        print("GET method at /api/v1/team/%SHORT% with existing team short.")
        expected = {"data": {"lost": 1, "name": "Prague Wizards", "short": "PRW", "win": 1}, "success": True}
        asyncio.get_event_loop().run_until_complete(self.test_get_method("/api/v1/team/PRW", expected, 200, "Successful"))
        return CheckResult.correct()

    @dynamic_test(order=11)
    def test11(self):
        ExitHandler.revert_exit()
        print("GET method at /api/v1/team/%SHORT% with wrong team short.")
        expected = {"data": "There is no team PRS", "success": False}
        asyncio.get_event_loop().run_until_complete(self.test_get_method("/api/v1/team/PRS", expected, 400, "Wrong"))
        return CheckResult.correct()

    @dynamic_test(order=12)
    def test12(self):
        ExitHandler.revert_exit()
        print("POST method at /api/v1/teams with wrong SHORT")
        input_post = [{"short": "PR", "name": "Prague Wizards"}, {"short": "", "name": "Chicago Gulls"}]
        expected = {"data": "Wrong short format", "success": False}
        for post in input_post:
            asyncio.get_event_loop().run_until_complete(self.test_post_method("/api/v1/teams", post, expected, 400, "Wrong"))
        return CheckResult.correct()

#  stage 5

    @dynamic_test(order=13)
    def test13(self):
        ExitHandler.revert_exit()
        print("POST method at /api/v2/games")
        input_post = [{"home_team": "PRW", "visiting_team": "CHG"}]
        expected = {"data": 3, "success": True}
        for post in input_post:
            asyncio.get_event_loop().run_until_complete(self.test_post_method("/api/v2/games", post, expected, 201, "Successful"))
        return CheckResult.correct()

    @dynamic_test(order=14)
    def test14(self):
        ExitHandler.revert_exit()
        print("GET method at /api/v2/games.")
        expected = {"success": True, "data": {"1": "Chicago Gulls 123:89 Prague Wizards",
                                              "2": "Prague Wizards 76:67 Chicago Gulls",
                                              "3": "Prague Wizards 0:0 Chicago Gulls"}}
        asyncio.get_event_loop().run_until_complete(self.test_get_method("/api/v2/games", expected, 200, "Successful"))
        return CheckResult.correct()

    @dynamic_test(order=15)
    def test15(self):
        ExitHandler.revert_exit()
        print("PATCH method at /api/v2/games/3")
        input_post = [{"quarters": "12:15"}, {"quarters": "21:18"}]
        expected = {"data": "Score updated", "success": True}
        for post in input_post:
            asyncio.get_event_loop().run_until_complete(self.test_post_method("/api/v2/games/3", post, expected, 201, "Successful"))
        return CheckResult.correct()

    @dynamic_test(order=16)
    def test16(self):
        ExitHandler.revert_exit()
        print("GET method at /api/v2/games.")
        expected = {"success": True, "data": {"1": "Chicago Gulls 123:89 Prague Wizards",
                                              "2": "Prague Wizards 76:67 Chicago Gulls",
                                              "3": "Prague Wizards 33:33 Chicago Gulls (12:15,21:18)"}}
        asyncio.get_event_loop().run_until_complete(self.test_get_method("/api/v2/games", expected, 200, "Successful"))
        return CheckResult.correct()

    @dynamic_test(order=17)
    def test17(self):
        ExitHandler.revert_exit()
        print("GET method at /api/v1/games.")
        expected = {"success": True, "data": {"1": "Chicago Gulls 123:89 Prague Wizards",
                                              "2": "Prague Wizards 76:67 Chicago Gulls",
                                              "3": "Prague Wizards 33:33 Chicago Gulls"}}
        asyncio.get_event_loop().run_until_complete(self.test_get_method("/api/v1/games", expected, 200, "Successful"))
        return CheckResult.correct()
#  !!!
    @dynamic_test(order=18)
    def test18(self):
        ExitHandler.revert_exit()
        print("PATCH method at /api/v2/games")
        input_post = [{"id": 6, "quarters": "12:20"}]
        expected = {'data': 'There is no game with id 6', 'success': False}
        for post in input_post:
            asyncio.get_event_loop().run_until_complete(self.test_post_method("/api/v2/games/6", post, expected, 400, "Wrong"))
        return CheckResult.correct()

    @dynamic_test(order=19)
    def test19(self):
        ExitHandler.revert_exit()
        print("PATCH method at /api/v2/games/3")
        input_post = [{"quarters": "12:21"}, {"quarters": "20:12"}, {"quarters": "3:9"}]
        expected = {"data": "Score updated", "success": True}
        for post in input_post:
            asyncio.get_event_loop().run_until_complete(self.test_post_method("/api/v2/games/3", post, expected, 201, "Successful"))
        return CheckResult.correct()

    @dynamic_test(order=20)
    def test20(self):
        ExitHandler.revert_exit()
        print("GET method at /api/v2/games.")
        expected = {"success": True, "data": {"1": "Chicago Gulls 123:89 Prague Wizards",
                                              "2": "Prague Wizards 76:67 Chicago Gulls",
                                              "3": "Prague Wizards 68:75 Chicago Gulls (12:15,21:18,12:21,20:12,3:9)"}}
        asyncio.get_event_loop().run_until_complete(self.test_get_method("/api/v2/games", expected, 200, "Successful"))
        return CheckResult.correct()

    @dynamic_test(order=21)
    def test21(self):
        ExitHandler.revert_exit()
        print("GET method at /api/v1/games.")
        expected = {"success": True, "data": {"1": "Chicago Gulls 123:89 Prague Wizards",
                                              "2": "Prague Wizards 76:67 Chicago Gulls",
                                              "3": "Prague Wizards 68:75 Chicago Gulls"}}
        asyncio.get_event_loop().run_until_complete(self.test_get_method("/api/v1/games", expected, 200, "Successful"))
        return CheckResult.correct()


if __name__ == '__main__':
    FlaskProjectTest().run_tests()
