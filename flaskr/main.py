from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
import requests
from . import db
from datetime import date
from . import cache
from .models import Todo

main = Blueprint('main', __name__)

# Make an API call to zenquotes.io and store in cache for 24 hours
@cache.cached()
def api_call():
    url = "https://zenquotes.io/api/today"
    response = requests.get(url).json()
    author = str(response[0]['a'])
    quote = str(response[0]['q'])
    text = quote + "\r\n - " + author
    return text

@main.route('/')
def home():
    return render_template('home.html')

@main.get('/todo')
# require login to access todo page, if not logged in, redirect to login page (WIP)
# store api call in text variable and call it in index.html
# query all todo items from database and store in todo_list variable and call it in index.html
@login_required
def index():
    text = api_call()
    todo_list = db.session.query(Todo).filter(Todo.username == current_user.username).all()
    return render_template('index.html', quote=text, todo_list=todo_list)

@main.post('/add')
# title is the name of the input field in index.html
# create new todo item and add to database
# redirect to index page
@login_required
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    username = current_user.username
    new_todo.username = username
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("main.index"))

@main.get("/update/<int:todo_id>")
# update todo item in database as complete or not 
# redirect to index page
@login_required
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
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

@main.route('/profile')
# redirect to profile page which will display user information (WIP)
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

