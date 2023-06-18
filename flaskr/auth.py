from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required

auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    # login code goes here
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(
            url_for("auth.login")
        )  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for("main.index"))


@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get("email")
    username = request.form.get("name")
    password = request.form.get("password")

    user_email = User.query.filter_by(
        email=email
    ).first()  # if this returns a user, then the email already exists in database
    user_username = User.query.filter_by(
        username=username
    ).first()  # if this returns a user, then the username already exists in database

    if (
        user_email
    ):  # if user is found then we want to redirect back to signup page so user can try again
        flash("Email address already exists")
        return redirect(url_for("auth.signup"))
    elif user_username:
        flash("Username already exists")
        return redirect(url_for("auth.signup"))

    # create new user with form data. Hash the password so plaintext version isn't saved
    new_user = User(
        email=email,
        username=username,
        password=generate_password_hash(password, method="pbkdf2"),
    )

    # add user to database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
