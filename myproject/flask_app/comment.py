from flask_app import db
from datetime import datetime

#Comment class, is stored as a table "comment" in app.db
#Every comment is connected to a specific post
#So the postId is used as a not null foreign key
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ownerId = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    date = db.Column(db.DateTime,default=datetime.today())
    content = db.Column(db.Text,nullable=False)
    postId = db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False)

    def __repr__(self):
        return '<Comment %r>' % self.id