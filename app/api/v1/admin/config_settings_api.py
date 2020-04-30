from app.models import ConfigValues
from app.api.v1 import api_v1
from app.helpers import Messages, Responses
from app.helpers.utility import res, parse_int, get_page_from_args
from flask import jsonify, request
from flask_jwt_extended import create_access_token
from app.decorators.authorisation import admin_only


@api_v1.route('/connect/configuration', methods=['GET'])
@api_v1.route('/connect/configuration/<string:name>', methods=['GET'])
#@admin_only
def get_config_value(name=None):
    """
    get_config_value for setting
    
    """
    item = ConfigValues.get_config_value(name)

    return res(item)


@api_v1.route('/connect/configuration/<string:name>', methods=['PUT'])
#@admin_only
def update_config_value(name):
    """
    update_config_value updates setting by using name

    """
    item = ConfigValues.query.filter_by(name = name).first() 

    if not item:
        return Responses.NOT_EXIST()
    json_dict = request.json

    
    if len(item.update(json_dict)) > 0:
        return Responses.OPERATION_FAILED()
    return Responses.SUCCESS()



