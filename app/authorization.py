import json
from datetime import datetime, timedelta

import jwt
from flask import Blueprint, Response, jsonify, request

from app import app, db

from .models import User
from .serializer import UserSerializer

bp_authorization = Blueprint('authorization', __name__)


@app.route('/api/auth/register', methods=['POST'])
def register():
    serializer = UserSerializer(many=False)
    email = request.json['email']
    password = request.json['password']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    new_user = User(
        email,
        password,
        first_name,
        last_name
    )
    db.session.add(new_user)
    db.session.commit()
    response_json = jsonify(
        data=serializer.dump(new_user),
        message="user added"
    )
    return response_json, 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    serializer = UserSerializer(many=False)
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user == None:
        return jsonify({
            "data": "",
            "message": "user not registered"
        }), 400
    if not user.verify_password(password):
        return jsonify({
            "data": "",
            "message": "incorrect credentials"
        }), 400
    payload = {
        "id": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=10)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'])
    return jsonify({
        "token": token.decode('UTF-8'),
        "message": ""
    }), 200
