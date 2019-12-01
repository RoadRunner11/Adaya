from app.models import User
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.decorators.authorisation import admin_only


@api_v1.route('/connect/users', methods=['GET'])
@api_v1.route('/connect/users/<string:email>', methods=['GET'])
@admin_only
def get_users(email=None):
    """
    get_users gets all user or specify user

    Args:
        email ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    page = parse_int(request.args.get('page')) or 1
    per_page = parse_int(request.args.get('per_page')) or 10
    users = [User.get_user_by_email(email)] if email else User.get(
        page=page, per_page=per_page)
    return res([user.as_dict() for user in users])


@api_v1.route('/connect/users/<string:email>', methods=['PUT'])
@admin_only
def update_user(email):
    """
    update_user updates user by using email

    Args:
        email (string): 

    Returns:
        (string,int): user info if update succesful, otherwise response no need to update
    """
    user = User.get_user_by_email(email)
    if not user:
        return Responses.NOT_EXIST()
    json_dict = request.json
    if len(user.update(json_dict)) > 0:
        return res(user.as_dict())
    return Responses.SUCCESS()


@api_v1.route('/connect/users', methods=['POST'])
@admin_only
def add_user():
    json_dict = request.json
    user = User()
    user.update_from_dict(json_dict)
    existing_user = User.get_user_by_email(json_dict['email'])
    if existing_user:
        return Responses.OBJECT_EXIST()
    error = user.update()
    if len(error) > 0:
        return Responses.OPERATION_FAILED()
    return res(user.as_dict())
