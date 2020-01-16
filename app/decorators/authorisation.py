from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, create_access_token
from app.models import User
from flask import abort, has_request_context
from app.helpers.enum import Messages, Roles
from app.helpers.utility import res
from functools import wraps


def permitted_roles(roles):
    """
    permitted_roles verifies both user authentication as well as user roles

    Args:
        roles ([strings]): user will need to be in one of the roles to access api

    """
    def decorater(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # Verify if user token is valid (logginged)
            if has_request_context():
                try:
                    verify_jwt_in_request()
                except:
                    return res('', Messages.AUTHENTICATION_FAILED, 401)
                email = get_jwt_identity()
                user = User.get_user_by_email(email)
                # Verify if user exists or not
                if not user:
                    return res('', Messages.AUTHENTICATION_FAILED, 401)
                # Verify if user is in the right role
                if len(roles) > 0:
                    # only check if requires role is more than 0
                    if not User.authorisation(email, roles):
                        return res('', Messages.AUTHORISATION_FAILED, 403)
            response = function(*args, **kwargs)
            # add new token to the response header
            response[0].headers.set(
                'new_token', create_access_token(identity=email))
            return response
        return wrapper
    return decorater


def user_only(function):
    @permitted_roles([])
    @wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
    return wrapper


def admin_only(function):
    @permitted_roles([Roles.ADMIN])
    @wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
    return wrapper
