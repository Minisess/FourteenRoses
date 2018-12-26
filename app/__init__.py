from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app


def create_db(app):
    new_db = SQLAlchemy(app)
    new_migrate = Migrate(app, new_db)
    return new_db, new_migrate


app = create_app()
db, migrate = create_db(app)

login = LoginManager(app)
login.login_view = 'login'

bootstrap = Bootstrap(app)

from app import routes, models
