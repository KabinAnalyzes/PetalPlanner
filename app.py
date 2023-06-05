from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import requests
import requests_cache
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(32), index=True, unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return '<User %r>' % self.username

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(500), index=True, unique=True)
    author = db.Column(db.String(32), index=True, unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return '<Quote %r>' % self.quote

@app.route('/home')
def home():
    return render_template('placehold.html')

@app.route('/Login')
def index():
    return render_template('login.html')

@app.route('/Register')
def register():
    return render_template('register.html')

@app.route('/test',)
def test():
    url = "https://zenquotes.io/api/today"
    response = requests.get(url).json()
    quote = response[0]['q'] + "\r\n - " + response[0]['a']
    return render_template('index.html', quote=quote)
    

if __name__ == '__main__':
    app.run(debug=True)