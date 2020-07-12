from app.models import ConfigValues
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.decorators.authorisation import user_only


@api_v1.route('/configuration/<string:name>', methods=['GET'])
#@user_only
def user_get_config_value(name=None):
    """
    get_config_value for setting
    
    """
    item = ConfigValues.get_config_value(name)

    return res(item)



