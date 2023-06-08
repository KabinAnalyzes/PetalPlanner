from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
import requests
from . import db
from datetime import date
from . import cache

main= Blueprint('main', __name__)


@main.route('/')
@cache.cached(timeout=86400)
def index():
    url = "https://zenquotes.io/api/today"
    response = requests.get(url).json()
    author = str(response[0]['a'])
    quote = str(response[0]['q'])
    text = quote + "\r\n - " + author
    return render_template('index.html', quote=text)


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

