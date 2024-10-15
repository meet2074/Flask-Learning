from flask_sqlalchemy import SQLAlchemy
import uuid
# from flask import Flask

# app = Flask(__name__)
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String,primary_key=True,default=str(uuid.uuid4()))
    first_name= db.Column(db.String(80),unique=False, nullable=False)
    last_name = db.Column(db.String(80),unique=False,nullable=False)
    mobile_number=db.Column(db.Integer,unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    