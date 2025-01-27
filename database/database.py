from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy()

def init_database(app):
    db.init_app(app)
    migrate = Migrate(app, db)

