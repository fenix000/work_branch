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

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    body = db.Column(db.Text)
    image = db.Column(db.String, nullable = True)

# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))
