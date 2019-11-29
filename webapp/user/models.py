from datetime import datetime
from hashlib import md5
from flask_login import UserMixin
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, BooleanField, SubmitField

from webapp.db import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    fullname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=False, nullable=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String, index=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    docs = db.relationship('Doc', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    phone = db.Column(db.String(30), nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.now)

    def avatar(self, size):
        pass

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == "admin"

    def __repr__(self):
        return '<Username {}>'.format(username)
