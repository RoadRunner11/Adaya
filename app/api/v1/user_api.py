from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.api.v1 import api_v1
from app.models import User
from app.helpers.enum import Messages,Roles,Responses
from app.helpers.utility import res
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.decorators.authorisation import permitted_roles,user_only


@api_v1.route('/users/token', methods=['POST'])
def request_token():
    """
    request_token takes in email and password, returns the authentication token 

    Returns:
        [type]: [description]
    """
    if request.json is None:
        return Responses.OPERATION_FAILED()
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = User.authenticate(email, password)
    if user:
        token = create_access_token(identity=user.email)
        return res(token)
    return Responses.AUTHENTICATION_FAILED()


@api_v1.route('/users', methods=['GET'])
@user_only
def get_current_user():
    """
    get_user retruns user info for my account page
    
    Returns:
        (json string, status)
    """
    email = get_jwt_identity()
    user = User.get_user_by_email(email)
    return res(user.as_dict())

@api_v1.route('/users', methods=['POST'])
def create_user():
    """
    creates a new user
    
    """
    json_dict = request.json
    item = User()
    item.update_from_dict(json_dict)
    existing_item = User.get_user_by_email(json_dict['email'])
    if existing_item:
        return Responses.OBJECT_EXIST()
    error = item.update(json_dict)
    if len(error) > 0:
        return Responses.OPERATION_FAILED()
    return res(item.as_dict())    

  