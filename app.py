import os
import json
import sys
from flask import Flask, flash, render_template, request, abort, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from auth import AuthError, requires_auth
from models import db, Recipe, Ingredient, RecipeIngredient, Unit, setup_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object("config")

    setup_db(app)
    CORS(app)

    #  Routes
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({"success": True})

    @app.route("/recipes", methods=["GET"])
    @requires_auth("get:recipes")
    def get_recipes(token):
        recipes = Recipe.query.all()
        return jsonify({
            "success": True,
            "recipe": [{recipe.recipe_id: recipe.recipe_name} for recipe in recipes]
        })
        #return render_template("recipes.html", recipes=recipes)


    @app.route("/recipes/<int:id>", methods=["GET"])
    #@requires_auth("get:recipes")
    def get_recipe_details(id):
        recipe = Recipe.query.filter(Recipe.recipe_id == id).first_or_404()
        recipe = {
            "name": recipe.recipe_name,
            "description": recipe.description,
            "ingredients": [
                {
                    "name": ingredient.ingredient.ingredient_name,
                    "amount": ingredient.amount,
                    "unit": Unit.query.filter(Unit.unit_id == ingredient.unit_id).first_or_404().unit_name,
                }
                for ingredient in recipe.ingredients
            ]
        }
        return jsonify({
            "success": True,
            "recipe": recipe
        })
        #return render_template("recipe_details.html", recipe=recipe)


    @app.route("/ingredients", methods=["GET"])
    #@requires_auth("get:ingredients")
    def get_ingredients():
        ingredients = Ingredient.query.all()
        return jsonify({
            "success": True,
            "ingredients": [{ingredient.ingredient_id: ingredient.ingredient_name} for ingredient in ingredients]
        })
        #return render_template("ingredients.html", ingredients=ingredients)


    @app.route("/units", methods=["GET"])
    #@requires_auth("get:units")
    def get_units():
        units = Unit.query.all()
        return jsonify({
            "success": True,
            "units": [{unit.unit_id: unit.unit_name} for unit in units]
        })
        return render_template("units.html", units=units)


    @app.route("/recipes", methods=["POST"])
    #@requires_auth("post:recipes")
    def post_recipes():
        recipe_data = request.get_json()
        recipe = Recipe(
            recipe_name=recipe_data.get("recipe_name"),
            description=json.dumps(recipe_data.get("description")),
        )
        recipe.insert()
        return jsonify({
            "success": True,
            "recipe": recipe.recipe_id,
        })


    @app.route("/ingredients", methods=["POST"])
    #@requires_auth("post:ingredients")
    def post_ingredients():
        ingredient_data = request.get_json()
        ingredient = Ingredient(
            ingredient_name=ingredient_data.get("ingredient_name"),
        )
        ingredient.insert()
        return jsonify({
            "success": True,
            "ingredient": ingredient.ingredient_id,
        })


    @app.route("/units", methods=["POST"])
    #@requires_auth("post:units")
    def post_units():
        unit_data = request.get_json()
        unit = Unit(
            unit_name=unit_data.get("unit_name"),
        )
        unit.insert()
        return jsonify({
            "success": True,
            "unit": unit.unit_id,
        })


    @app.route("/recipes/<int:id>", methods=["PATCH"])
    #@requires_auth("patch:recipes")
    def patch_recipes(id):
        recipe_data = request.get_json()
        recipe = Recipe.query.filter(Recipe.recipe_id == id).first_or_404()
        recipe.recipe_name = recipe_data.get("recipe_name")
        recipe.description = recipe_data.get("description")
        recipe.update()
        return jsonify({
            "success": True,
            "recipe": recipe.recipe_id,
        })


    @app.route("/recipes/<int:id>/ingredients", methods=["PATCH"])
    #@requires_auth("patch:recipes")
    def patch_recipes_ingredients(id):
        recipe_data = request.get_json()
        for ingredient in recipe_data.get("recipe_ingredients"):
            recipe_ingredient = RecipeIngredient(
                recipe_id=id,
                ingredient_id=ingredient["ingredient_id"],
                unit_id=ingredient["unit_id"],
                amount=ingredient["amount"],
            )
            db.session.add(recipe_ingredient)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
        return jsonify({
            "success": True,
            "recipe": id,
        })


    @app.route("/recipes/<int:id>", methods=["DELETE"])
    #@requires_auth("delete:recipes")
    def delete_recipes(id):
        recipe = Recipe.query.filter(Recipe.recipe_id == id).first_or_404()
        recipe.delete()
        return jsonify({
            "success": True,
            "delete": recipe.recipe_id,
        })


    @app.route("/ingredients/<int:id>", methods=["DELETE"])
    #@requires_auth("delete:ingredients")
    def delete_ingredients(id):
        ingredient = Ingredient.query.filter(Ingredient.ingredient_id == id).first_or_404()
        ingredient.delete()
        return jsonify({
            "success": True,
            "delete": ingredient.ingredient_id,
        })


    @app.route("/units/<int:id>", methods=["DELETE"])
    #@requires_auth("delete:units")
    def delete_units(id):
        unit = Unit.query.filter(Unit.unit_id == id).first_or_404()
        unit.delete()
        return jsonify({
            "success": True,
            "delete": unit.unit_id,
        })


    # Error handlers
    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
            }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
            }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
            }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
            }), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error["description"],
            }), error.status_code


    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
