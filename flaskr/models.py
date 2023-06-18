from sqlalchemy.sql import func
from flask_login import UserMixin
from . import db

# This is the database model for the user and todo items
# The UserMixin class provides default implementations for the methods that Flask-Login expects user objects to have.


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(32), index=True, unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return "<User %r>" % self.username
    
    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=False)
    category = db.Column(db.String(32), index=True, unique=False)
    title = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    previously_completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Task %r>" % self.id

class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), db.ForeignKey('user.username'))
    month = db.Column(db.String(32), index=True, unique=False)
    year = db.Column(db.String(32), index=True, unique=False)
    completed_tasks = db.Column(db.Integer, default=0)

    user = db.relationship("User", backref="statistics", lazy=True)

    def __repr__(self):
        return "<Statistics %r>" % self.id
