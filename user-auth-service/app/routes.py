from flask import request, jsonify
from app import app, db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token
import re


import warnings
from sqlalchemy.exc import SAWarning

warnings.filterwarnings('ignore', category=SAWarning)



@app.route("/user/register", methods=["POST"])
def register():
    data = request.get_json()

    # validation for every field data
    if not data["username"] or not data["email"] or not data["password"]:
        return jsonify({"message": "All fields are required"}), 400

    # validation for accureate email address
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(regex, data["email"]) is not None:
        return jsonify({"message": "Invalid email address"}), 400

    # validation for existing username
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"message": "Username already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user = User(
        username=data["username"], email=data["email"], password_hash=hashed_password
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@app.route("/user/login", methods=["POST"])
def login():
    data = request.get_json()

    # validation for every field data
    if not data["username"] or not data["email"] or not data["password"]:
        return jsonify({"message": "All fields are required"}), 400

    # validation for accureate email address
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(regex, data["email"]) is not None:
        return jsonify({"message": "Invalid email address"}), 400
    
    user = User.query.filter_by(username=data["username"]).first()

    if user and bcrypt.check_password_hash(user.password_hash, data["password"]):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401
