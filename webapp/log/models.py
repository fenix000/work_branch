from datetime import datetime

from wtforms import StringField, PasswordField, BooleanField, SubmitField

from webapp.db import db
from webapp.user.models import User


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}'.format(self.body)


class Doc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True, index=True)
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('docs', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, category, timestamp=None):
        self.title = title
        self.body = text
        if timestamp is None:
            timestamp = datetime.utcnow()
        self.timestamp = timestamp
        self.category = category

    def __repr__(self):
        return '<Doc {}'.format(self.body)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category {}'.format(self.body)
