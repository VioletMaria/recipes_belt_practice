from flask.helpers import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re


class Recipe:
    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.under_thirty = data["under_thirty"]
        self.instructions = data["instructions"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate_recipe_update(recipes):
        is_valid = True
        if len(recipes["name"]) < 3:
            flash("Name must be at least 3 chracters.")
            is_valid = False
        if len(recipes["description"]) < 3:
            flash("Description must be at least 3 chracters.")
            is_valid = False
        if len(recipes["instructions"]) < 3:
            flash("Instructions must be at least 3 chracters.")
            is_valid = False
        if "under_thirty" not in recipes:
            flash("Must select yes or no.")
            is_valid = False
        if len(recipes["created_at"]) < 1:
            flash("You need to choose a date.")
            is_valid = False

        return is_valid


    @classmethod
    def add_recipe(cls,data):
        query = "INSERT INTO recipes (name,description,instructions,under_thirty,created_at,user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under_thirty)s, %(created_at)s, %(current_id)s)"
        return connectToMySQL("users_recipes").query_db(query,data)

    @classmethod
    def get_recipe(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        recipe_db = connectToMySQL("users_recipes").query_db(query,data)
        return cls(recipe_db[0])

    @classmethod
    def edit_recipe(cls,data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, under_thirty = %(under_thirty)s, instructions = %(instructions)s, updated_at = %(updated_at)s WHERE id = %(id)s"
        return connectToMySQL("users_recipes").query_db(query,data)

    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL("users_recipes").query_db(query,data)