import os
import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db

ADMIN_TOKEN = os.environ["ADMIN_TOKEN"]
CHEF_TOKEN = os.environ["CHEF_TOKEN"]
VIEWER_TOKEN = os.environ["VIEWER_TOKEN"]


class RecipeTestCase(unittest.TestCase):
    """This class represents the recipe test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "recipe_test"
        self.database_path = "postgresql://postgres:postgres@{}/{}".format(
            "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test GET routes with and without valid tokens
    def test_successful_get_recipes(self):
        res = self.client().get(
            "/recipes", headers={
                "Authorization": "Bearer {}".format(VIEWER_TOKEN)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["recipes"])

    def test_get_recipes_forbidden(self):
        res = self.client().get("/recipes")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_successful_get_recipe_and_404(self):
        res = self.client().get(
            "/recipes/1", headers={
                "Authorization": "Bearer {}".format(VIEWER_TOKEN)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["recipe"])
        res = self.client().get(
            "/recipes/1000", headers={
                "Authorization": "Bearer {}".format(VIEWER_TOKEN)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_get_recipe_405(self):
        res = self.client().post(
            "/recipes/1", headers={
                "Authorization": "Bearer {}".format(VIEWER_TOKEN)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)

    def test_get_recipe_forbidden(self):
        res = self.client().get("/recipes/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_successful_get_ingredients(self):
        res = self.client().get(
            "/ingredients", headers={
                "Authorization": "Bearer {}".format(VIEWER_TOKEN)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["ingredients"])

    def test_get_ingredients_forbidden(self):
        res = self.client().get("/ingredients")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_get_units(self):
        res = self.client().get(
            "/units", headers={
                "Authorization": "Bearer {}".format(VIEWER_TOKEN)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["units"])

    def test_get_units_forbidden(self):
        res = self.client().get("/units")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    # Test POST routes with and without valid tokens
    def test_successful_post_recipes(self):
        res = self.client().post(
            "/recipes",
            json={
                "recipe_name": "Lasagna",
                "description": "Garfields favourite"
            },
            headers={
                "Authorization": "Bearer {}".format(CHEF_TOKEN)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["recipe"])

    def test_post_recipes_forbidden(self):
        res = self.client().post(
            "/recipes",
            json={
                "recipe_name": "Lasagna",
                "description": "Garfields favourite"
            },
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_successful_post_ingredients(self):
        res = self.client().post(
            "/ingredients",
            json={
                "ingredient_name": "Milk chocolate",
            },
            headers={
                "Authorization": "Bearer {}".format(CHEF_TOKEN)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["ingredient"])

    def test_post_ingredients_forbidden(self):
        res = self.client().post(
            "/ingredients",
            json={
                "ingredient_name": "Milk chocolate",
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_successful_post_units(self):
        res = self.client().post(
            "/units",
            json={
                "unit_name": "chips",
            },
            headers={
                "Authorization": "Bearer {}".format(CHEF_TOKEN)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["unit"])

    def test_post_units_forbidden(self):
        res = self.client().post(
            "/units",
            json={
                "unit_name": "Milk chocolate",
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    # Test PATCH routes with and without valid tokens
    def test_successful_patch_recipes(self):
        res = self.client().patch(
            "/recipes/1",
            json={
                "recipe_name": "Lasagna",
                "description": "Odies favourite"
            },
            headers={
                "Authorization": "Bearer {}".format(CHEF_TOKEN)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["recipe"])

    def test_patch_recipes_forbidden(self):
        res = self.client().patch(
            "/recipes/1",
            json={
                "recipe_name": "Lasagna",
                "description": "Odies favourite"
            },
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_successful_patch_recipes_ingredients(self):
        res = self.client().patch(
            "/recipes/1/ingredients",
            json={
                "recipe_ingredients": [
                    {"ingredient_id": 4, "unit_id": 1, "amount": 250},
                    {"ingredient_id": 7, "unit_id": 1, "amount": 500},
                    {"ingredient_id": 10, "unit_id": 2, "amount": 3},
                    {"ingredient_id": 15, "unit_id": 1, "amount": 100}
                ]
            },
            headers={
                "Authorization": "Bearer {}".format(CHEF_TOKEN)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["recipe"], 1)

    def test_patch_recipes_ingredients_forbidden(self):
        res = self.client().patch(
            "/recipes/2/ingredients",
            json={
                "recipe_ingredients": [
                    {"ingredient_id": 4, "unit_id": 1, "amount": 250},
                    {"ingredient_id": 7, "unit_id": 1, "amount": 500},
                    {"ingredient_id": 10, "unit_id": 2, "amount": 3},
                    {"ingredient_id": 15, "unit_id": 1, "amount": 100}
                ]
            },
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    # Test DELETE routes with and without valid tokens
    def test_successful_delete_recipes(self):
        res = self.client().delete(
            "/recipes/4", headers={
                "Authorization": "Bearer {}".format(ADMIN_TOKEN)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["delete"], 4)

    def test_delete_recipes_forbidden(self):
        res = self.client().delete("/recipes/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_successful_delete_ingredients(self):
        res = self.client().delete(
            "/ingredients/1", headers={
                "Authorization": "Bearer {}".format(ADMIN_TOKEN)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["delete"], 1)

    def test_delete_ingredients_forbidden(self):
        res = self.client().delete("/ingredients/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    def test_delete_units(self):
        res = self.client().delete(
            "/units/5", headers={
                "Authorization": "Bearer {}".format(ADMIN_TOKEN)
            }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["delete"], 5)

    def test_delete_units_forbidden(self):
        res = self.client().delete("/units/5")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
