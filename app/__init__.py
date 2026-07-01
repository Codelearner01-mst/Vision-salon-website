from flask_mail import Mail
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap4
from config import config

db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap4()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    return app