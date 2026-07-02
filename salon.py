from app import create_app, db
from flask_migrate import Migrate

app = create_app('default')
migrate = Migrate(app, db)
