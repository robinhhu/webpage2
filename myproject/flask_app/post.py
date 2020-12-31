from flask_app import db
from datetime import datetime
from .users import collect

#The like table indicates a many to many relationship
#between users and posts.
#In another word, a user can like various number of posts
#meanwhile a post can be liked by multiple users
like = db.Table('like',
    db.Column('postId', db.Integer, db.ForeignKey('post.id'),primary_key=True),
    db.Column('userId', db.Integer, db.ForeignKey('user.id'),primary_key=True)
)

#The post is an instance class that stored vital information
#about the post. Such as title, subject, img, description, etc.
#We use id as our primary key, and an ownerId as our foreign
#key, which means every post should be posted by a user of the
#website.
#Comment, like and collect are all relationship to another instance
#class or relationship
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



