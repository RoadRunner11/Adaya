from app.models import User, Role
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.decorators.authorisation import admin_only


@api_v1.route('/connect/users', methods=['GET'])
@api_v1.route('/connect/users/<string:email>', methods=['GET'])
# @admin_only
def get_users(email=None):
    """
    get_users gets all user or specify user

    Args:
        email ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    page, per_page = get_page_from_args()
    items = [User.get_user_by_email(email)] if email else User.get(
        page=page, per_page=per_page)
    return res([item.as_dict() for item in items])

@api_v1.route('/connect/users/pagination', methods=['GET'])
#@admin_only
def get_users_pages(email=None):
    """
    get_users gets all user or specify user

    Args:
        email ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    page, per_page = get_page_from_args()
    
    page_details =  User.get_page_details(page=page, per_page=per_page)

    return res({"total_items": page_details.total, "no_of_pages": page_details.pages, "per_page": page_details.per_page})

@api_v1.route('/connect/users/<string:email>', methods=['PUT'])
# @admin_only
def update_user(email):
    """
    update_user updates user by using email

    Args:
        email (string): 

    Returns:
        (string,int): user info if update succesful, otherwise response no need to update
    """
    item = User.get_user_by_email(email)
    if not item:
        return Responses.NOT_EXIST()
    json_dict = request.json
    if len(item.update(json_dict)) > 0:
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()


@api_v1.route('/connect/users', methods=['POST'])
# @admin_only
def add_user():
    json_dict = request.json
    if 'email' not in json_dict:
        return Responses.OPERATION_FAILED(Messages.EMAIL_EMPTY)
    existing_item = User.get_user_by_email(json_dict['email'])
    if existing_item:
        return Responses.OBJECT_EXIST(Messages.EMAIL_EXIST)
    # set admin email to confirmed
    role = Role.query.get(json_dict['role_id'])
    if(role.name == "admin"):
        json_dict['email_confirmed'] = True
    item = User()
    error = item.insert_as_new_item(json_dict)
    if len(error) > 0:
        return Responses.OPERATION_FAILED(error)
    return res(item.as_dict())


@api_v1.route('/connect/users/<string:email>', methods=['DELETE'])
# @admin_only
def delete_user(email=None):
    """
    get_users gets all user or specify user

    Args:
        email ([type], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """
    item = User.get_user_by_email(email)
    error = item.delete()
    if len(error) > 0:
        return Responses.OPERATION_FAILED(error)
    return Responses.SUCCESS()