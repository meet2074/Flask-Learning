from flask import Blueprint, request, jsonify
import functions.user_functions.user_function as user_function
from src.resources.user.schemas import CreateUser
from flask_jwt_extended import jwt_required,get_jwt
from database.database import db
from werkzeug.exceptions import NotFound

user_blueprint = Blueprint("user",__name__)

@user_blueprint.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    user = CreateUser(**data)
    user_function.create_user(db, user)
    access_token = user_function.create_access_token(user.email)
    refresh_token = user_function.create_refresh_token(user.email)

    return jsonify({"access_token": access_token, "refresh_token": refresh_token})


@user_blueprint.route("/get/<string:id>", methods=["GET"])
@jwt_required()
def read(id):
    data = user_function.get_user(id)
    
    if data is None:
        raise NotFound("user not found!")
    return {
        "first_name": data.first_name,
        "last_name": data.last_name,
        "mobile_number": data.mobile_number,
        "email": data.email,
    }

@user_blueprint.route("/update", methods=["PUT"])
@jwt_required()
def update():
    data = request.get_json()
    payload = get_jwt()
    user_function.update_user(payload.get("id"),data , db)
    return "Updated successfully!"


@user_blueprint.route("/delete", methods=["DELETE"])
@jwt_required()
def delete():
    payload = get_jwt()
    user_function.delete_user(payload.get("id"),db)
    return "Deleted successfully!"


