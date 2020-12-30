from flask_app import db
from datetime import datetime
from .users import collect

like = db.Table('like',
    db.Column('postId', db.Integer, db.ForeignKey('post.id'),primary_key=True),
    db.Column('userId', db.Integer, db.ForeignKey('user.id'),primary_key=True)
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    subject = db.Column(db.String(50))
    imgFile = db.Column(db.String(128))
    date = db.Column(db.DateTime, default=datetime.today())
    description = db.Column(db.Text,nullable=False)
    ownerId = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    comment = db.relationship('Comment', backref='post', lazy=True)
    like = db.relationship('User', secondary=like, lazy='subquery',
                           backref=db.backref('posts', lazy=True))
    collect = db.relationship('User', secondary=collect, lazy='subquery',
                           backref=db.backref('Post', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.id



