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
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .service import main as service_blueprint
    app.register_blueprint(service_blueprint)

    from .book import main as book_blueprint
    app.register_blueprint(book_blueprint)

    from .contact import main as contact_blueprint
    app.register_blueprint(contact_blueprint)

    from .gallery import main as gallery_blueprint
    app.register_blueprint(gallery_blueprint)

    from .story import main as story_blueprint
    app.register_blueprint(story_blueprint)

    from .team import main as team_blueprint
    app.register_blueprint(team_blueprint)

    return app