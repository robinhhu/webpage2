from flask_app import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    subject = db.Column(db.String(50))
    message = db.Column(db.String(200))

    def __repr__(self):
        return '<Contact %r>' % self.name
