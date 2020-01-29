from flask import jsonify, request, flash, Flask, request, url_for, render_template
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from app.api.v1 import api_v1
from app.models import User
from app.helpers.enum import Messages, Roles, Responses
from app.helpers.utility import res
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.decorators.authorisation import permitted_roles, user_only
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from app import mail
from app import templates
from datetime import datetime

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
        token = create_access_token(identity=user.token_identity())
        response, status = res()
        set_access_cookies(response, token)
        # set token to httponly cookies
        return response, status
    return Responses.AUTHENTICATION_FAILED()


@api_v1.route('/users/token', methods=['DELETE'])
def remove_token():
    response, status = res()
    unset_jwt_cookies(response)
    return response, status


@api_v1.route('/users', methods=['GET'])
@user_only
def get_current_user():
    """
    get_user retruns user info for my account page

    Returns:
        (json string, status)
    """
    identity = get_jwt_identity()
    email = User.get_email_from_identity(identity)
    if not email:
        return Responses.AUTHENTICATION_FAILED()
    user = User.get_user_by_email(email)
    return res(user.as_dict())


@api_v1.route('/users', methods=['POST'])
def register_user():    
    """
    registers a new user

    """
    json_dict = request.json
    item = User()
    item.update_from_dict(json_dict, ['id', 'role_id', 'role'])
    existing_item = User.get_user_by_email(json_dict['email'])
    if existing_item:
       return Responses.OBJECT_EXIST()
    error = item.update()
    if len(error) > 0:
        return Responses.OPERATION_FAILED()
    item.send_confirmation_email(json_dict['email'])
    flash('Thanks for registering!  Please check your email to confirm your email address.', 'success')
    return res(item.as_dict())

@api_v1.route('/users/<string:email>', methods=['PUT'])
def update_user_information(email):
    """
    updates user by using email

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

@api_v1.route('/users/confirm_email/<token>')
def confirm_email(token):
    confirm_serializer = URLSafeTimedSerializer('Thisisasecret!')
    try:
        email = confirm_serializer.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        return Responses.TOKEN_EXPIRED()

    item = User.get_user_by_email(email)
    if not item:
        return Responses.NOT_EXIST()
    
    item.email_confirmed = True
    item.email_confirmed_on = datetime.now()
    item.update()
    return Responses.SUCCESS()
    
# This are the next things that are needed i believe.
# TODO - User to make payment for order
# TODO - User subscription: to subscribe to service for a period(eg month, 6months, year)
