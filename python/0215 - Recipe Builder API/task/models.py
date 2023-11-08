from marshmallow import Schema, fields
from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker


class Base(DeclarativeBase):
    pass


class Direction(Base):
    __tablename__ = 'direction'

    id: Mapped[int] = mapped_column(primary_key=True)
    step: Mapped[str] = mapped_column(String(80), nullable=False)

    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipe.id'))

    recipe: Mapped['Recipe'] = relationship(back_populates='directions')


class Recipe(Base):
    __tablename__ = 'recipe'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(80), nullable=False)
    description: Mapped[str] = mapped_column(String(80), nullable=False)

    directions: Mapped[list['Direction']] = relationship(
        back_populates='recipe', cascade='all, delete'
    )
    ingredients: Mapped[list['Ingredient']] = relationship(
        back_populates='recipe', cascade='all, delete'
    )

    def to_dict(self, include_id=True):
        response = {
            'title': self.title,
            'description': self.description,
            'directions': [direction.step for direction in self.directions],
            'ingredients': [
                {'title': ingredient.title,
                 'measure': ingredient.measure,
                 'amount': ingredient.amount}
                for ingredient in self.ingredients
            ]
        }

        if include_id:
            response['id'] = self.id

        return response


class Ingredient(Base):
    __tablename__ = 'ingredient'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(80), nullable=False)
    measure: Mapped[str] = mapped_column(String(10), nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)

    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipe.id'))

    recipe: Mapped['Recipe'] = relationship(back_populates='ingredients')


class IngredientSchema(Schema):
    title = fields.String(required=True)
    measure = fields.String(required=True)
    amount = fields.Float(required=True)


class RecipeSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    directions = fields.List(fields.String(), required=True)
    ingredients = fields.List(fields.Nested(IngredientSchema), required=True)


db_path = '/recipes.db'
engine = create_engine(f'sqlite://{db_path}', echo=True)
Session = sessionmaker(bind=engine)
schema = RecipeSchema()
