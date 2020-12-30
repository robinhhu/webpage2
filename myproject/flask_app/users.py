from flask_app import db
from flask_login import UserMixin

collect = db.Table('collect',
    db.Column('postId', db.Integer, db.ForeignKey('post.id'),primary_key=True),
    db.Column('userId', db.Integer, db.ForeignKey('user.id'),primary_key=True)
)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80),unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(400))
    post = db.relationship('Post', backref='user', lazy=True)
    comment = db.relationship('Comment',backref='user',lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username