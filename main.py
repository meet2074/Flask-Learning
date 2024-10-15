from flask import Flask, request,jsonify
from config import Env
import crud
from schemas import CreateUser,UpdateUser
from model import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from datetime import datetime ,timezone,timedelta
from flask_migrate import Migrate

app = Flask(__name__)

# key = Env.key

 
app.config["SQLALCHEMY_DATABASE_URI"] = Env.url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = str(Env.key)

jwt = JWTManager(app)

db.init_app(app)

with app.app_context():
    db.create_all()
migrate = Migrate(app,db)


@app.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    user = CreateUser(**data)
    crud.create_user(db,user)
    access_token = crud.create_access_token(user.email)
    refresh_token = crud.create_refresh_token(user.email)
    return jsonify({"access_token":str(access_token),"refresh_token":str(refresh_token)})
        
@app.route("/get/<string:id>",methods=["GET"])
@jwt_required()
def read(id):
    data = crud.get_user(id)
    # breakpoint()  
    return {"first_name":data.first_name,"last_name":data.last_name,"mobile_number":data.mobile_number,"email":data.email}
    
@app.route("/update/<string:id>",methods=["PUT"])
@jwt_required()
def update(id):
    data = request.get_json()
    user = UpdateUser(**data)
    crud.update_user(id,user,db)
    return "user Updated successfully!"

@app.route("/delete/<string:id>",methods=["DELETE"])
@jwt_required()
def delete(id):
    crud.delete_user(id,db)
    return "Deleted successfully!"
    
    


if __name__ == "__main__":
    app.run(debug=True)
