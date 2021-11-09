from flask_app import app
from flask import render_template,flash,redirect,request,session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def reg_and_log():
    return render_template("index.html")


@app.route("/register",methods=["POST"])
def create_user():
    if User.validate_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
            "first_name":request.form["first_name"],
            "last_name":request.form["last_name"],
            "email":request.form["email"],
            "password":pw_hash
        }
        current_id = User.insert_user(data)
        session["current_id"] = current_id  # store user id into session
        flash("User created!", "register")
        return redirect("/dashboard")
    else:
        return redirect("/")


@app.route("/login",methods=["POST"])
def login():
    # see if the username exists in the database
    user_in_db = User.get_by_email(request.form)
    # user is not registered
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password", "login")  # if false after checking password
        return redirect("/")
    # if passwords match, set user_id into session
    session["current_id"] = user_in_db.id
    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    flash("logged out!", "login")
    return redirect("/")