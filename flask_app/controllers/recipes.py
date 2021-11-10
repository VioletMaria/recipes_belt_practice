from werkzeug import datastructures
from flask_app import app
from flask import render_template,flash,redirect,request,session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route("/dashboard")
def user_page():
    if "current_id" not in session:
        flash("Must be logged in!", "register")
        return redirect("/")
    else:
        data = {
            "current_id": session["current_id"]
        }
        user = User.get_user_recipe(data)
        return render_template("dashboard.html", user=user)

@app.route("/view/<int:id>")
def instructions(id):
    if "current_id" not in session:
        flash("Must be logged in!", "register")
        return redirect("/")
    else:
        data = {
            "current_id": session["current_id"],
            "id":id
        }
        user = User.get_user_recipe(data)
        return render_template("recipe.html",user=user)

@app.route("/new")
def new_recipe():
    return render_template("addrecipe.html")

@app.route("/create",methods=["POST"])
def create_recipe():
    if "current_id" not in session:
        flash("Log in please")
        return redirect("/")
    if Recipe.validate_recipe_update(request.form):
        data = {
            "name":request.form["name"],
            "description":request.form["description"],
            "instructions":request.form["instructions"],
            "under_thirty":request.form["under_thirty"],
            "created_at":request.form["created_at"],
            "current_id": session["current_id"]
        }
        Recipe.add_recipe(data)
        flash("Recipe added")
        return redirect("/dashboard")
    else:
        return redirect("/new")

@app.route("/recipes/<int:id>")
def recipe(id):
    data = {
        # "current_id": session["current_id"],
        "id":id
    }
    recipe = Recipe.get_recipe(data)
    return render_template("editrecipe.html", recipe=recipe)

@app.route("/edit/<int:id>", methods=["POST"])
def update_recipe(id):
    if "current_id" not in session:
        flash("Log in please")
        return redirect("/")

    if Recipe.validate_recipe_update(request.form):
        data = {
            "name":request.form["name"],
            "description":request.form["description"],
            "under_thirty":request.form["under_thirty"],
            "instructions":request.form["instructions"],
            "updated_at":request.form["updated_at"],
            "id":id
        }
        Recipe.edit_recipe(data)
        return redirect("/dashboard")
    else:
        return redirect("/recipes")

@app.route("/delete/<int:id>")
def remove_recipe(id):
    if "current_id" not in session:
        flash("Log in please")
        return redirect("/")
    data = {
        "id":id
    }
    Recipe.delete_recipe(data)
    return redirect("/dashboard")