
import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app


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

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_successful_get_recipes(self):
        res = self.client().get("/recipes")
        data = json.loads(res.data)
        print(len(data["recipes"]))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["recipes"]))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
