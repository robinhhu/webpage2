import os
# configure the database
basedir = os.path.abspath(os.path.dirname(__file__))
# The database storing data
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# track the objects
SQLALCHEMY_TRACK_MODIFICATIONS = True