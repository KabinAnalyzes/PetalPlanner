from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import UserMixin, LoginManager
import os
import requests
import requests_cache
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
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

@app.route('/index')
def home():
    url = "https://zenquotes.io/api/today"
    response = requests.get(url).json()
    quote = response[0]['q'] + "\r\n - " + response[0]['a']
    return render_template('index.html', quote=quote)

@app.route('/profile')
def profile():
    return "profile"

@app.route('/login')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()
    
    #check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('index')) #if user doesn't exist or password is wrong, reload the page
    
    #if the above check passes, then we know the user has the right credentials
    return redirect(url_for('profile'))

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: #if user is found then we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('register'))
    
    #create new user with form data. Hash the password so plaintext version isn't saved
    new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))

    #add user to database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    return "logout"


if __name__ == '__main__':
    app.run(debug=True)