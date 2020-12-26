from app import db
from datetime import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ownerId = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    date = db.Column(db.DateTime,default=datetime.today())
    content = db.Column(db.Text,nullable=False)
    postId = db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False)

    def __repr__(self):
        return '<Comment %r>' % self.id