import os

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Recipe(db.Model):
    __tablename__ = 'Recipe'

    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    ingredients = db.relationship('RecipeIngredient', backref="recipe", lazy=True, cascade="all, delete-orphan")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Ingredient(db.Model):
    __tablename__ = 'Ingredient'

    ingredient_id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String, nullable=False)
    recipes = db.relationship('RecipeIngredient', backref="ingredient", lazy=True, cascade="all, delete-orphan")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Unit(db.Model):
    __tablename__ = 'Unit'

    unit_id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class RecipeIngredient(db.Model):
    __tablename__ = 'RecipeIngredient'

    recipe_ingredient_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.recipe_id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('Ingredient.ingredient_id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('Unit.unit_id'), nullable=False)
    amount = db.Column(db.String, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
