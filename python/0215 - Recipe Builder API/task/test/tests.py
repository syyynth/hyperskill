import asyncio
import copy
import os
import sqlite3

from hstest import FlaskTest, CheckResult, WrongAnswer
from hstest import dynamic_test
from hstest.dynamic.security.exit_handler import ExitHandler
import xml.etree.ElementTree as ET
import json
from pip._vendor import requests

class Ingredient:
    title: str
    amount: float
    measure: str
    def __eq__(self, other):
        if isinstance(other, Ingredient) == False:
            return False
        if self.title != other.title or self.amount != other.amount or self.measure != other.measure:
            return False
        else:
            return True
class Recipe_info:
    title = ''
    ingredients = []
    directions = []
    description = ''

    def __lt__(self, other):
        return self.title < other.title

    def __init__(self, recipe=None, ingredients=None):
        if recipe is None:
            return
        if isinstance(recipe, str):
            recipe_json = json.loads(recipe)
            self.title = recipe_json['title']
            for direction in recipe_json['directions']:
                self.directions.append(direction)
            self.description = recipe_json['description']
            self.ingredients = []
            for ingredient in recipe_json['ingredients']:
                i = Ingredient()
                i.title = ingredient['title']
                i.amount = ingredient['amount']
                i.measure = ingredient['measure']
                self.ingredients.append(i)
        elif isinstance(recipe, Recipe_info):
            copy_other = copy.deepcopy(recipe)
            self.title = copy_other.title
            self.directions = copy_other.directions
            self.ingredients = copy_other.ingredients
        elif isinstance(recipe, dict):
            self.__init__(json.dumps(recipe))


    def __eq__(self, other):
        if not isinstance(other, Recipe_info) and not isinstance(other, Recipe_info_with_id):
            return False
        if self.title != other.title:
            return False
        if len(self.directions) != len(other.directions):
            return False
        for direction in self.directions:
            if direction not in other.directions:
                return False
        if len(self.ingredients) != len(other.ingredients):
            return False
        for ingredient1 in self.ingredients:
            flag = True
            for ingredient2 in other.ingredients:
                if ingredient1.title == ingredient2.title and ingredient1.measure == ingredient2.measure and ingredient1.amount == ingredient2.amount:
                    flag = False
                    break
            if flag:
                return False
        return True

    def to_json(self):
        recipe_dict = copy.deepcopy(self).__dict__
        recipe_dict['ingredient'] = []
        for ingredient in self.ingredients:
            ingredient.amount = float(ingredient.amount)
            recipe_dict['ingredient'].append((ingredient.__dict__))
        del recipe_dict['ingredients']
        recipe_dict['ingredients'] = recipe_dict.pop('ingredient')
        jsonStr = json.dumps(recipe_dict)
        return jsonStr

    def to_json_with_id(self, id):
        recipe_dict = copy.deepcopy(self).__dict__
        recipe_dict['ingredient'] = []
        for ingredient in self.ingredients:
            ingredient.amount = float(ingredient.amount)
            recipe_dict['ingredient'].append((ingredient.__dict__))
        del recipe_dict['ingredients']
        recipe_dict['id'] = id
        recipe_dict['ingredients'] = recipe_dict.pop('ingredient')
        jsonStr = json.dumps(recipe_dict)
        return jsonStr
    def __str__(self):
        return self.to_json()
    def get_ingredients_url_parameters(self):
        return "|".join([ingredient.title for ingredient in self.ingredients])

class Recipe_info_with_id(Recipe_info) :
    id: int
    def __str__(self, without_id=True):
        if without_id:
            return self.to_json_without_id()
        else:
            return super.__str__()
    def from_other_recipe(self, recipe):
        copy_other = copy.deepcopy(recipe)
        self.title = copy_other.title
        self.directions = copy_other.directions
        self.ingredients = copy_other.ingredients
        self.description = copy_other.description
    def from_json(self, recipe: str):
        recipe_json = json.loads(recipe)
        self.title = recipe_json['title']
        self.directions = recipe_json['directions']
        self.ingredients = []
        for ingredient in recipe_json['ingredients']:
            i = Ingredient()
            i.title = ingredient['title']
            i.amount = ingredient['amount']
            i.measure = ingredient['measure']
            self.ingredients.append(i)
    def __init__(self, other=None, id=None):
        if other is None:
            return
        if isinstance(other, Recipe_info):
            self.from_other_recipe(other)
            self.id = id
        if isinstance(other, Recipe_info_with_id):
            self.from_other_recipe(other)
            self.id = other.id
            if id is not None:
                self.id = id
        elif isinstance(other, str):
            recipe_json = json.loads(other)
            self.from_json(other)
            try:
                self.id = recipe_json['id']
            except:
                if id is not None:
                    self.id = id

    def to_json(self):
        recipe_dict = copy.deepcopy(self).__dict__
        recipe_dict['ingredient'] = []
        for ingredient in self.ingredients:
            ingredient.amount = float(ingredient.amount)
            recipe_dict['ingredient'].append((ingredient.__dict__))
        del recipe_dict['ingredients']
        recipe_dict['ingredients'] = recipe_dict.pop('ingredient')
        jsonStr = json.dumps(recipe_dict)
        return jsonStr
    def to_json_without_id(self):
        recipe_dict = copy.deepcopy(self).__dict__
        recipe_dict['ingredient'] = []
        for ingredient in self.ingredients:
            ingredient.amount = float(ingredient.amount)
            recipe_dict['ingredient'].append((ingredient.__dict__))
        del recipe_dict['ingredients']
        del recipe_dict['id']
        recipe_dict['ingredients'] = recipe_dict.pop('ingredient')
        jsonStr = json.dumps(recipe_dict)
        return jsonStr
    def get_ingredients_url_parameters(self):
        return "|".join([ingredient.title for ingredient in self.ingredients])


def recipes_from_xml():
    list_recipes = []
    root_el = ET.fromstring('<recipes><recipe title="All-Day-Long Crockpot Beef" description="Instead of having to be in the kitchen for hours, why not try this easy crockpot recipe that will help you create a succulent dinner without spending hours in the kitchen."><ingredients><ingredient amount="907.2" measure="g">beef</ingredient><ingredient amount="10" measure="ml">black pepper</ingredient><ingredient amount="2" measure="each">garlic</ingredient><ingredient amount="2" measure="each">onion soup mix</ingredient><ingredient amount="10" measure="ml">worcestershire sauce</ingredient><ingredient amount="5" measure="ml">steak sauce</ingredient><ingredient amount="3" measure="each">carrots</ingredient><ingredient amount="2" measure="each">celery</ingredient><ingredient amount="1" measure="each">sweet red bell peppers</ingredient><ingredient amount="1" measure="each">onions</ingredient><ingredient amount="118" measure="ml">water</ingredient><ingredient amount="118" measure="ml">tomato juice</ingredient></ingredients><directions><direction>Cut beef roast into serving-sized portions.</direction><direction>Use more beef if you need more than 6 servings.</direction><direction>Brown beef in a bit of vegetable oil, although you can skip this step if rushed for time.</direction><direction>Slice onion and separate into rings.</direction><direction>Dice the peeled carrots, dice the celery and slice the peppers into thin strips or circles.</direction><direction>Place these into bottom of crockpot.</direction><direction>Sprinkle the beef pieces with fresh ground black pepper, minced garlic and the onion soup mix.</direction><direction>Place on top of the vegetables.</direction><direction>Mix the steak sauce and worcestershire sauce in a small</direction><direction>Pour this over the meat.</direction><direction>Turn the crockpot to High for 30 minutes, or, if you\'re in a hurry, skip this step.</direction><direction>Turn to Low, cover and cook for 7 to 9 hours.</direction><direction>Keep the crockpot covered as much as possible throughout cooking time.</direction><direction>A crockpot can be used to cook this type of meal for a varied amount of time, depending on your schedule.  It is not important that you take the meat and vegetables out at a specific amount of time.  One or two hours either way usually makes no difference.</direction><direction>When ready to serve, dip meat and vegetables out of pot with a slotted spoon.  Use the liquid as is or turn crockpot to High and thicken liquid with a little</direction></directions></recipe><recipe title="All-Day-Long Potato Soup" description="Easy crock pot potato soup. Serve with chopped green onions and slice cheddar cheese. SUPERB! Absolutely wonderful."><ingredients><ingredient amount="680.4" measure="g">potatoes</ingredient><ingredient amount="1" measure="each">onions</ingredient><ingredient amount="15" measure="ml">butter</ingredient><ingredient amount="1" measure="each">vegetable stock cubes</ingredient><ingredient amount="15" measure="ml">parsley leaves</ingredient><ingredient amount="710" measure="ml">water</ingredient><ingredient amount="237" measure="ml">milk</ingredient><ingredient amount="59" measure="ml">all-purpose flour</ingredient></ingredients><directions><direction>Place the first six ingredients in your slow cooker and cook all day on the low setting.</direction><direction>About &#189;  to one hour before serving; add milk and</direction><direction>Once the soup starts to thicken, it is ready to serve.</direction><direction>This simple slow cooker potato soup from scratch is a mainstay in our family.  We frequently vary the recipe as follows:</direction><direction>Stir in &#188; pound (125 g) of shredded cheese just prior to serving for cheese potato soup. A can of evaporated milk may be substituted for the regular milk.</direction><direction>When serving, top with crispy</direction><direction>Combine cheese and bacon as noted in both variations above.</direction></directions></recipe><recipe title="Good As Gold Chicken (Like Kfc\'s and Boston\'s)" description="If you\'re family loves chicken, they will simply enjoy eating this scrumptious dish!"><ingredients><ingredient amount="59" measure="ml">vegetable oil</ingredient><ingredient amount="15" measure="ml">honey</ingredient><ingredient amount="15" measure="ml">lime juice</ingredient><ingredient amount="1.3" measure="ml">paprika</ingredient><ingredient amount="1" measure="x">seasoned salt</ingredient><ingredient amount="4" measure="each">chicken breasts</ingredient></ingredients><directions><direction>Mix ingredients (except chicken) in a saucepan and warm just to melt honey.</direction><direction>Arrange chicken breast-side-up in a square</direction><direction>Bake uncovered at 400 degrees about 35 to 40 minutes.</direction><direction>Basting pieces without turning them, 3 or 4 times during baking.</direction><direction>Immediately upon removing from oven, seal baking dish or pan tightly in foil and let stand 15 to 20 minutes before serving.</direction></directions></recipe><recipe title=\"100% Parmesan Chicken\" description=\"Add some cheese to your succulent chicken with this delicious recipe that uses parmesan cheese and a variety of spices.\"><ingredients><ingredient amount=\"6\" measure=\"each\">chicken breasts</ingredient><ingredient amount=\"30\" measure="ml">butter</ingredient><ingredient amount="118" measure="ml">Parmesan cheese</ingredient><ingredient amount="59" measure="ml">bread crumbs</ingredient><ingredient amount="5" measure="ml">oregano</ingredient><ingredient amount="5" measure="ml">parsley flakes</ingredient><ingredient amount="1.3" measure="ml">paprika</ingredient><ingredient amount="1.3" measure="ml">salt</ingredient><ingredient amount="1.3" measure="ml">black pepper</ingredient></ingredients><directions><direction>Heat</direction><direction>Dip chicken in margarine; coat with combined remaining ingredients. Place in prepared pan. Bake 20 to 25 minutes or until tender.</direction><direction>Substitute &#8539; to &#188; teaspoon ground red pepper for black pepper.</direction></directions></recipe><recipe title="10 Minute Sichuan/Szechuan Chicken" description="Quick, easy and tasty.  Why order out for Chinese when it\'s so easy to make at home.  Low in fat only 223 calories per serving with great flavor. If you are quick you can have it ready in only 10 minutes, 15 minutes at the most!"><ingredients><ingredient amount="4" measure="each">chicken breasts</ingredient><ingredient amount="23" measure="ml">vinegar</ingredient><ingredient amount="45" measure="ml">cornstarch</ingredient><ingredient amount="5" measure="ml">sugar</ingredient><ingredient amount="15" measure="ml">vegetable oil</ingredient><ingredient amount="59" measure="ml">water</ingredient><ingredient amount="3" measure="cloves">garlic</ingredient><ingredient amount="6" measure="each">scallions, spring or green onions</ingredient><ingredient amount="75" measure="ml">soy sauce, tamari</ingredient><ingredient amount="0.6" measure="ml">cayenne pepper</ingredient></ingredients><directions><direction>Cut chicken into cubes.</direction><direction>Lightly toss with cornstarch in bag to coat.</direction><direction>Heat oil in skillet or wok, medium-high heat.</direction><direction>Stir-fry chicken and garlic until lightly browned.</direction><direction>Add soy sauce, vinegar, sugar and water.</direction><direction>Cover and cook 3 minutes or until chicken is cooked through.</direction><direction>Add green onions and cayenne; cook uncovered about 2 minutes longer.</direction></directions></recipe></recipes>')
    for recipe_el in root_el:
        recipe = Recipe_info()
        recipe.title = recipe_el.attrib['title']
        recipe.description = recipe_el.attrib['description']
        recipe.directions = []
        for direction in recipe_el.find("directions"):
            recipe.directions.append(direction.text)
        ingredients = recipe_el.find("ingredients")
        recipe.ingredients = []
        for ingredient_el in ingredients:
            ingredient = Ingredient()
            ingredient.title = ingredient_el.text
            ingredient.amount = float(ingredient_el.attrib['amount'])
            ingredient.measure = ingredient_el.attrib['measure']
            recipe.ingredients.append(ingredient)
        list_recipes.append(recipe)
    return list_recipes

class FlaskProjectTest(FlaskTest):
    source = 'app'
    list_recipes = []
    list_added_recipes = []
    recipe_name_table = ""
    ingredient_name_table = ""
    wrong_answers = \
        [
            "The database must contain a table with {} (named {} or {})",#0
            "{} route should return code 200, now code is {}", #1
            "{} {} key should be in the json response", #2
            "{} response should not be empty", #3
            "{} route should return '{}' if no recipes added, now '{}'", #4
            "{} route should return '{}' If not enough ingredients, now '{}'",  # 5
            "{} route should return json with {} keys, now '{}'",  # 6
            "{} route should return correct json response, if recipe added, now response: '{}'",  # 7
            "{} route, id added recipe must be a digit", #8
            "{} route, id must not be static", #9
            "{} route, should return 404 status code if recipe with id={} not added, now status code is {}",  # 10
            "{} route should return a list of recipes, according to the list of specified ingredients, now number recipes is '{}', but expected '{}'",  # 11
            "{} route, {} from recipe should be '{}', now '{}'",  # 12
            "{} route, the number of ingredients in the recipe does not correspond to the original, now {}, expected {}",  # 13
            "{} route, one of the ingredients of the original recipe is not returned, title='{}', measure='{}', amount='{}'",  # 14
            "{} route should return {} status code, if no recipe with specified id, now status code is '{}'",  # 15
            "{} route should delete recipe and return {} status code, if recipe with specified id found, now status code is '{}'",  # 16
            "{} route, 'directions' from json recipe must be a list ",  # 17
            "{}' route should update recipe and return 204 if recipe with id {} exists, now status code is {}", #18
            "{}' route, invalid json response: {}", #19
            "{}' route should return '[]' If there are no prescriptions that meet the restrictions, now response '{}'", #20
            "{}' route, another recipe was expected, number directions not checked", #21
            "Since the recipe(s) have already been added to the system, the output format should be a list of recipes []", #22
            "{} route should return a list of recipes in json format, now the route returns a list of strings. Look at example #5", # 23
            "{} route should return a list of recipes in the correct format. See example #5",  # 24
            "{}, {} key should not be in the json response",  # 25
        ]
    connection_error = "Could not establish a {} connection to {}."
    links = \
    [
        "{}api/recipe", #0
        "{}api/recipe?ingredients={}", #1
        "{}api/recipe/new", #2
        "{}api/recipe/{}",  # 3
        "{}api/recipe?ingredients={}&max_directions={}",  # 4
    ]
    strings = \
    [
        "No recipe here yet", #0
    ]
    json_responses = \
        [
            {"error": strings[0]},
            []
        ]

    def my_init(self):
        self.list_recipes = recipes_from_xml()

    def __init__(self, source_name: str = ''):
        super().__init__(source_name)
        self.my_init()
    def check_exist_table(self, table_name:str):
        con = sqlite3.connect('recipes.db')
        cursor = con.cursor()
        sql_query = """SELECT count(name) FROM sqlite_master  
                  WHERE type='table' and name='{}';"""
        cursor.execute(sql_query.format(table_name))
        res = cursor.fetchall()
        if res[0][0] == 1:
            con.close()
            return True
        else:
            con.close()
            return False
    def check_table_columns(self, table_name, list_columns):
        con = sqlite3.connect('recipes.db')
        cursor = con.cursor()
        sql_query = "SELECT name FROM PRAGMA_TABLE_INFO('{}')"
        cursor.execute(sql_query.format(table_name))
        res = cursor.fetchall()
        list_column_names = []
        for tuple in res:
            name = tuple[0]
            list_column_names.append(name)
        for name in list_columns:
            if name not in list_column_names:
                raise WrongAnswer(f"Table '{table_name}' must contain a column named '{name}'")

    async def test_database_structure(self):
        if not os.path.exists("recipes.db"):
            raise WrongAnswer("Strange, the database file is not involved. You may not have named the database correctly (recipes.db).")
        #check data base structure
        if self.check_exist_table("recipe"):
            self.recipe_name_table = "recipe"
        elif self.check_exist_table("recipes"):
            self.recipe_name_table = "recipes"
        else:
            raise WrongAnswer(self.wrong_answers[0].format("recipes", "recipe", "recipes"))
        if self.check_exist_table("ingredient"):
            self.ingredient_name_table = "ingredient"
        elif self.check_exist_table("ingredients"):
            self.ingredient_name_table = "ingredients"
        else:
            raise WrongAnswer(self.wrong_answers[0].format("ingredients", "ingredient", "ingredients"))
        #table columns
        self.check_table_columns(self.recipe_name_table, ['id', 'title', 'description'])
        self.check_table_columns(self.ingredient_name_table, ['id', 'title', 'measure', 'amount'])
        await self.check_data_base(self.list_added_recipes)

    def check_recipes_str(self, recipes:list, content:str, recipe_added, enough_ingredients):
        try:
            recipes_dict = json.loads(content)
        except:
            raise WrongAnswer(self.wrong_answers[7].format(self.links[1].format("GET /", "..."), content))
        if recipe_added and enough_ingredients:
            if not content:
                raise WrongAnswer(self.wrong_answers[3].format(self.links[1].format("GET /", "...")))
            if len(recipes) != len(recipes_dict):
                raise WrongAnswer(self.wrong_answers[11].format(self.links[1].format("GET /", "..."), len(recipes_dict), len(recipes),))
            if type(recipes_dict) != list:
                raise WrongAnswer(self.wrong_answers[22])
            for recipe in recipes_dict:
                if type(recipe) == str:
                    raise WrongAnswer(self.wrong_answers[23].format(self.links[1].format("GET /", "...")))
                if type(recipe) != dict:
                    raise WrongAnswer(self.wrong_answers[24].format(self.links[1].format("GET /", "...")))
                if "title" not in recipe.keys():
                    raise WrongAnswer(self.wrong_answers[2].format(self.links[1].format("GET /", "..."), "'title'"))
                if "directions" not in recipe.keys():
                    raise WrongAnswer(self.wrong_answers[2].format(self.links[1].format("GET /", "..."), "'directions'"))
                if "ingredients" not in recipe.keys():
                    raise WrongAnswer(self.wrong_answers[2].format(self.links[1].format("GET /", "..."), "ingredients"))
                if "id" not in recipe.keys():
                    raise WrongAnswer(self.wrong_answers[2].format(self.links[3].format("GET /", "id"), "id"))
                if not "description" in recipe.keys():
                    raise WrongAnswer(self.wrong_answers[2].format(self.links[3].format("GET /", "id"), "'description'"))
                if not isinstance(recipe['directions'], list):
                    raise WrongAnswer(self.wrong_answers[17].format(self.links[3].format("GET /", "id")))
                if len(recipe.keys()) > 5:
                    raise WrongAnswer(
                        self.wrong_answers[6].format(self.links[1].format("GET /", "..."), 5, len(recipe.keys())))
        elif recipe_added == False:
            if recipes_dict != self.json_responses[0]:
                raise WrongAnswer(self.wrong_answers[4].format(self.links[1].format("GET /", "..."), str(self.json_responses[0]), content))
        elif recipe_added and not enough_ingredients:
            if recipes_dict != self.json_responses[1]:
                raise WrongAnswer(self.wrong_answers[5].format(self.links[1].format("GET /", "..."), str(self.json_responses[1]), content))

    async def test_get_recipe_by_ingredients(self, recipes: list, recipe_added=True, enough_ingredients=True):
        try:
            r = requests.get(self.links[1].format(self.get_url(), recipes[0].get_ingredients_url_parameters()))
        except requests.exceptions.ConnectionError as e:
            raise WrongAnswer(self.connection_error.format(e.request.method, e.request.url.split('?')[0]))
        if r.status_code != 200:
            raise WrongAnswer(self.wrong_answers[1].format(self.links[1].format("GET /", "..."), r.status_code))
        content = r.content.decode('UTF-8')
        self.check_recipes_str(recipes, content, recipe_added, enough_ingredients)

    async def test_get_recipe_by_ingredients_max_directions(self, recipe: Recipe_info, max_directions=0, exists_result=False):
        try:
            r = requests.get(self.links[4].format(self.get_url(), recipe.get_ingredients_url_parameters(), max_directions))
        except requests.exceptions.ConnectionError as e:
            raise WrongAnswer(self.connection_error.format(e.request.method, e.request.url.split('?')[0]))
        if r.status_code != 200:
            raise WrongAnswer(self.wrong_answers[1].format(self.links[1].format("GET /", "..."), r.status_code))
        content = r.content.decode('UTF-8')
        try:
            dict_result = json.loads(content)
        except:
            raise WrongAnswer(self.wrong_answers[19].format(self.links[4].format("GET /", "...","..."), content))
        if not exists_result:
            if len(dict_result) != 0:
                raise WrongAnswer(self.wrong_answers[20].format(self.links[4].format("GET /", "...","..."), content))
        else:
            recipe_from_db = Recipe_info(dict_result[0])
            if len(recipe_from_db.directions) > max_directions:
                raise WrongAnswer(self.wrong_answers[20].format(self.links[4].format("GET /", "...","...")))

    async def test_sorting(self):
        ingredients = '|'.join([recipe.get_ingredients_url_parameters() for recipe in self.list_added_recipes])
        try:
            r = requests.get(self.links[1].format(self.get_url(), ingredients))
        except requests.exceptions.ConnectionError as e:
            raise WrongAnswer(self.connection_error.format(e.request.method, e.request.url.split('?')[0]))
        if r.status_code != 200:
            raise WrongAnswer(self.wrong_answers[1].format(self.links[1].format("GET /", "..."), r.status_code))
        content = r.content.decode("UTF-8")
        recipes_list_dict = None
        try:
            recipes_list_dict = json.loads(content)
        except:
            raise WrongAnswer("Error converting received response to json object")
        list_recipes = []
        for json_recipe in recipes_list_dict:
            list_recipes.append(Recipe_info(json_recipe))
        sorted_list = []
        for r in list_recipes:
            sorted_list.append(r)
        sorted_list.sort(reverse = True)
        for i in range(len(list_recipes)):
            if sorted_list[i]!=list_recipes[i]:
                raise WrongAnswer(self.links[1].format("GET /", "...")+", improperly sorted recipes");
    def check_recipe_str_get_by_id(self, recipe: Recipe_info, content: str, id:int):
        try:
            recipe_dict = json.loads(content)
        except:
            raise WrongAnswer(self.wrong_answers[7].format(self.links[3].format("GET /", id), content))
        if not content:
            raise WrongAnswer(self.wrong_answers[3].format(self.links[3].format("GET /", id)))
        if "title" not in recipe_dict.keys():
            raise WrongAnswer(self.wrong_answers[2].format(self.links[3].format("GET /", id), "'title'"))
        if "directions" not in recipe_dict.keys():
            raise WrongAnswer(self.wrong_answers[2].format(self.links[3].format("GET /", id), "'directions'"))
        if "ingredients" not in recipe_dict.keys():
            raise WrongAnswer(self.wrong_answers[2].format(self.links[3].format("GET /", id), "'ingredients'"))
        if "description" not in recipe_dict.keys():
            raise WrongAnswer(self.wrong_answers[2].format(self.links[3].format("GET /", id), "'description'"))
        if not isinstance(recipe_dict['directions'], list):
            raise WrongAnswer(self.wrong_answers[17].format(self.links[3].format("GET /", id)))
        if "id" in recipe_dict.keys():
            raise WrongAnswer(self.wrong_answers[25].format(self.links[3].format("GET /", id), "'id'"))
        if len(recipe_dict.keys()) > 4:
            raise WrongAnswer(
                self.wrong_answers[6].format(self.links[3].format("GET /", id), 4, len(recipe_dict.keys())))
        if recipe.title != recipe_dict['title']:
            raise WrongAnswer(self.wrong_answers[12].format(self.links[3].format("GET /", id), 'title', recipe.title, recipe_dict['title']))
        if recipe.directions != recipe_dict['directions']:
            raise WrongAnswer(self.wrong_answers[12].format(self.links[3].format("GET /", id), 'directions', recipe.directions, recipe_dict['directions']))
        link = self.links[3].format("GET /", id)
        try:
            if len(recipe.ingredients) != len(recipe_dict['ingredients']):
                raise WrongAnswer(self.wrong_answers[13].format(link, len(recipe_dict['ingredient']), len(recipe.ingredients)))
        except KeyError:
            raise WrongAnswer("Make sure you added all the ingredients")
        self.check_ingredients(recipe.ingredients, recipe_dict['ingredients'], id)
    def check_ingredients(self, recipe_ingredients:list, json_ingredients:list, id):
        for ingredient_recipe in recipe_ingredients:
            flag_exists = False
            for ingredient_json in json_ingredients:
                if ingredient_json['title'] == ingredient_recipe.title\
                        and ingredient_json['measure'] == ingredient_recipe.measure\
                        and str(ingredient_json['amount']) == str(ingredient_recipe.amount):
                    flag_exists = True
                    break
            if not flag_exists:
                raise WrongAnswer(self.wrong_answers[14].format(self.links[3].format("GET /", id), ingredient_recipe.title, ingredient_recipe.measure, ingredient_recipe.amount))

    async def test_del_recipe_by_id(self, id:int, recipe_added=False, recipe: Recipe_info=None):
        try:
            r = requests.delete(self.links[3].format(self.get_url(), id))
        except requests.exceptions.ConnectionError as e:
            raise WrongAnswer(self.connection_error.format(e.request.method, e.request.url.split('?')[0]))
        if not recipe_added:
            if r.status_code != 404:
                raise WrongAnswer(self.wrong_answers[15].format(self.links[3].format("DELETE /", id), 404, r.status_code))
        else:
            if r.status_code != 204:
                raise WrongAnswer(self.wrong_answers[16].format(self.links[3].format("DELETE /", id), 204, r.status_code))
            else:
                for recipe in self.list_added_recipes:
                    if recipe.id == id:
                        self.list_added_recipes.remove(recipe)
                        break
    async def test_get_recipe_by_id(self, id:int, recipe_added=False, recipe: Recipe_info=None):
        try:
            r = requests.get(self.links[3].format(self.get_url(), id))
        except requests.exceptions.ConnectionError as e:
            raise WrongAnswer(self.connection_error.format(e.request.method, e.request.url.split('?')[0]))
        if not recipe_added:
            if r.status_code != 404:
                raise WrongAnswer(self.wrong_answers[10].format(self.links[3].format(self.get_url(), id), id, r.status_code))
        else:
            content = r.content.decode("UTF-8")
            self.check_recipe_str_get_by_id(recipe, content, id)
    def check_post_recipe_respond(self, content):
        if not content:
            raise WrongAnswer(self.wrong_answers[7].format(self.links[2].format("POST /", ), content))
        try:
            json_dict = json.loads(content)
        except:
            raise WrongAnswer(self.wrong_answers[7].format(self.links[2].format("POST /"), content))
        if "id" not in json_dict.keys():
            raise WrongAnswer(self.wrong_answers[2].format(self.links[2].format("POST /"), "id"))
        if len(json_dict.keys()) > 1:
            raise WrongAnswer(self.wrong_answers[6].format(self.links[1].format("GET /", "..."), len(json_dict.keys())))
        if not str(json_dict['id']).isdigit() and str(int(json_dict['id'])) == str(json_dict['id']):
            raise WrongAnswer(self.wrong_answers[8].format(self.links[2].format("POST /")))
        if len(self.list_recipes) != 0:
            for recipe in self.list_added_recipes:
                if recipe.id == int(json_dict['id']):
                    raise WrongAnswer(self.wrong_answers[9].format(self.links[2].format("POST /")))

    async def check_data_base(self, list_recipes):
        con = sqlite3.connect('recipes.db')
        cursor = con.cursor()
        sql_query = """SELECT count(*) FROM {}"""
        if len(list_recipes) == 0:
            cursor.execute(sql_query.format(self.recipe_name_table))
            res = cursor.fetchall()
            if res[0][0] != 0:
                con.close()
                raise WrongAnswer(
                    "The database should now be empty and should not contain any recipes. Perhaps your database is open in another program and the tests cannot remove it")
            cursor.execute(sql_query.format(self.ingredient_name_table))
            res = cursor.fetchall()
            if res[0][0] != 0:
                con.close()
                raise WrongAnswer("Now the database should be empty and it should not store recipe ingredients")
        else:
            cursor.execute(sql_query.format(self.recipe_name_table))
            res = cursor.fetchall()
            if res[0][0] != len(list_recipes):
                con.close()
                raise WrongAnswer("Now the number of recipes is {}, expected {}".format(res[0][0], len(list_recipes)))
            cursor.execute(sql_query.format(self.ingredient_name_table))
            res = cursor.fetchall()
            if res[0][0] == 0:
                con.close()
                raise WrongAnswer("Recipe ingredients are not stored in the database")
            sql_query = f"SELECT * FROM {self.ingredient_name_table};"
            cursor.execute(sql_query)
            res = cursor.fetchall()
            list_ingredients = []
            for tup in res:
                title = tup[1]
                measure = tup[2]
                amount = tup[3]
                ing = Ingredient()
                ing.title = title
                ing.amount = amount
                ing.measure = measure
                list_ingredients.append(ing)
            for i in list_ingredients:
                if list_ingredients.count(i) > 1:
                    con.close()
                    raise WrongAnswer(
                        "Ingredients in the database must be stored in a single copy, duplicates take up a lot of space. The ingredients are now kept in multiple copies")
            for r in list_recipes:
                for ingredient in r.ingredients:
                    if ingredient not in list_ingredients:
                        con.close()
                        raise WrongAnswer(
                            f"Ingredient '{ingredient.title}' was not found in the database, although it was in a previously added recipe (title recipe '{r.title}'). This ingredient may have been in another recipe that was previously removed.Or you did not update the data correctly (PUT).")
            sql_query = f"SELECT title FROM {self.recipe_name_table};"
            cursor.execute(sql_query)
            res = cursor.fetchall()
            list_names = []
            for tup in res:
                name = tup[0]
                list_names.append(name)
            for r in list_recipes:
                if r.title not in list_names:
                    con.close()
                    raise WrongAnswer(f"No recipe with the title {r.title} is found in the database")
        con.close()



    async def test_post_recipe(self, recipe:Recipe_info):
        try:
            r = requests.post(self.links[2].format(self.get_url()), json=str(recipe))
        except requests.exceptions.ConnectionError as e:
            raise WrongAnswer(self.connection_error.format(e.request.method, e.request.url.split('?')[0]))
        if r.status_code != 200:
            raise WrongAnswer(self.wrong_answers[1].format(self.links[0].format("POST /"), r.status_code))
        content = r.content.decode("UTF-8")
        self.check_post_recipe_respond(content)
        json_dict = json.loads(content)
        self.list_added_recipes.append(Recipe_info_with_id(recipe, int(json_dict['id'])))

    async def test_put_recipe(self, id, recipe, recipe_exists=False):
        url = self.links[3].format(self.get_url(), id)
        json_recipe = recipe.to_json()
        try:
            r = requests.put(url, json=json_recipe)
        except requests.exceptions.ConnectionError as e:
            raise WrongAnswer(self.connection_error.format(e.request.method, e.request.url.split('?')[0]))
        if recipe_exists:
            if r.status_code != 204:
                raise WrongAnswer( self.wrong_answers[18].format(self.links[3].format("PUT /", id), id, r.status_code))
            for r in self.list_added_recipes:
                if r.id == int(id):
                    self.list_added_recipes.remove(r)
                    self.list_added_recipes.append(Recipe_info_with_id(recipe, id))
                    break

        if not recipe_exists:
            if r.status_code != 404:
                raise WrongAnswer(
                    "GET '/{}' route should return 404 if no recipes with id {} exists".format(url, id));

    @dynamic_test(order=-1)
    def test_1(self):
        ExitHandler.revert_exit()
        print("Test database (structure)")
        asyncio.get_event_loop().run_until_complete(
            self.test_database_structure())
        return CheckResult.correct()

    @dynamic_test(order=0)
    def test0(self):
        ExitHandler.revert_exit()
        print("Check database data")
        asyncio.get_event_loop().run_until_complete(
            self.check_data_base(self.list_added_recipes))
        return CheckResult.correct()

    @dynamic_test(order=1)
    def test1(self):
        ExitHandler.revert_exit()
        print("Get recipe by ingredients, no recipe added")
        asyncio.get_event_loop().run_until_complete(self.test_get_recipe_by_ingredients([self.list_recipes[0]], False, False))
        return CheckResult.correct()

    @dynamic_test(order=2)
    def test2(self):
        ExitHandler.revert_exit()
        print("Add recipe")
        asyncio.get_event_loop().run_until_complete(self.test_post_recipe(self.list_recipes[0]))
        asyncio.get_event_loop().run_until_complete(self.check_data_base(self.list_added_recipes))
        return CheckResult.correct()

    @dynamic_test(order=3)
    def test3(self):
        ExitHandler.revert_exit()
        print("Get recipe by added recipe ingredients")
        asyncio.get_event_loop().run_until_complete(self.test_get_recipe_by_ingredients([self.list_recipes[0]], True, True))
        return CheckResult.correct()

    @dynamic_test(order=4)
    def test4(self):
        ExitHandler.revert_exit()
        print("Get recipe by invalid recipe ingredients")
        asyncio.get_event_loop().run_until_complete(self.test_get_recipe_by_ingredients([self.list_recipes[1]], True, False))
        return CheckResult.correct()

    @dynamic_test(order=5)
    def test5(self):
        ExitHandler.revert_exit()
        print("Add second recipe")
        asyncio.get_event_loop().run_until_complete(self.test_post_recipe(self.list_recipes[3]))
        asyncio.get_event_loop().run_until_complete(self.check_data_base(self.list_added_recipes))
        return CheckResult.correct()

    @dynamic_test(order=6)
    def test6(self):
        ExitHandler.revert_exit()
        print("Get recipe by second recipe ingredients")
        asyncio.get_event_loop().run_until_complete(self.test_get_recipe_by_ingredients([self.list_recipes[3]], True, True))
        return CheckResult.correct()

    @dynamic_test(order=7)
    def test7(self):
        ExitHandler.revert_exit()
        print("Get recipe by invalid recipe ingredients")
        asyncio.get_event_loop().run_until_complete(self.test_get_recipe_by_ingredients([self.list_recipes[4]], True, False))
        return CheckResult.correct()

    @dynamic_test(order=8)
    def test8(self):
        ExitHandler.revert_exit()
        print("Get recipe by invalid id")
        asyncio.get_event_loop().run_until_complete(self.test_get_recipe_by_id(99))
        return CheckResult.correct()

    @dynamic_test(order=9)
    def test9(self):
        ExitHandler.revert_exit()
        print("Get recipe by valid id, from added recipe")
        asyncio.get_event_loop().run_until_complete(self.test_get_recipe_by_id(self.list_added_recipes[0].id, True, self.list_added_recipes[0]))
        return CheckResult.correct()

    @dynamic_test(order=10)
    def test10(self):
        ExitHandler.revert_exit()
        print("Get another recipe with valid id, from added recipe")
        asyncio.get_event_loop().run_until_complete(
            self.test_get_recipe_by_id(self.list_added_recipes[1].id, True, self.list_added_recipes[1]))
        return CheckResult.correct()

    @dynamic_test(order=11)
    def test11(self):
        ExitHandler.revert_exit()
        print("Delete recipe with valid id, from added recipes")
        asyncio.get_event_loop().run_until_complete(self.test_del_recipe_by_id(self.list_added_recipes[1].id, True, self.list_added_recipes[1]))
        asyncio.get_event_loop().run_until_complete(self.check_data_base(self.list_added_recipes))
        return CheckResult.correct()

    @dynamic_test(order=12)
    def test12(self):
        ExitHandler.revert_exit()
        print("Delete recipe, with not added recipe id")
        asyncio.get_event_loop().run_until_complete(self.test_del_recipe_by_id(99, False))
        asyncio.get_event_loop().run_until_complete(self.check_data_base(self.list_added_recipes))
        return CheckResult.correct()



    @dynamic_test(order=14)
    def test14(self):
        print("Check put incorrect id")
        asyncio.get_event_loop().run_until_complete(self.test_put_recipe(99, self.list_recipes[4], False))
        asyncio.get_event_loop().run_until_complete(self.check_data_base(self.list_added_recipes))
        return CheckResult.correct()

    changed_recipe_id = 0
    new_recipe = None

    @dynamic_test(order=15)
    def test15(self):
        self.changed_recipe_id = self.list_added_recipes[0].id
        self.new_recipe = self.list_recipes[4]
        print("Check put correct id and correct recipe")
        asyncio.get_event_loop().run_until_complete(self.test_put_recipe(self.list_added_recipes[0].id, self.list_recipes[4], True))
        asyncio.get_event_loop().run_until_complete(self.check_data_base(self.list_added_recipes))
        return CheckResult.correct()

    @dynamic_test(order=16)
    def test16(self):
        ExitHandler.revert_exit()
        print("Add third recipe")
        asyncio.get_event_loop().run_until_complete(self.test_post_recipe(self.list_recipes[3]))
        return CheckResult.correct()

    @dynamic_test(order=17)
    def test17(self):
        print("Check get changed recipe")
        asyncio.get_event_loop().run_until_complete(
            self.test_get_recipe_by_id(self.changed_recipe_id, True, self.new_recipe))
        return CheckResult.correct()

    @dynamic_test(order=18)
    def test18(self):
        print("Check max_directions")
        asyncio.get_event_loop().run_until_complete(
            self.test_get_recipe_by_ingredients_max_directions(self.list_added_recipes[0], len(self.list_added_recipes[0].directions), True))
        return CheckResult.correct()

    @dynamic_test(order=19)
    def test19(self):
        print("Check max_directions")
        asyncio.get_event_loop().run_until_complete(
            self.test_get_recipe_by_ingredients_max_directions(self.list_added_recipes[0], len(self.list_added_recipes[0].directions)-1, False))
        return CheckResult.correct()

    @dynamic_test(order=20)
    def test20(self):
        print("Get recipes by all ingredients from all added recipes")
        asyncio.get_event_loop().run_until_complete(
            self.test_sorting())
        return CheckResult.correct()

if __name__ == '__main__':
    try: os.remove("recipes.db")
    except: pass
    FlaskProjectTest().run_tests()
    try: os.remove("recipes.db")
    except: pass
