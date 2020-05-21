# app/__init__.py

# third-party imports
from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

# local imports
from config import DevelopmentConfig

# db variable initialization
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(DevelopmentConfig())
    app.config.from_pyfile('config.py')
    db.init_app(app)
    app.config['TESTING'] = True
    # app name

    @app.errorhandler(404)
    # inbuilt function which takes error as parameter
    def not_found(e):

        # defining function
        flash('404 Page not found')
        return render_template("home/index.html", title='404 page not found')

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)

    Bootstrap(app)
    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    return app
