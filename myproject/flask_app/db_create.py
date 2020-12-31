from flask_app import db


#create the database
if __name__ == '__main__':
    db.create_all()