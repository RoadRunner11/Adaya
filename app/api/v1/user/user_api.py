from flask import jsonify, request, flash, Flask, request, url_for, render_template
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from app.api.v1 import api_v1
from app.models import User
from app.models.config_values import ConfigValues
from app.helpers.enum import Messages, Roles, Responses
from app.helpers.utility import res
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.decorators.authorisation import permitted_roles, user_only
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from app import mail
from app import templates
from datetime import datetime
import webbrowser

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
    # ensure email is confirmed
    if not user.email_confirmed:
        user.send_confirmation_email(user.email)
        return Responses.UNCONFIRMED_USER()

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
    user = User()
    user.update_from_dict(json_dict, ['id', 'role_id', 'role'])
    existing_user = User.get_user_by_email(json_dict['email'])
    if existing_user:
       return Responses.OBJECT_EXIST()
    error = user.update()
    if len(error) > 0:
        return Responses.OPERATION_FAILED()
    user.send_confirmation_email(json_dict['email'])
    flash('Thanks for registering!  Please check your email to confirm your email address.', 'success')
    return res(user.as_dict())

@api_v1.route('/users/<string:email>', methods=['PUT'])
def update_user_information(email):
    """
    updates user by using email

    Args:
        email (string): 

    Returns:
        (string,int): user info if update succesful, otherwise response no need to update
    """
    user = User.get_user_by_email(email)
    if not user:
        return Responses.NOT_EXIST()
    
    json_dict = request.json
    if len(user.update(json_dict)) > 0: #['password']
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()

@api_v1.route('/users/password_reset', methods=['POST'])
def password_reset():
    json_dict = request.json
    email = json_dict['email']
    user = User.get_user_by_email(email)
    if not user:
        return Responses.NOT_EXIST()
    
    user.send_password_reset_email(email)
    
@api_v1.route('/users/password_reset/<token>')
def password_reset_with_token(token):
    passwordnewurl = '/user-new-password'
    passwordfailureurl = '/user-password-reset-failure'

    secret_key = ConfigValues.get_config_value('EMAIL_PASSWORD_RESET_SECRET_KEY')

    password_reset_serializer = URLSafeTimedSerializer(secret_key)
    
    try:
        email = password_reset_serializer.loads(token, salt='password-reset', max_age=3600)
    except SignatureExpired:
        webbrowser.open_new_tab(passwordfailureurl + 'doc/')
        return
        #return Responses.TOKEN_EXPIRED()   
    
    webbrowser.open_new_tab(passwordnewurl + 'doc/')
    
@api_v1.route('/users/password_update', methods=['PUT'])
def password_update():
    json_dict = request.json
    user = User.get_user_by_email(json_dict['email'])
    
    #passwordurlsuccess = 'http://localhost:8010/user-password-reset-confirmation'
    #passwordurlfailure = 'http://localhost:8010/user-password-reset-failure'

    error = user.update(json_dict['password'])

    if len(error) > 0:
        #webbrowser.open_new_tab(passwordurlfailure + 'doc/')
        return Responses.OPERATION_FAILED()
    else:
        #webbrowser.open_new_tab(passwordurlsuccess + 'doc/')
        return Responses.SUCCESS()

@api_v1.route('/users/confirm_email/<token>')
def confirm_email(token):
    # Open email confirmation URL in a new tab, if a browser window is already open.
    urlsuccess = '/user-email-confirmation'
    urlfailure = '/user-email-failure'


    secret_key = ConfigValues.get_config_value('EMAIL_PASSWORD_RESET_SECRET_KEY')

    confirm_serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = confirm_serializer.loads(token, salt='email-confirm', max_age=3600)
    except SignatureExpired:
        webbrowser.open_new_tab(urlfailure + 'doc/')
        return
        #return Responses.TOKEN_EXPIRED()

    user = User.get_user_by_email(email)
    if not user:
        webbrowser.open_new_tab(urlfailure + 'doc/')
        return
        #return Responses.NOT_EXIST()
    
    user.email_confirmed = True
    user.email_confirmed_on = datetime.now()
    
    error = user.update()
    if len(error) > 0:
        user.delete()
        webbrowser.open_new_tab(urlfailure + 'doc/')
        #return Responses.OPERATION_FAILED()
    else:
        webbrowser.open_new_tab(urlsuccess + 'doc/')
        #return Responses.SUCCESS()


@api_v1.route('/users/contact_us', methods=['POST'])
def contact_us():
    json_dict = request.json
    email = json_dict['email']
    subject = json_dict['subject']
    name = json_dict['name']
    message = json_dict['message']
    
    User.contact_us_email(email, subject, name, message)
    
    return Responses.SUCCESS()