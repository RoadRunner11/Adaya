from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.api.v1 import api_v1
from app.models import User
from app.helper.enum import ErrorMessages,Roles
from app.helper.utility import res
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.decorators.authorisation import permitted_roles


@api_v1.route('/users/token', methods=['POST'])
def login():
    """
    login takes in email and password, returns the authentication token 

    Returns:
        [type]: [description]
    """
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = User.authenticate(email, password)
    if user:
        token = create_access_token(identity=user.email)
        return res(token)
    return res('', ErrorMessages.AUTHENTICATION_FAILED, 400)


@api_v1.route('/users', methods=['GET'])
@jwt_required
def get_user():
    email = get_jwt_identity()
    user = User.get_user_by_email(email)
    return res(user.as_dict())