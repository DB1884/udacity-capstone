from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Recipe(db.Model):
    __tablename__ = 'Recipe'

    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    ingredients = db.relationship('RecipeIngredient', backref="recipe", lazy=True, cascade="all, delete-orphan")


class Ingredient(db.Model):
    __tablename__ = 'Ingredient'

    ingredient_id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String, nullable=False)
    recipes = db.relationship('RecipeIngredient', backref="ingredient", lazy=True, cascade="all, delete-orphan")


class Unit(db.Model):
	__tablename__ = 'Unit'

	unit_id = db.Column(db.Integer, primary_key=True)
	unit_name = db.Column(db.String, nullable=False)


class RecipeIngredient(db.Model):
  __tablename__ = 'RecipeIngredient'

  recipe_ingredient_id = db.Column(db.Integer, primary_key=True)
  recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.recipe_id'), nullable=False)
  ingredient_id = db.Column(db.Integer, db.ForeignKey('Ingredient.ingredient_id'), nullable=False)
  unit_id = db.Column(db.Integer, db.ForeignKey('Unit.unit_id'), nullable=False)
  amount = db.Column(db.String, nullable=False)
