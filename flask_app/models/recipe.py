from flask_app.config.mysqlconnection import connectToMySQL


class Recipe:
    def __init__(self,data):
        self.name = data["name"]
        self.description = data["description"]
        self.under_thirty = data["under_thirty"]
        self.instructions = data["instructions"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def add_recipe(self,data):
        query = "INSERT INTO recipes (name,description,instructions,under_thirty,created_at,user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under_thirty)s, %(created_at)s, %(current_id)s)"
        return connectToMySQL("users_recipes").query_db(query,data)

    @classmethod
    def edit_recipe(self,data):
        query = "UPDATE recipes SET name = %(name)s,"