from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
import requests
from . import db
from datetime import date
from . import cache
from .models import Todo, Statistics

main = Blueprint("main", __name__)


# Make an API call to zenquotes.io and store in cache for 24 hours
@cache.cached()
def api_call():
    """
    Make an API call to zenquotes.io and store in cache for 24 hours

    :param: None
    :return: (str) quote of the day and author
    """
    url = "https://zenquotes.io/api/today"
    response = requests.get(url).json()
    author = str(response[0]["a"])
    quote = str(response[0]["q"])
    text = quote + "\r\n - " + author
    return text


@main.route("/")
def home():
    return render_template("home.html")


@main.get("/todo")
# query todo table for all todo items for current user
# render index.html with todo_list
@login_required
def index():
    text = api_call()
    todo_list = (
        db.session.query(Todo).filter(Todo.username == current_user.username).all()
    )
    return render_template("index.html", quote=text, todo_list=todo_list)


@main.post("/add")
# title is the name of the input field in index.html
# create new todo item and add to database
# redirect to index page
@login_required
def add():
    title = request.form.get("title")
    category = request.form.get("category")
    new_todo = Todo(title=title, complete=False)
    username = current_user.username
    date_created = date.today()
    new_todo.category = category
    new_todo.date_created = date_created
    new_todo.username = username
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("main.index"))


@main.get("/update/<int:todo_id>")
# update todo item in database as complete or not
# redirect to index page
@login_required
def update(todo_id):
    # query statistics table for current user, with current month and year
    # if it doens't exist, create new row with current month and year
    # query todo table for todo item with todo_id
    if (
        db.session.query(Statistics)
        .filter(
            Statistics.username == current_user.username,
            Statistics.month == date.today().strftime("%B"),
            Statistics.year == date.today().strftime("%Y"),
        )
        .first()
        is None
    ):
        new_stats = Statistics(
            username=current_user.username,
            month=date.today().strftime("%B"),
            year=date.today().strftime("%Y"),
        )
        db.session.add(new_stats)
        db.session.commit()

    stats = (
        db.session.query(Statistics)
        .filter(
            Statistics.username == current_user.username,
            Statistics.month == date.today().strftime("%B"),
            Statistics.year == date.today().strftime("%Y"),
        )
        .first()
    )
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    # check if todo item has been previously completed
    # if not, update todo item as complete and update previously_completed to True
    # update completed_tasks in statistics table for the current month and year
    if todo.previously_completed == False:
        todo.complete = not todo.complete
        todo.previously_completed = True
        stats.completed_tasks += 1
        db.session.commit()

    else:
        todo.complete = not todo.complete
        db.session.commit()
    return redirect(url_for("main.index"))


@main.get("/delete/<int:todo_id>")
# delete todo item from database
# redirect to index page
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("main.index"))


@main.route("/profile")
# redirects to profile page with current user's username and statistics for the current month and year
@login_required
def profile():
    monthly_stats = (
        db.session.query(Statistics)
        .filter(
            Statistics.username == current_user.username,
            Statistics.month == date.today().strftime("%B"),
            Statistics.year == date.today().strftime("%Y"),
        )
        .first()
    )
    if monthly_stats is None:
        monthly_stats = 0
        month = date.today().strftime("%B")
        year = date.today().strftime("%Y")
    else:
        monthly_stats = monthly_stats.completed_tasks
        month = date.today().strftime("%B")
        year = date.today().strftime("%Y")
    return render_template(
        "profile.html",
        name=current_user.username,
        tasks=monthly_stats,
        month=month,
        year=year,
    )
