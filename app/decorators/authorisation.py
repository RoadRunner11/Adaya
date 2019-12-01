from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app.models import User
from flask import abort, has_request_context
from app.helper.enum import ErrorMessages, Roles
from app.helper.utility import res
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
                    return res('', ErrorMessages.AUTHENTICATION_FAILED, 403)
                email = get_jwt_identity()
                # Verify if user is in the right role
                if not User.authorisation(email, roles):
                    return res('', ErrorMessages.AUTHORISATION_FAILED, 403)
            else:
                abort(500)
            return function(*args, **kwargs)
        return wrapper
    return decorater


def user_only(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if has_request_context():
            try:
                verify_jwt_in_request()
            except:
                return res('', ErrorMessages.AUTHENTICATION_FAILED, 403)
        else:
            abort(500)
        return function(*args, **kwargs)
    return wrapper


@permitted_roles([Roles.ADMIN])
def admin_only(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
    return wrapper
