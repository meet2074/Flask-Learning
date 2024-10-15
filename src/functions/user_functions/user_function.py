from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from jose import jwt
from config import Env
from src.resources.user.model import User
from src.resources.user.schemas import CreateUser
from datetime import timedelta, timezone, datetime
import uuid
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import (
    NotFound,
    Conflict,
    BadRequest,
)

algo = "HS256"
access_token_exp_time = 500
refresh_token_exp_time = 1000


def create_user(db: SQLAlchemy, user: CreateUser):
    try:
        data = User(
            id=str(uuid.uuid4()),
            first_name=user.first_name,
            last_name=user.last_name,
            mobile_number=user.mobile_number,
            email=user.email
        )
        # breakpoint()
        db.session.add(data)
        db.session.commit()
        db.session.refresh(data)
    except IntegrityError as err:
        raise Conflict("User already exist!")
    except Exception as err:
        raise BadRequest("A database error!")


def create_access_token(email: str):
    try:
        data = User.query.filter(User.email == email).first()
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
        raise jsonify({"error": str(err)})


def create_refresh_token(email: str):
    try:
        data = User.query.filter(email == email).first()
        payload = {"id": data.id, "name": data.first_name, "sub": "refresh_token"}
        payload.update(
            {
                "exp": datetime.now(tz=timezone.utc)
                + timedelta(hours=refresh_token_exp_time)
            }
        )
        token = jwt.encode(payload, key=Env.key, algorithm=algo)
        return token
    except Exception as err:
        raise jsonify({"error": str(err)})


def decode_token(token: str):
    try:
        payload = jwt.decode(token, key=Env.key, algorithms=algo)
        if payload is None:
            return jsonify({"error": "No payload in token"})
        return payload
    except Exception as err:
        return jsonify({"error": str(err)})


def get_user(uid: str):
    data = User.query.filter_by(id=uid).first()
    if data:
        return data
    else:
        raise NotFound("user not found!")


def update_user(id: str, updated_data: dict, db: SQLAlchemy):
    data = User.query.filter(User.id == id).first()
    if data:
        if updated_data.get("first_name") is not None:
            data.first_name = updated_data.get("first_name")
        if updated_data.get("last_name") is not None:
            data.last_name = updated_data.get("last_name")
        if updated_data.get("mobile_number") is not None:
            data.mobile_number = updated_data.get("mobile_number")
        if updated_data.get("email") is not None:
            data.email = updated_data.get("email")
        db.session.commit()
    else:
        raise NotFound("user not found!")


def delete_user(uid: str, db: SQLAlchemy):
    try:
        user = User.query.filter(User.id == uid).first_or_404()
        db.session.delete(user)
        db.session.commit()
        db.session.refresh(user)
    except Exception as err:
        return jsonify({"error": str(err)}), 404
