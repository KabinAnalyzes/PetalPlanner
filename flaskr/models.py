from sqlalchemy.sql import func
from flask_login import UserMixin
from. import db

# This is the database model for the user and todo items 
# The UserMixin class provides default implementations for the methods that Flask-Login expects user objects to have.

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(32), index=True, unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return '<User %r>' % self.username

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String(32), index=True, unique=True)
    title = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean)

    def __repr__(self):
        return '<Task %r>' % self.id