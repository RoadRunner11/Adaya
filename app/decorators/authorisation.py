from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, create_access_token, set_access_cookies
from app.models import User
from flask import abort, has_request_context
from app.helpers.enum import Messages, Roles, Responses
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
                except Exception as e:
                    return Responses.AUTHENTICATION_FAILED()
                identity = get_jwt_identity()
                email = User.get_email_from_identity(identity)
                if not email:
                    return Responses.AUTHENTICATION_FAILED()
                #TODO add check if email is activated
                # Verify if user is in the right role
                if not User.authorisation(email, roles):
                    return Responses.AUTHORISATION_FAILED()
            response, status = function(*args, **kwargs)
            set_access_cookies(response, create_access_token(
                identity=User.generate_token_identity(email)))
            return response, status
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
