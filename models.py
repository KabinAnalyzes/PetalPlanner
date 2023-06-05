from sqlalchemy.sql import func
from flask_login import UserMixin
from. import db

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