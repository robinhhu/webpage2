from app import db
from flask_login import UserMixin


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80),unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % self.username