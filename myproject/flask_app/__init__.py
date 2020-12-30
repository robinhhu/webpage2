from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config2')
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'an secret string'
db = SQLAlchemy(app)
migrate = Migrate(app, db,render_as_batch=True,compare_type=True)

#login settings
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'sign'
USE_SESSION_FOR_NEXT = True
login_manager.login_message = "Please log in to access the previous page"


from flask_app import views
from .users import User

@login_manager.user_loader
def user_loader(user_id):
    from .users import User
    user = User.query.get(int(user_id))
    return user