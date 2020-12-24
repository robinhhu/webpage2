from app import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    subject = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=datetime.today())
    description = db.Column(db.Text,nullable=False)
    ownerId = db.Column(db.String(80),db.ForeignKey('user.id'),nullable=False)


    def __repr__(self):
        return '<Post %r>' % self.id

