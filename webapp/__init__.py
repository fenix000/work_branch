from flask import Flask, request, current_app
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import logging
from logging.handlers import RotatingFileHandler
import os

from webapp.admin.views import blueprint as admin_bp
from webapp.db import db

from webapp.user.forms import LoginForm
from webapp.user.models import User


login = LoginManager()
login.login_view = 'user.login'


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    login.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(admin_bp)

    from webapp.log.views import blueprint as log_bp
    app.register_blueprint(log_bp)

    from webapp.error.handlers import blueprint as errors_bp
    app.register_blueprint(errors_bp)

    from webapp.user.views import blueprint as user_bp
    app.register_blueprint(user_bp)

    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/log.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Work_log startup')


    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
