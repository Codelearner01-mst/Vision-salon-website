from app import create_app, db
from flask_migrate import Migrate
from app.models import service_model, book_model, team_model, gallery_model, socials_model, time_model, user_model


app = create_app('default')
migrate = Migrate(app, db)
