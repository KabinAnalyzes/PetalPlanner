from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
import requests
from . import db
from datetime import date
from . import cache
from .models import Todo

main= Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.get('/todo')
#@cache.cached(timeout=86400)
@login_required
def index():
    url = "https://zenquotes.io/api/today"
    response = requests.get(url).json()
    author = str(response[0]['a'])
    quote = str(response[0]['q'])
    text = quote + "\r\n - " + author
    todo_list = db.session.query(Todo).all()
    return render_template('index.html', quote=text, todo_list=todo_list)

@main.post('/add')
@login_required
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("main.index"))

@main.get("/update/<int:todo_id>")
@login_required
def update(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("main.index"))

@main.get("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("main.index"))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

