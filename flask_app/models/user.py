from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, request
from flask_app.models.recipe import Recipe
import re
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
pass_regex = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')

class User:
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []
        
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user["first_name"]) < 3:
            flash("First name must be at least 3 characters.", "register")
            is_valid = False
        if len(user["last_name"]) < 3:
            flash("Last name must be at least 3 characters.", "register")
            is_valid = False
        if not email_regex.match(user['email']):
            flash("Invalid Email!", "register")
            is_valid = False
        else:
            valid_email = connectToMySQL("users_recipes")
            query = "SELECT * FROM users WHERE email = %(email)s;"
            data = {
                "email":request.form["email"]
            }
            result = valid_email.query_db(query,data)
            if result != ():
                flash("Existing email, please enter a new email", "register")
                is_valid = False
        if not pass_regex.match(user['password']):
            flash("Password must contain at least 8 characters, at least 1 letter and 1 number.", "register")
            is_valid = False
        if user["confirm_password"] != user["password"]:
            flash("Passwords must match", "register")
            is_valid = False
        return is_valid


    @classmethod
    def insert_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL("users_recipes").query_db(query,data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        user_db = connectToMySQL("users_recipes").query_db(query,data)
        if len(user_db) < 1:
            return False
        return cls(user_db[0])

    @classmethod
    def get_user_recipe(cls,data):
        query = "SELECT * FROM users JOIN recipes ON users.id = recipes.user_id WHERE users.id = %(current_id)s"
        user_recipe_db = connectToMySQL("users_recipes").query_db(query,data)
        user = User(user_recipe_db[0])

        for ur in user_recipe_db:
            recipe_data = {
                "id":ur["recipes.id"],
                "name":ur["name"],
                "description":ur["description"],
                "under_thirty":ur["under_thirty"],
                "instructions":ur["instructions"],
                "created_at":ur["recipes.created_at"],
                "updated_at":ur["recipes.updated_at"],
                "user_id":ur["user_id"]
            }
            user.recipes.append(Recipe(recipe_data))
        return user