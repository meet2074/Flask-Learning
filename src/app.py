from flask import Flask
from flask_jwt_extended import JWTManager
from database.database import init_database
from src.resources.user.api import user_blueprint
from config import Env

app = Flask(__name__)
jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = Env.url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = str(Env.key)

init_database(app)


app.register_blueprint(user_blueprint)
