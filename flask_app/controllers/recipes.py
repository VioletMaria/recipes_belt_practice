from flask_app import app
from flask import render_template,flash,redirect,request,session
from flask_app.models.user import User
from flask_app.models.user import Recipe

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
            "id":id,
            "current_id": session["current_id"]
        }
        user = User.get_user_recipe(data)
        return render_template("recipe.html",user=user)