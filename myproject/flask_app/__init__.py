from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#app settings, configure the application
#set secret key to ensure security
#DB and migration folder also created here
app = Flask(__name__)
app.config.from_object('config2')
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'an secret string'
db = SQLAlchemy(app)
migrate = Migrate(app, db,render_as_batch=True,compare_type=True)

#remove default
from flask.logging import default_handler

app.logger.removeHandler(default_handler)


#login settings
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'sign'
USE_SESSION_FOR_NEXT = True
login_manager.login_message = "Please log in to access the previous page"

#logging
import os
import logging
import time
from logging.handlers import RotatingFileHandler

#make file name
def make_dir(make_dir_path):
    path = make_dir_path.strip()
    if not os.path.exists(path):
        os.makedirs(path)

log_dir_name = "Logs"
log_file_name = 'logs-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
log_file_folder = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir)) + os.sep + log_dir_name
make_dir(log_file_folder)
log_file_str = log_file_folder + os.sep + log_file_name

#logging configuration
logging.basicConfig(level=logging.WARNING)
file_log_handler = RotatingFileHandler(log_file_str, maxBytes=1024 * 1024, backupCount=10)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
file_log_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_log_handler)

from flask_app import views
from .users import User

#login manager
@login_manager.user_loader
def user_loader(user_id):
    from .users import User
    user = User.query.get(int(user_id))
    return user
