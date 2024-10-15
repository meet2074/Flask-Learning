from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from jose import jwt
from config import Env
from model import User
from schemas import CreateUser
from datetime import timedelta, timezone, datetime

algo = "HS256"
access_token_exp_time = 500
refresh_token_exp_time = 1000


def create_user(db: SQLAlchemy, user: CreateUser):
    try:
        data = User(
            first_name=user.first_name,
            last_name=user.last_name,
            mobile_number=user.mobile_number,
            email=user.email,
        )
        db.session.add(data)
        db.session.commit()
        db.session.refresh(data)
        # db.session.close()
        
    except Exception as err:
        return jsonify({"error": str(err)})


def create_access_token(email: str):
    try:
        data = User.query.filter(email==email).one()
        payload = {"id": data.id, "name": data.first_name, "sub": "access_token"}
        payload.update(
            {
                "exp": datetime.now(tz=timezone.utc)
                + timedelta(hours=access_token_exp_time)
            }
        )
        token = jwt.encode(payload, key=Env.key, algorithm=algo)
        return token
    except Exception as err:
        return jsonify({"error": str(err)})


def create_refresh_token(email: str):
    try:
        data = User.query.filter(email==email).one()
        payload = {"id": data.id, "name": data.first_name, "sub": "access_token"}
        payload.update(
            {
                "exp": datetime.now(tz=timezone.utc)
                + timedelta(hours=refresh_token_exp_time)
            }
        )
        token = jwt.encode(payload, key=Env.key, algorithm=algo)
        return token
    except Exception as err:
        return jsonify({"error": str(err)})


def decode_token(token: str):
    try:
        payload = jwt.decode(token, key=Env.key, algorithms=algo)

        if payload is None:
            return jsonify({"error": "No payload in token"})
        return payload
    except Exception as err:
        return jsonify({"error": str(err)})


def get_user(uid:str):
    # try:
    data = User.query.filter(id==uid).one()
    breakpoint()
    return data
    # except Exception as err:
    #     return jsonify({"error":str(err)})

def update_user(id:str,updated_data:dict,db:SQLAlchemy):
    try:
        data = User.query.filter(id==id).one()
        # breakpoint()
        
        if updated_data.first_name is not None:
            data.first_name = updated_data.first_name
        if updated_data.last_name is not None:
            data.last_name = updated_data.last_name
        if updated_data.mobile_number is not None:
            data.mobile_number = updated_data.mobile_number
        if updated_data.email is not None:
            data.email = updated_data.email

        db.session.commit()
        
    except Exception as err:
        return jsonify({"error":str(err)})

def delete_user(uid:str,db:SQLAlchemy):
    try:
        user = User.query.filter(id==uid).one_or_none()
        # db.Query(User).filter(id==uid).delete()
        # breakpoint()
        db.session.delete(user)
        db.session.commit()
        db.session.refresh(user)
    except Exception as err:
        return jsonify({"error":str(err)})
