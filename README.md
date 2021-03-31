# No Frills Recipe

# Recipe API Backend

This API is designed to store recipes, ingredients and units of measurement in a standardised format. While very basic at this stage, just supporting CRUD functions on recipes and ingredients, the motivation is to provide a platform in future that allows users to select a number of recipes and then prepare a shopping list based on the required ingredients.

The API is running live at https://no-frills-recipe.herokuapp.com/

## Getting Started

### Installing Dependencies

#### Python 3.8.5

The project has been tested using Python 3.8.5 but should work on most versions of Python 3. Instructions for installing the newest version of Python on your machine can be found in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Setup a virtual envrionment for running the for your platform. Again instructions for doing this can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once the virtual envrionment is up and running and you are within that environment, install dependencies by running:

```pip install -r requirements.txt```

This will install all of the required packages we selected within the `requirements.txt` file.

## Local database setup

With Postgres running, load some test data into a database using the recipe.psql file provided. From the main project directory in your terminal terminal run the following to create the db, apply migrations and load test data:

```
createdb recipeapp
source setup.sh
python manage.py db upgrade
psql recipeapp < recipe.psql
```

You may need to update the database URL depending on your settings.

## Running the app locally

Once you've installed the dependencies and setup the database, you're ready to run the app locally. To do this, execute the following:

```
export FLASK_APP=app
export FLASK_ENV=development
flask run
```

Three test users have been configured in Auth0 with the following roles and credentials:

* Admin:

This role has access to all routes.

Email: admin@test.com
Password: Z72Ttoon5k6y

* Chef:

This role has access to add new recipes, ingredients and units and amend existing recipes. 

Email: chef@test.com
Password: Z72Ttoon5k6y

* Viewer:

This role has access to view recipes, ingredients and units

Email: viewer@test.com
Password: Z72Ttoon5k6y

To obtain a JWT for any of these users please login using the link:

https://fsnd-recipe.eu.auth0.com/authorize?audience=recipe&response_type=token&client_id=YMrwzoezQAt2heWLhSqBj69VgaV43OZ5&redirect_uri=http://localhost:5000/

The token will be in the URL bar following successful login and can then be used to make test requests. Alternatively existing valid tokens for each role are also provided within the setup.sh file.

## Error Handling

Errors are returned by the API as JSON objects in the following format:

```
{
    "success": False,
    "error": 404,
    "message": "Not found"
}
```

The API may return one of four expected error types when requests fail:

- 400: Bad request
- 401: Unauthorised
- 403: Forbidden
- 404: Not found
- 405: Method not allowed
- 422: Unprocessable entity

## Endpoints

GET /recipes

- Fetches a list of recipe names
- Request arguments: None
- Returns: An object with two keys, success and recipes.
- Example request:
    `curl -H "Authorization: Bearer $ADMIN_TOKEN" https://no-frills-recipe.herokuapp.com/recipes`
- Example response:
    ```
    {
        "success": True,
        "recipes": [
            (1: "Lasagne"},
            {2: "Apple Pie"},
            {3: "Vanilla Cheesecake"},
            {4: "Spaghetti Carbonara"}
        ]
    }
    ```

GET /recipes/<int:recipe_id>

- Fetches the details of a recipe with a specific ID
- Request arguments: None
- Returns: An object with two keys, success, and recipe. Recipe is a dictionary object with the keys name, description and ingredients. Ingredients is a list containing objects with keys name, amount and unit.
- Example request:
    `curl -H "Authorization: Bearer $ADMIN_TOKEN" https://no-frills-recipe.herokuapp.com/recipes/1`
- Example response:
    ```
    {
        "success": True,
        "recipe": {
            "name" : "Apple Pie",
            "description" : "A rich and hearty pasta dish",
            "ingredients": [
                {
                    "name": "Apples",
                    "amount": "500",
                    "unit": "grams"
                },
                {
                    "name": "Pie",
                    "amount": "500",
                    "unit": "grams",
                }
            ]
        }
    }
    ```

GET /ingredients

- Fetches a list of ingredient names
- Request arguments: None
- Returns: An object with two keys, success and ingredients.
- Example request:
    `curl -H "Authorization: Bearer $ADMIN_TOKEN" https://no-frills-recipe.herokuapp.com/ingredients`
- Example response:
    ```
    {
        "success": True,
        "ingredients": [
            {1: "Apples"},
            {2: "Pie"},
            {3: "Lasagna pasta"},
            {4: "Beef mince"},
            {5: "Eggs"},
            {6: "Parmesan cheese"}
        ]
    }
    ```

GET /units

- Fetches a list of unit names
- Request arguments: None
- Returns: An object with two keys, success and units.
- Example request:
    `curl -H "Authorization: Bearer $ADMIN_TOKEN" https://no-frills-recipe.herokuapp.com/units`
- Example response:
    ```
    {
        "success": True,
        "units": [
            {1: "grams"},
            {2: "mililitres"},
            {3: "tablespoons"},
            {4: "large"},
            {5: "medium"},
            {6: "teaspoons"},
            {7: "sheets"}
        ]
    }
    ```

POST /recipes

- Adds a new recipe name and description to the database
- Request arguments:
    ```
    {
        "recipe_name": recipe_name,
        "description": description,
    }
    ```
- Returns: An object with two keys, success and recipe which will be the new recipe ID.
- Example request:
    `curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $ADMIN_TOKEN" --data '{"recipe_name": "Cheese on toast", "description": "Hot gooey bread"}' https://no-frills-recipe.herokuapp.com/recipes`
- Example response:
    ```
    {
        "success": True,
        "recipe": 8,
    }
    ```

POST /ingredients

- Adds a new ingredient
- Request arguments:
    ```
    {
        "ingredient_name": ingredient_name,
    }
    ```
- Returns: An object with two keys, success and ingredient which will be the new ingredient ID.
- Example request:
    `curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $ADMIN_TOKEN" --data '{"recipe_name": "Cheese on toast"}' https://no-frills-recipe.herokuapp.com/ingredients`
- Example response:
    ```
    {
        "success": True,
        "recipe": 12,
    }
    ```

POST /units

- Adds a new unit to the database
- Request arguments:
    ```
    {
        "unit": unit_name,
    }
    ```
- Returns: An object with two keys, success and unit which will be the new recipe ID.
- Example request:
    `curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $ADMIN_TOKEN" --data '{"unit_name": "dessert spoons"}' https://no-frills-recipe.herokuapp.com/units`
- Example response:
    ```
    {
        "success": True,
        "recipe": 9,
    }
    ```

PATCH /recipes/<int:id>

- Updates the name and description of a recipe
- Request arguments:
    ```
    {
        "recipe_name": recipe_name,
        "description": description,
    }
    ```
- Returns: An object with two keys, success and recipe which will be the modified recipe ID.
- Example request:
    `curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer $ADMIN_TOKEN" --data '{"recipe_name": "Double cheese on toast", "description": "Hot double gooey bread"}' https://no-frills-recipe.herokuapp.com/recipes/12`
- Example response:
    ```
    {
        "success": True,
        "recipe": 12,
    }
    ```

PATCH /recipes/<int:id>/ingredients

- Add ingredients to a recipe
- Request arguments:
    ```
    {
        "recipe_ingredients": [
            {
                "ingredient_id": 1,
                "unit_id": 1,
                "amount": 250
            },
            {
                "ingredient_id": 2,
                "unit_id": 2,
                "amount": 100
            }
        ]
    }
    ```
- Returns: An object with two keys, success and recipe which will be the modified recipe ID.
- Example request:
    `curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer $ADMIN_TOKEN" --data '{"recipe_ingredients": [{"ingredient_id": 1, "unit_id": 1, "amount": 250}, {"ingredient_id": 1, "unit_id": 2, "amount": 5}]}' https://no-frills-recipe.herokuapp.com/recipes/1/ingredients`
- Example response:
    ```
    {
        "success": True,
        "recipe": 1,
    }
    ```

DELETE /recipes/<int:id>

- Deletes a recipe from the database
- Request arguments: None
- Returns: An object with two keys, success and delete which will include the deleted recipe ID.
- Example request:
    `curl -X DELETE -H "Authorization: Bearer $ADMIN_TOKEN" https://no-frills-recipe.herokuapp.com/recipes/1`
- Example response:
    ```
    {
        "success": True,
        "delete": 1
    }
    ```

DELETE /ingredients/<int:id>

- Deletes an ingredient from the database
- Request arguments: None
- Returns: An object with two keys, success and delete which will include the deleted ingredient ID.
- Example request:
    `curl -X DELETE -H "Authorization: Bearer $ADMIN_TOKEN" https://no-frills-recipe.herokuapp.com/ingredients/1`
- Example response:
    ```
    {
        "success": True,
        "delete": 1
    }
    ```

DELETE /units/<int:id>

- Deletes a unit from the database
- Request arguments: None
- Returns: An object with two keys, success and delete which will include the deleted unit ID.
- Example request:
    `curl -X DELETE -H "Authorization: Bearer $ADMIN_TOKEN" https://no-frills-recipe.herokuapp.com/units/1`
- Example response:
    ```
    {
        "success": True,
        "delete": 1
    }
    ```


## Testing

To run the tests, run
```
dropdb recipe_test
createdb recipe_test
psql recipe_test < recipe.psql
python test_app.py
```