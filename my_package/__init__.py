from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ada2341414#21414@!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/pathsala'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from my_package import models
from my_package import routes
