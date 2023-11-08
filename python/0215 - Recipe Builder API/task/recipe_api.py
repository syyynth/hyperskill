import json
from http import HTTPStatus

from flask import Response, jsonify, request
from flask.views import MethodView
from marshmallow import ValidationError
from sqlalchemy import desc, select

from models import Direction, Ingredient, Recipe, Session, schema


class RecipeAPI(MethodView):
    def get(self, recipe_id=None) -> tuple[Response, HTTPStatus]:
        return self.get_by_ingredients() if recipe_id is None else self.get_by_id(recipe_id)

    def get_by_ingredients(self) -> tuple[Response, HTTPStatus]:
        with Session() as session:
            ingredients = set(request.args.get('ingredients', '').split('|'))
            max_directions = float(request.args.get('max_directions', float('inf')))

            recipies = session.execute(
                select(Recipe).order_by(desc(Recipe.title))
            ).scalars().all()

            if not recipies:
                return jsonify({'error': 'No recipe here yet'}), HTTPStatus.OK

            response = [recipe.to_dict() for recipe in recipies
                        if {ingredient.title for ingredient in recipe.ingredients} <= ingredients
                        and len(recipe.directions) <= max_directions]

            return jsonify(response), HTTPStatus.OK

    def get_by_id(self, recipe_id) -> tuple[Response, HTTPStatus]:
        with Session() as session:
            recipe = self._get_recipe(session, recipe_id)

            if recipe is None:
                return jsonify({'error': f'No recipe with id {recipe_id}'}), HTTPStatus.NOT_FOUND

            return jsonify(recipe.to_dict(include_id=False)), HTTPStatus.OK

    def post(self) -> tuple[Response, HTTPStatus]:
        try:
            title, description, directions, ingredients = self._get_request_body()
        except ValidationError:
            return jsonify(), HTTPStatus.BAD_REQUEST

        with Session.begin() as session:
            recipe = Recipe(title=title, description=description)

            session.add(recipe)
            session.flush()

            recipe.directions = self._add_directions(directions, recipe)
            recipe.ingredients = self._add_ingredients(ingredients, recipe)

            return jsonify({'id': recipe.id}), HTTPStatus.OK

    def delete(self, recipe_id) -> tuple[Response, HTTPStatus]:
        with Session.begin() as session:
            recipe = self._get_recipe(session, recipe_id)

            if not recipe:
                return jsonify({'error': f'No recipe with id {recipe_id}'}), HTTPStatus.NOT_FOUND

            session.delete(recipe)
            return jsonify(), HTTPStatus.NO_CONTENT

    def put(self, recipe_id) -> tuple[Response, HTTPStatus]:
        try:
            title, description, directions, ingredients = self._get_request_body()
        except ValidationError:
            return jsonify(), HTTPStatus.BAD_REQUEST

        with Session.begin() as session:
            recipe = self._get_recipe(session, recipe_id)

            if not recipe:
                return jsonify({'error': f'No recipe with id {recipe_id}'}), HTTPStatus.NOT_FOUND

            recipe.title = title
            recipe.description = description

            for direction in recipe.directions:
                session.delete(direction)
            for ingredient in recipe.ingredients:
                session.delete(ingredient)

            recipe.directions = self._add_directions(directions, recipe)
            recipe.ingredients = self._add_ingredients(ingredients, recipe)

            return jsonify(), HTTPStatus.NO_CONTENT

    def _get_recipe(self, session, recipe_id):
        return session.execute(
            select(Recipe).filter(Recipe.id == recipe_id)
        ).scalar()

    def _add_directions(self, directions, recipe):
        return [
            Direction(step=step, recipe_id=recipe.id)
            for step in directions
        ]

    def _add_ingredients(self, ingredients, recipe):
        return [
            Ingredient(recipe_id=recipe.id, **ingredient_data)
            for ingredient_data in ingredients
        ]

    def _get_request_body(self):
        req = json.loads(request.get_json())
        validated = schema.load(req)
        return validated['title'], validated['description'], validated['directions'], validated['ingredients']
