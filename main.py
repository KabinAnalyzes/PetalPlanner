from flask import Flask, render_template, request, redirect, url_for, flash, blueprint
from flask_login import login_required, current_user
import requests



main= blueprint('main', __name__)

@main.route('/')
def index():
    url = "https://zenquotes.io/api/today"
    response = requests.get(url).json()
    quote = response[0]['q'] + "\r\n - " + response[0]['a']
    return render_template('index.html', quote=quote)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.username)

